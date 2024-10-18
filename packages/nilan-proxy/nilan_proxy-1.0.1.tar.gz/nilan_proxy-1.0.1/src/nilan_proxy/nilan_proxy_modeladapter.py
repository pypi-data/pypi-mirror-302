import logging
from typing import Dict, List
from collections.abc import Callable
from .models import ( NilanProxyBaseModel, NilanProxyOptima314, NilanProxyOptima312, NilanProxyOptima301, NilanProxyOptima270, NilanProxyOptima260, NilanProxyOptima251, NilanProxyOptima250, NilanProxyCTS400, NilanProxyCTS602, NilanProxyCTS602Light,NilanProxyDatapoint, NilanProxyDatapointKey, NilanProxySetpoint, NilanProxySetpointKey )

_LOGGER = logging.getLogger(__name__)

class NilanProxyModelAdapter:
    _loaded_model: NilanProxyBaseModel
    _current_datapoint_list: Dict[int, List[NilanProxyDatapointKey]] = {}
    _current_setpoint_list: Dict[int, List[NilanProxySetpointKey]] = {}
    _update_handlers: Dict[NilanProxyDatapointKey|NilanProxySetpointKey, List[Callable[[float|int, float|int], None]]] = {}
    """Callable[old_value, new_value]"""

    _values: Dict[NilanProxyDatapointKey|NilanProxySetpointKey, float|int] = {}

    def __init__(self, model:int, device_number:int, slave_device_number:int, slave_device_model:int) -> None:
        model_to_load = NilanProxyModelAdapter.translate_to_model(model, device_number, slave_device_number, slave_device_model)
        if model_to_load == None:
            raise Exception("Invalid model")
        self._loaded_model = model_to_load(device_number, slave_device_number, slave_device_model)
            
        self._current_datapoint_list = {100: self._loaded_model.get_datapoints_for_read()}
        self._current_setpoint_list = {200: self._loaded_model.get_setpoints_for_read()}

    def get_model_name(self) -> str:
        return self._loaded_model.get_model_name()
    
    def get_manufacturer(self) -> str:
        return self._loaded_model.get_manufacturer()

    @staticmethod
    def translate_to_model(model:int, device_number:int, slave_device_number:int, slave_device_model:int) -> Callable[[int,int,int], NilanProxyBaseModel]|None:
        if model == 2010:
            if device_number == 79265:
                return NilanProxyOptima270
        if model == 2020:
            if device_number == 79280:
                return NilanProxyOptima314
        if model == 1040:
            if slave_device_number == 70810:
                if slave_device_model == 26:
                    return NilanProxyOptima260
            if slave_device_number == 79250:
                if slave_device_model == 9:
                    return NilanProxyOptima312
                if slave_device_model == 8:
                    return NilanProxyOptima251
                if slave_device_model == 5:
                    return NilanProxyOptima301
                if slave_device_model == 1:
                    return NilanProxyOptima250
        if model == 1140 or model == 1141:
            if slave_device_number == 72270:
                if slave_device_model == 1:
                    return NilanProxyCTS400
            if slave_device_number == 2763306:
                if slave_device_model == 2:
                    return NilanProxyCTS602Light
                return NilanProxyCTS602
            
        return None

    @staticmethod
    def provides_model(model:int, device_number:int, slave_device_number:int, slave_device_model:int) -> bool:
        return NilanProxyModelAdapter.translate_to_model(model, device_number, slave_device_number, slave_device_model) is not None
    
    def provides_value(self, key: NilanProxyDatapointKey|NilanProxySetpointKey) -> bool:
        if isinstance(key, NilanProxyDatapointKey): return self._loaded_model.model_provides_datapoint(key) 
        return self._loaded_model.model_provides_setpoint(key)

    def has_value(self, key: NilanProxyDatapointKey|NilanProxySetpointKey) -> bool:
        return key in self._values
    
    def get_value(self, key: NilanProxyDatapointKey|NilanProxySetpointKey) -> float|int|None:
        return self._values.get(key)
    
    def get_min_value(self, key: NilanProxySetpointKey) -> float|int|None:
        if self._loaded_model.model_provides_setpoint(key): 
            return self.parse_from_modbus_value(point=self._loaded_model.setpoints[key], value=self._loaded_model.setpoints[key]['min'])
        return None
    
    def get_max_value(self, key: NilanProxySetpointKey) -> float|int|None:
        if self._loaded_model.model_provides_setpoint(key): 
            return self.parse_from_modbus_value(point=self._loaded_model.setpoints[key], value=self._loaded_model.setpoints[key]['max'])
        return None
    
    def get_unit_of_measure(self, key: NilanProxyDatapointKey|NilanProxySetpointKey) -> str|None:
        return self._loaded_model.get_unit_of_measure(key)
    
    def get_setpoint(self, key:NilanProxySetpointKey) -> NilanProxySetpoint|None:
        if not self._loaded_model.model_provides_setpoint(key): return None
        return self._loaded_model.setpoints[key]
    
    def get_setpoint_step(self, key: NilanProxySetpointKey) -> float|int:
        if self._loaded_model.model_provides_setpoint(key):
            if 'step' in self._loaded_model.setpoints[key]:
                divider = self.get_point_divider(self._loaded_model.setpoints[key])    
                step = self.get_point_step(self._loaded_model.setpoints[key]) 
                if divider > 1: return step / divider
                return step
        return 1
     
    def register_update_handler(self, key: NilanProxyDatapointKey|NilanProxySetpointKey, update_method: Callable[[float|int, float|int], None]):
        if not self.provides_value(key): return
        if key not in self._update_handlers:
            self._update_handlers[key] = []
        self._update_handlers[key].append(update_method)
    
    def deregister_update_handler(self, key: NilanProxyDatapointKey|NilanProxySetpointKey, update_method: Callable[[float|int, float|int], None]):
        if not self.provides_value(key): return
        if key not in self._update_handlers: return
        self._update_handlers[key].remove(update_method)

    def notify_all_update_handlers(self) -> None:
        for key in self._update_handlers:
            for method in self._update_handlers[key]:
                method(-1, self._values[key])

    def getDatapointRequestList(self, sequence_id:int) -> List[NilanProxyDatapoint]|None:
        if sequence_id not in self._current_datapoint_list: return None
        return_list:List[NilanProxyDatapoint] = []
        for key in self._current_datapoint_list[sequence_id]:
            return_list.append(self._loaded_model.datapoints[key])
        return return_list
    
    def get_setpoint_request_list(self, sequence_id:int) -> List[NilanProxySetpoint]|None:
        if sequence_id not in self._current_setpoint_list: return None
        return_list:List[NilanProxySetpoint] = []
        for key in self._current_setpoint_list[sequence_id]:
            return_list.append(self._loaded_model.setpoints[key])
        return return_list
    
    def parse_data_response(self, response_seq:int, response_payload:bytes) -> None:
        _LOGGER.debug(f"Got dataresponse with sequence id: {response_seq}")
        if response_seq in self._current_datapoint_list:
            _LOGGER.debug(f"Is a datapoint response")
            self.parse_datapoint_response(response_seq, response_payload)
        if response_seq in self._current_setpoint_list:
            _LOGGER.debug(f"Is a setpoint response")
            self.parse_setpoint_response(response_seq, response_payload)

    def parse_datapoint_response(self, response_seq:int, response_payload:bytes) -> None:
        if response_seq not in self._current_datapoint_list: return None
        decoding_keys = self._current_datapoint_list[response_seq]
        _LOGGER.debug(list(map(lambda tt: tt.value, decoding_keys)))
        response_length = int.from_bytes(response_payload[0:2])
        for position in range(response_length):
            valueKey = decoding_keys[position]
            payload_slice = response_payload[2+position*2:4+position*2]
            old_value = -1
            if valueKey in self._values:
                old_value = self._values[valueKey]
            point = self._loaded_model.datapoints[valueKey]
            signed = self.get_point_signed(point)
            self._values[valueKey] = self.parse_from_modbus_value(point=point, value=int.from_bytes(payload_slice, 'big', signed=signed))
            # _LOGGER.debug(f"New Datapoint value set: {valueKey} = {self.values[valueKey]} (old={old_value}), rawVal={int.from_bytes(payload_slice, 'big', signed=signed)}, point={point}")
            if old_value != self._values[valueKey]:
                if valueKey in self._update_handlers:
                    for method in self._update_handlers[valueKey]:
                        method(old_value, self._values[valueKey])
     
    def parse_setpoint_response(self, response_seq:int, response_payload:bytes) -> None:
        if response_seq not in self._current_setpoint_list: return None
        decoding_keys = self._current_setpoint_list[response_seq]
        _LOGGER.debug(list(map(lambda tt: tt.value, decoding_keys)))
        response_length = int.from_bytes(response_payload[1:3])
        for position in range(response_length):
            valueKey = decoding_keys[position]
            payload_slice = response_payload[3+position*2:5+position*2]
            old_value = -1
            if valueKey in self._values:
                old_value = self._values[valueKey]
            point = self._loaded_model.setpoints[valueKey]
            signed = self.get_point_signed(point)
            self._values[valueKey] = self.parse_from_modbus_value(point=point, value=int.from_bytes(payload_slice, 'big', signed=signed))
            if old_value != self._values[valueKey]:
                if valueKey in self._update_handlers:
                    for method in self._update_handlers[valueKey]:
                        method(old_value, self._values[valueKey])

    def parseToModbusValue(self, point:NilanProxyDatapoint|NilanProxySetpoint, value: float|int) -> int:
        divider = self.get_point_divider(point)
        offset = self.get_point_offset(point)
        modifier = self.get_point_write_modifier(point)
        new_value:float|int = value
        if modifier is not None: new_value = modifier(new_value)
        if divider > 1: new_value *= divider
        if offset != 0: new_value -= offset 
        return int(new_value) #cast to int, modbus writes only accept an int

    def parse_from_modbus_value(self, point:NilanProxyDatapoint|NilanProxySetpoint, value: int) -> float|int:
        divider = self.get_point_divider(point)
        offset = self.get_point_offset(point)
        modifier = self.get_point_read_modifier(point)
        new_value:float|int = value
        if offset != 0: new_value += offset 
        if divider > 1: new_value /= divider
        if modifier is not None: new_value = modifier(new_value)
        return new_value

    def get_point_divider(self, point:NilanProxyDatapoint|NilanProxySetpoint) -> int: 
        return 1 if 'divider' not in point else point['divider']
    def get_point_offset(self, point:NilanProxyDatapoint|NilanProxySetpoint) -> int: 
        return 0 if 'offset' not in point else point['offset']
    def get_point_read_address(self, point:NilanProxyDatapoint) -> int: 
        return point['read_address']
    def get_point_read_obj(self, point:NilanProxyDatapoint|NilanProxySetpoint) -> int: 
        return 0 if 'read_obj' not in point else point['read_obj']
    def get_point_write_address(self, point:NilanProxySetpoint) -> int: 
        return point['write_address']
    def get_point_write_obj(self, point:NilanProxySetpoint) -> int: 
        return 0 if 'write_obj' not in point else point['write_obj']
    def get_point_signed(self, point:NilanProxyDatapoint|NilanProxySetpoint) -> bool: 
        return point['signed']
    def get_point_step(self, point:NilanProxySetpoint) -> int: 
        return 1 if 'step' not in point else point['step']
    def get_point_max(self, point:NilanProxySetpoint) -> int: 
        return point['max']
    def get_point_min(self, point:NilanProxySetpoint) -> int: 
        return point['min']
    def get_point_read_modifier(self, point:NilanProxyDatapoint|NilanProxySetpoint) -> Callable[[float|int], float|int]|None: 
        return None if 'read_modifier' not in point else point['read_modifier']
    def get_point_write_modifier(self, point:NilanProxyDatapoint|NilanProxySetpoint) -> Callable[[float|int], float|int]|None: 
        return None if 'write_modifier' not in point else point['write_modifier']