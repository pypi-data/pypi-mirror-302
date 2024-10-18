from .basemodel import ( NilanProxyBaseModel, NilanProxyDatapointKey, NilanProxyDatapoint, NilanProxySetpointKey, NilanProxySetpoint )

class NilanProxyCTS602Light(NilanProxyBaseModel):
    def __init__(self, device_number:int, slave_device_number:int, slave_device_model:int):
        super().__init__()

        self._attr_manufacturer="Nilan"
        self._attr_model_name="CTS 602 light"


        self.datapoints = {
            NilanProxyDatapointKey.BYPASS_ACTIVE: NilanProxyDatapoint(read_address=129, divider=1, signed=False),
            NilanProxyDatapointKey.FAN_DUTYCYCLE_EXTRACT: NilanProxyDatapoint(read_address=99, divider=1, signed=False),
            NilanProxyDatapointKey.FAN_DUTYCYCLE_SUPPLY: NilanProxyDatapoint(read_address=98, divider=1, signed=False),
            NilanProxyDatapointKey.FILTER_REPLACE_TIME_REMAIN: NilanProxyDatapoint(read_address=101, divider=1, signed=False),
            NilanProxyDatapointKey.HUMIDITY: NilanProxyDatapoint(read_address=51, divider=100, signed=False),
            NilanProxyDatapointKey.TEMP_EXHAUST: NilanProxyDatapoint(read_address=33, divider=100, signed=True),
            NilanProxyDatapointKey.TEMP_EXTRACT: NilanProxyDatapoint(read_address=34, divider=100, signed=True),
            NilanProxyDatapointKey.TEMP_OUTSIDE: NilanProxyDatapoint(read_address=38, divider=100, signed=True),
            NilanProxyDatapointKey.TEMP_SUPPLY: NilanProxyDatapoint(read_address=37, divider=100, signed=True),
        }

        self.setpoints = {
            NilanProxySetpointKey.FAN_LEVEL: NilanProxySetpoint(read_address=135, write_address=135, divider=1, min=0, max=4, signed=False),
            NilanProxySetpointKey.FILTER_REPLACE_INTERVAL: NilanProxySetpoint(read_address=153, write_address=153, divider=1, min=0, max=365, signed=False),
            NilanProxySetpointKey.FILTER_REPLACE_RESET: NilanProxySetpoint(read_address=67, write_address=67, divider=1, min=0, max=1, signed=False),            
            NilanProxySetpointKey.TEMP_TARGET: NilanProxySetpoint(read_address=136, write_address=136, divider=100, min=0, max=3000, step=5, signed=True),
        }

        self.set_default_configs()
        
        #place config modifiers here