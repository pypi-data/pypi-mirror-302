from .basemodel import ( NilanProxyBaseModel, NilanProxyDatapointKey, NilanProxyDatapoint, NilanProxySetpointKey, NilanProxySetpoint, NilanProxyUnits )

class NilanProxyOptima314(NilanProxyBaseModel):
    def __init__(self, device_number:int, slave_device_number:int, slave_device_model:int):
        super().__init__()

        self._attr_manufacturer="Genvex"
        self._attr_model_name="Optima 314"

        self.datapoints = {
            NilanProxyDatapointKey.BYPASS_ACTIVE: NilanProxyDatapoint(read_address=12, divider=1, signed=False),
            NilanProxyDatapointKey.FAN_DUTYCYCLE_EXTRACT: NilanProxyDatapoint(read_address=19, divider=100, signed=False),
            NilanProxyDatapointKey.FAN_DUTYCYCLE_SUPPLY: NilanProxyDatapoint(read_address=18, divider=100, signed=False),
            NilanProxyDatapointKey.FAN_RPM_EXTRACT: NilanProxyDatapoint(read_address=36, divider=1, signed=False),
            NilanProxyDatapointKey.FAN_RPM_SUPPLY: NilanProxyDatapoint(read_address=35, divider=1, signed=False),
            NilanProxyDatapointKey.HUMIDITY: NilanProxyDatapoint(read_address=26, divider=1, signed=False),
            NilanProxyDatapointKey.TEMP_EXHAUST: NilanProxyDatapoint(read_address=22, divider=10, offset=-300, signed=True),
            NilanProxyDatapointKey.TEMP_EXTRACT: NilanProxyDatapoint(read_address=64, divider=10, offset=-300, signed=True),
            NilanProxyDatapointKey.TEMP_OUTSIDE: NilanProxyDatapoint(read_address=21, divider=10, offset=-300, signed=True),
            NilanProxyDatapointKey.TEMP_SUPPLY: NilanProxyDatapoint(read_address=20, divider=10, offset=-300, signed=True),
        }

        self.setpoints = {
            NilanProxySetpointKey.BOOST_ENABLE: NilanProxySetpoint(read_address=30, write_address=70, divider=1, min=0, max=1, signed=False),
            NilanProxySetpointKey.BOOST_TIME: NilanProxySetpoint(read_address=70, write_address=150, divider=1, min=1, max=120, signed=False),
            NilanProxySetpointKey.FAN_LEVEL: NilanProxySetpoint(read_address=7, write_address=24, divider=1, min=0, max=4, signed=False),
            NilanProxySetpointKey.FAN_LEVEL1_EXTRACT_PRESET: NilanProxySetpoint(read_address=13, write_address=36, divider=1, min=0, max=100, signed=False),
            NilanProxySetpointKey.FAN_LEVEL1_SUPPLY_PRESET: NilanProxySetpoint(read_address=10, write_address=30, divider=1, min=0, max=100, signed=False),
            NilanProxySetpointKey.FAN_LEVEL2_EXTRACT_PRESET: NilanProxySetpoint(read_address=14, write_address=38, divider=1, min=0, max=100, signed=False),
            NilanProxySetpointKey.FAN_LEVEL2_SUPPLY_PRESET: NilanProxySetpoint(read_address=11, write_address=32, divider=1, min=0, max=100, signed=False),
            NilanProxySetpointKey.FAN_LEVEL3_EXTRACT_PRESET: NilanProxySetpoint(read_address=15, write_address=40, divider=1, min=0, max=100, signed=False),
            NilanProxySetpointKey.FAN_LEVEL3_SUPPLY_PRESET: NilanProxySetpoint(read_address=12, write_address=34, divider=1, min=0, max=100, signed=False),
            NilanProxySetpointKey.FAN_LEVEL4_EXTRACT_PRESET: NilanProxySetpoint(read_address=9, write_address=28, divider=1, min=0, max=100, signed=False),
            NilanProxySetpointKey.FAN_LEVEL4_SUPPLY_PRESET: NilanProxySetpoint(read_address=8, write_address=26, divider=1, min=0, max=100, signed=False),
            NilanProxySetpointKey.FILTER_REPLACE_INTERVAL: NilanProxySetpoint(read_address=100, write_address=210, divider=1, min=0, max=12, signed=False),
            NilanProxySetpointKey.FILTER_REPLACE_RESET: NilanProxySetpoint(read_address=50, write_address=110, divider=1, min=0, max=1, signed=False),
            NilanProxySetpointKey.HUMIDITY_CONTROL_ENABLE: NilanProxySetpoint(read_address=6, write_address=22, divider=1, min=0, max=1, signed=False),
            NilanProxySetpointKey.REHEAT_ENABLE: NilanProxySetpoint(read_address=3, write_address=16, divider=1, min=0, max=1, signed=False),
            NilanProxySetpointKey.TEMP_HOTWATER: NilanProxySetpoint(read_address=122, write_address=254, divider=10, min=0, max=550, signed=True),
            NilanProxySetpointKey.TEMP_TARGET: NilanProxySetpoint(read_address=1, write_address=12, divider=10, offset=100, min=0, max=200, step=5, signed=True),
        }
        
        self.set_default_configs()
        
        #place config modifiers here
        self._configs[NilanProxySetpointKey.FILTER_REPLACE_INTERVAL]["unit_of_measurement"] = NilanProxyUnits.MONTHS