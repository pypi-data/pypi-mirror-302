from .basemodel import ( NilanProxyBaseModel, NilanProxyDatapointKey, NilanProxyDatapoint, NilanProxySetpointKey, NilanProxySetpoint )

class NilanProxyCTS602(NilanProxyBaseModel):
    def __init__(self, device_number:int, slave_device_number:int, slave_device_model:int):
        super().__init__()

        self._attr_manufacturer="Nilan"
        self._attr_model_name="CTS 602"

        self.datapoints = {
            NilanProxyDatapointKey.BYPASS_ACTIVE: NilanProxyDatapoint(read_address=187, divider=1, signed=False),
            NilanProxyDatapointKey.CO2_LEVEL: NilanProxyDatapoint(read_address=53, divider=1, signed=False),
            NilanProxyDatapointKey.FAN_LEVEL_EXTRACT: NilanProxyDatapoint(read_address=100, divider=1, signed=False),
            NilanProxyDatapointKey.FAN_LEVEL_SUPPLY: NilanProxyDatapoint(read_address=99, divider=1, signed=False),
            NilanProxyDatapointKey.FILTER_REPLACE_TIME_REMAIN: NilanProxyDatapoint(read_address=102, divider=1, signed=False),
            NilanProxyDatapointKey.HUMIDITY: NilanProxyDatapoint(read_address=52, divider=100, signed=False),
            NilanProxyDatapointKey.STATE_CODE: NilanProxyDatapoint(read_address=86, divider=1, signed=False),
            NilanProxyDatapointKey.TEMP_CONDENSER: NilanProxyDatapoint(read_address=36, divider=100, signed=True),
            NilanProxyDatapointKey.TEMP_EVAPORATOR: NilanProxyDatapoint(read_address=37, divider=100, signed=True),
            NilanProxyDatapointKey.TEMP_EXTRACT: NilanProxyDatapoint(read_address=35, divider=100, signed=True),
            NilanProxyDatapointKey.TEMP_OUTSIDE: NilanProxyDatapoint(read_address=39, divider=100, signed=True),
            NilanProxyDatapointKey.TEMP_ROOM: NilanProxyDatapoint(read_address=41, divider=100, signed=True),
            NilanProxyDatapointKey.TEMP_SUPPLY: NilanProxyDatapoint(read_address=38, divider=100, signed=True),
        }

        self.setpoints = {
            NilanProxySetpointKey.FAN_LEVEL: NilanProxySetpoint(read_address=139, write_address=139, divider=1, min=0, max=4, signed=False),
            NilanProxySetpointKey.FILTER_REPLACE_INTERVAL: NilanProxySetpoint(read_address=159, write_address=159, divider=1, min=0, max=365, signed=False),
            NilanProxySetpointKey.FILTER_REPLACE_RESET: NilanProxySetpoint(read_address=71, write_address=71, divider=1, min=0, max=1, signed=False),
            NilanProxySetpointKey.TEMP_TARGET: NilanProxySetpoint(read_address=140, write_address=140, divider=100, min=0, max=3000, step=5, signed=True),
        }
        
        #device quirks
        if self.device_has_quirk("hotwaterTempSensor", slave_device_model):
            self.datapoints[NilanProxyDatapointKey.TEMP_HOTWATER_TOP] = NilanProxyDatapoint(read_address=42, divider=100, signed=True)
            self.datapoints[NilanProxyDatapointKey.TEMP_HOTWATER_BOTTOM] = NilanProxyDatapoint(read_address=43, divider=100, signed=True)

        if self.device_has_quirk("sacrificialAnode", slave_device_model):  
            self.datapoints[NilanProxyDatapointKey.SACRIFICIAL_ANODE_OK] = NilanProxyDatapoint(read_address=142, divider=1, signed=False)
            
        if self.device_has_quirk("reheat", slave_device_model):  
            self.setpoints[NilanProxySetpointKey.REHEAT_ENABLE] = NilanProxySetpoint(read_address=281, write_address=281, divider=1, min=0, max=1, signed=False)

        if self.device_has_quirk("exhaustTempSensor", slave_device_model):  
            self.datapoints[NilanProxyDatapointKey.TEMP_EXHAUST] = NilanProxyDatapoint(read_address=34, divider=100, signed=True)

        if self.device_has_quirk("antiLegionella", slave_device_model):  
            self.setpoints[NilanProxySetpointKey.ANTILEGIONELLA_DAY] = NilanProxySetpoint(read_address=194, write_address=194, divider=1, min=0, max=7, signed=False)

        if self.device_has_quirk("hotwaterTempSet", slave_device_model):  
            self.setpoints[NilanProxySetpointKey.TEMP_HOTWATER] = NilanProxySetpoint(read_address=190, write_address=190, divider=100, min=2000, max=7000, step=10, signed=True)
            self.setpoints[NilanProxySetpointKey.TEMP_HOTWATER_BOOST] = NilanProxySetpoint(read_address=189, write_address=189, divider=100, min=2000, max=7000, step=10, signed=True)

        if self.device_has_quirk("summerTemperatures", slave_device_model):
            self.setpoints[NilanProxySetpointKey.TEMP_SUMMER_SUPPLY_MIN] = NilanProxySetpoint(read_address=171, write_address=171, divider=100, min=0, max=4000, step=10, signed=True)
            self.setpoints[NilanProxySetpointKey.TEMP_SUMMER_SUPPLY_MAX] = NilanProxySetpoint(read_address=173, write_address=173, divider=100, min=0, max=4000, step=10, signed=True)

        if self.device_has_quirk("coolingPriority", slave_device_model):
            self.setpoints[NilanProxySetpointKey.COMPRESSOR_PRIORITY] = NilanProxySetpoint(read_address=191, write_address=191, divider=1, min=0, max=1, signed=False)

        if self.device_has_quirk("coolingOffset", slave_device_model):
            self.setpoints[NilanProxySetpointKey.TEMP_COOLING_START_OFFSET] = NilanProxySetpoint(read_address=170, write_address=170, divider=1, min=0, max=8, signed=True)
        
        self.set_default_configs()

        #place config modifiers here

        
        self._quirks = {
            "hotwaterTempSensor": [
                9, 10, 11,  12,  18, 19,
                20, 21, 23,  30,  32, 34,
                38, 43, 44, 144, 244
            ],
            "sacrificialAnode": [
                9, 10,  11,  12, 18, 19,
                20, 21,  23,  30, 34, 38,
                43, 44, 144, 244
            ],
            "reheat": [
                2,   3,   4,  9, 10, 11, 12, 13, 18,
                19,  20,  21, 23, 26, 27, 30, 31, 33,
                34,  35,  36, 38, 39, 40, 41, 43, 44,
                45, 144, 244
            ],
            "exhaustTempSensor": [ 2, 13, 27, 31 ],
            "antiLegionella": [
                3,  4,  9, 10,  11,  12, 18,
                19, 20, 21, 23,  30,  32, 34,
                38, 43, 44, 45, 144, 244
            ],
            "hotwaterTempSet": [
                9, 10, 11,  12,  13, 18, 19,
                20, 21, 23,  30,  31, 32, 34,
                38, 43, 44, 144, 244
            ],
            "summerTemperatures": [
                2,  4,  9, 10, 12, 13, 19,  21,
                26, 30, 31, 32, 33, 34, 35,  36,
                38, 39, 40, 41, 43, 44, 45, 144,
                244
            ],
            "coolingPriority": [
                2,  9, 10, 12, 13,  30,
                31, 32, 38, 43, 44, 144,
                244
            ],
            "coolingOffset": [
                4,  9, 10, 12, 19,  21,  26,
                30, 32, 33, 35, 36,  38,  39,
                40, 41, 43, 44, 45, 144, 244
            ]
        }
        
        
    def device_has_quirk(self, quirk:str, device:int) -> bool:
        if quirk not in self._quirks: return False
        return device in self._quirks[quirk]