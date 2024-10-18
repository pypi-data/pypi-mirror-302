from .basemodel import ( NilanProxyBaseModel, NilanProxyDatapointKey, NilanProxyDatapoint, NilanProxySetpointKey, NilanProxySetpoint, NilanProxyUnits )

class NilanProxyOptima301(NilanProxyBaseModel):
    def __init__(self, device_number:int, slave_device_number:int, slave_device_model:int):
        super().__init__()

        self._attr_manufacturer="Genvex"
        self._attr_model_name="Optima 301"

        self.datapoints = {
            NilanProxyDatapointKey.BYPASS_ACTIVE: NilanProxyDatapoint(read_address=104, divider=1, signed=False),
            NilanProxyDatapointKey.FAN_DUTYCYCLE_EXTRACT: NilanProxyDatapoint(read_address=103, divider=1, signed=False),
            NilanProxyDatapointKey.FAN_DUTYCYCLE_SUPPLY: NilanProxyDatapoint(read_address=102, divider=1, signed=False),
            NilanProxyDatapointKey.FAN_RPM_EXTRACT: NilanProxyDatapoint(read_address=109, divider=1, signed=False),
            NilanProxyDatapointKey.FAN_RPM_SUPPLY: NilanProxyDatapoint(read_address=108, divider=1, signed=False),
            NilanProxyDatapointKey.HUMIDITY: NilanProxyDatapoint(read_address=10, divider=1, signed=False),
            NilanProxyDatapointKey.TEMP_EXHAUST: NilanProxyDatapoint(read_address=3, divider=10, offset=-300, signed=True), #T4
            NilanProxyDatapointKey.TEMP_EXTRACT: NilanProxyDatapoint(read_address=6, divider=10, offset=-300, signed=True), #T7
            NilanProxyDatapointKey.TEMP_OUTSIDE: NilanProxyDatapoint(read_address=2, divider=10, offset=-300, signed=True), #T3
            NilanProxyDatapointKey.TEMP_SUPPLY: NilanProxyDatapoint(read_address=0, divider=10, offset=-300, signed=True), #T1
        }

        self.setpoints = {
            NilanProxySetpointKey.COOLING_ENABLE: NilanProxySetpoint(read_address=2, write_address=2, divider=1, min=0, max=1, signed=False),
            NilanProxySetpointKey.FAN_LEVEL: NilanProxySetpoint(read_address=100, write_address=100, divider=1, min=0, max=4, signed=False),
            NilanProxySetpointKey.FAN_LEVEL1_EXTRACT_PRESET: NilanProxySetpoint(read_address=9, write_address=9, divider=1, min=0, max=100, signed=False),
            NilanProxySetpointKey.FAN_LEVEL1_SUPPLY_PRESET: NilanProxySetpoint(read_address=6, write_address=6, divider=1, min=0, max=100, signed=False),
            NilanProxySetpointKey.FAN_LEVEL2_EXTRACT_PRESET: NilanProxySetpoint(read_address=10, write_address=10, divider=1, min=0, max=100, signed=False),
            NilanProxySetpointKey.FAN_LEVEL2_SUPPLY_PRESET: NilanProxySetpoint(read_address=7, write_address=7, divider=1, min=0, max=100, signed=False),
            NilanProxySetpointKey.FAN_LEVEL3_EXTRACT_PRESET: NilanProxySetpoint(read_address=11, write_address=11, divider=1, min=0, max=100, signed=False),
            NilanProxySetpointKey.FAN_LEVEL3_SUPPLY_PRESET: NilanProxySetpoint(read_address=8, write_address=8, divider=1, min=0, max=100, signed=False),
            NilanProxySetpointKey.FILTER_REPLACE_RESET: NilanProxySetpoint(read_address=105, write_address=105, divider=1, min=0, max=1, signed=False),
            NilanProxySetpointKey.PREHEAT_ENABLE: NilanProxySetpoint(read_address=20, write_address=20, divider=1, min=0, max=1, signed=False),         
            NilanProxySetpointKey.TEMP_COOLING_START_OFFSET: NilanProxySetpoint(read_address=1, write_address=1, divider=10, min=30, max=100, signed=True),
            NilanProxySetpointKey.TEMP_TARGET: NilanProxySetpoint(read_address=0, write_address=0, divider=10, offset=100, min=0, max=200, step=5, signed=True),         
        }
       
        self.set_default_configs()
        
        #place config modifiers here
        self._configs[NilanProxySetpointKey.FILTER_REPLACE_INTERVAL]["unit_of_measurement"] = NilanProxyUnits.MONTHS