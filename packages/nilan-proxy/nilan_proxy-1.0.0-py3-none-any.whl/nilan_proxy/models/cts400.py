from .basemodel import ( NilanProxyBaseModel, NilanProxyDatapointKey, NilanProxyDatapoint, NilanProxySetpointKey, NilanProxySetpoint )


class NilanProxyCTS400(NilanProxyBaseModel):
    def __init__(self, device_number:int, slave_device_number:int, slave_device_model:int):
        super().__init__()

        self._attr_manufacturer="Nilan"
        self._attr_model_name="CTS 400"

        self.datapoints = {
            NilanProxyDatapointKey.BYPASS_ACTIVE: NilanProxyDatapoint(read_address=23, divider=1, signed=False),
            NilanProxyDatapointKey.FAN_DUTYCYCLE_EXTRACT: NilanProxyDatapoint(read_address=24, divider=10, signed=False),
            NilanProxyDatapointKey.FAN_DUTYCYCLE_SUPPLY: NilanProxyDatapoint(read_address=25, divider=10, signed=False),
            NilanProxyDatapointKey.TEMP_OUTSIDE: NilanProxyDatapoint(read_address=27, divider=10, signed=True),
            NilanProxyDatapointKey.TEMP_SUPPLY: NilanProxyDatapoint(read_address=28, divider=10, signed=True),
            NilanProxyDatapointKey.TEMP_EXTRACT: NilanProxyDatapoint(read_address=29, divider=10, signed=True),
            NilanProxyDatapointKey.TEMP_EXHAUST: NilanProxyDatapoint(read_address=30, divider=10, signed=True),
            NilanProxyDatapointKey.HUMIDITY: NilanProxyDatapoint(read_address=31, divider=10, signed=False),
            NilanProxyDatapointKey.HUMIDITY_AVG: NilanProxyDatapoint(read_address=46, divider=10, signed=False),
            NilanProxyDatapointKey.CO2_LEVEL: NilanProxyDatapoint(read_address=47, divider=1, signed=False),
            NilanProxyDatapointKey.VOC_LEVEL: NilanProxyDatapoint(read_address=48, divider=1, signed=False),
            NilanProxyDatapointKey.FILTER_OK: NilanProxyDatapoint(read_address=49, divider=1, signed=False, read_modifier = self.modifier_flip_bool),
            NilanProxyDatapointKey.ALARM_STATUS: NilanProxyDatapoint(read_address=50, divider=1, signed=False),
            NilanProxyDatapointKey.ALARM_1_CODE: NilanProxyDatapoint(read_address=51, divider=1, signed=False),
            NilanProxyDatapointKey.ALARM_2_CODE: NilanProxyDatapoint(read_address=52, divider=1, signed=False),
            NilanProxyDatapointKey.ALARM_3_CODE: NilanProxyDatapoint(read_address=53, divider=1, signed=False),     
            NilanProxyDatapointKey.ALARM_1_INFO: NilanProxyDatapoint(read_address=56, divider=1, signed=False),
            NilanProxyDatapointKey.ALARM_2_INFO: NilanProxyDatapoint(read_address=57, divider=1, signed=False),
            NilanProxyDatapointKey.ALARM_3_INFO: NilanProxyDatapoint(read_address=58, divider=1, signed=False),             
            NilanProxyDatapointKey.FAN_LEVEL_CURRENT: NilanProxyDatapoint(read_address=63, divider=1, signed=False),             
            NilanProxyDatapointKey.HUMIDITY_HIGH_ACTIVE: NilanProxyDatapoint(read_address=64, divider=1, signed=False, read_modifier = self.modifier_flip_bool),
            NilanProxyDatapointKey.HUMIDITY_HIGH_LEVEL: NilanProxyDatapoint(read_address=66, divider=10, signed=False),             
            NilanProxyDatapointKey.HUMIDITY_HIGH_LEVEL_TIME: NilanProxyDatapoint(read_address=70, divider=1, signed=False, read_modifier = self.modifier_seconds_to_minutes),
            NilanProxyDatapointKey.WINTER_MODE_ACTIVE: NilanProxyDatapoint(read_address=72, divider=1, signed=False),
            NilanProxyDatapointKey.FILTER_REPLACE_TIME_AGO: NilanProxyDatapoint(read_address=77, divider=1, signed=False, read_modifier = self.modifier_hours_to_days),
            NilanProxyDatapointKey.DEFROST_ACTIVE: NilanProxyDatapoint(read_address=91, divider=1, signed=False),
            NilanProxyDatapointKey.FILTER_REPLACE_TIME_REMAIN: NilanProxyDatapoint(read_address=110, divider=1, signed=False),
        }

        self.setpoints = {
            NilanProxySetpointKey.ALARM_RESET: NilanProxySetpoint(read_address=30, write_address=30, divider=1, min=0, max=1, signed=False),
            NilanProxySetpointKey.HUMIDITY_LOW_THRESHOLD: NilanProxySetpoint(read_address=31, write_address=31, divider=10, min=150, max=450, step=5, signed=False),
            NilanProxySetpointKey.FAN_LEVEL_LOW_HUMIDITY: NilanProxySetpoint(read_address=32, write_address=32, divider=1, min=0, max=3, signed=False),
            NilanProxySetpointKey.FAN_LEVEL_HIGH_HUMIDITY: NilanProxySetpoint(read_address=33, write_address=33, divider=1, min=2, max=4, signed=False),
            NilanProxySetpointKey.FAN_LEVEL_HIGH_HUMIDITY_TIME: NilanProxySetpoint(read_address=34, write_address=34, divider=1, min=0, max=180, signed=False),
            NilanProxySetpointKey.CO2_THRESHOLD: NilanProxySetpoint(read_address=35, write_address=35, divider=1, min=500, max=2000, signed=False),
            NilanProxySetpointKey.VOC_THRESHOLD: NilanProxySetpoint(read_address=36, write_address=36, divider=1, min=500, max=2000, signed=False),
            NilanProxySetpointKey.TEMP_TARGET: NilanProxySetpoint(read_address=37, write_address=37, divider=10, min=100, max=300, step=5, signed=True),
            NilanProxySetpointKey.TEMP_REGULATION_DEAD_BAND: NilanProxySetpoint(read_address=38, write_address=38, divider=10, min=0, max=40, step=5, signed=True),
            NilanProxySetpointKey.TEMP_DEFROST_LOW_THRESHOLD: NilanProxySetpoint(read_address=39, write_address=39, divider=10, min=10, max=50, step=5, signed=True),
            NilanProxySetpointKey.TEMP_DEFROST_HIGH_THRESHOLD: NilanProxySetpoint(read_address=40, write_address=40, divider=10, min=50, max=100, step=5, signed=True),
            NilanProxySetpointKey.DEFROST_MAX_TIME: NilanProxySetpoint(read_address=41, write_address=41, divider=1, min=5, max=60, signed=False),
            NilanProxySetpointKey.DEFROST_BREAK_TIME: NilanProxySetpoint(read_address=43, write_address=43, divider=1, min=15, max=760, signed=False),
            NilanProxySetpointKey.TEMP_WINTER_MODE_THRESHOLD: NilanProxySetpoint(read_address=45, write_address=45, divider=10, min=50, max=200, step=5, signed=True),
            NilanProxySetpointKey.FILTER_REPLACE_INTERVAL: NilanProxySetpoint(read_address=50, write_address=50, divider=1, min=0, max=360, signed=False),
            NilanProxySetpointKey.FILTER_REPLACE_RESET: NilanProxySetpoint(read_address=51, write_address=51, divider=1, min=0, max=1, signed=False),
            NilanProxySetpointKey.TEMP_SUPPLY_MIN: NilanProxySetpoint(read_address=57, write_address=57, divider=10, min=100, max=200, step=5, signed=True),
            NilanProxySetpointKey.TEMP_SUPPLY_MAX: NilanProxySetpoint(read_address=58, write_address=58, divider=10, min=100, max=500, step=5, signed=True),
            NilanProxySetpointKey.FAN_LEVEL1_SUPPLY_PRESET: NilanProxySetpoint(read_address=59, write_address=59, divider=10, min=200, max=1000, signed=False),
            NilanProxySetpointKey.FAN_LEVEL2_SUPPLY_PRESET: NilanProxySetpoint(read_address=60, write_address=60, divider=10, min=200, max=1000, signed=False),
            NilanProxySetpointKey.FAN_LEVEL3_SUPPLY_PRESET: NilanProxySetpoint(read_address=61, write_address=61, divider=10, min=200, max=1000, signed=False),
            NilanProxySetpointKey.FAN_LEVEL4_SUPPLY_PRESET: NilanProxySetpoint(read_address=62, write_address=62, divider=10, min=200, max=1000, signed=False),
            NilanProxySetpointKey.FAN_LEVEL1_EXTRACT_PRESET: NilanProxySetpoint(read_address=63, write_address=63, divider=10, min=200, max=1000, signed=False),
            NilanProxySetpointKey.FAN_LEVEL2_EXTRACT_PRESET: NilanProxySetpoint(read_address=64, write_address=64, divider=10, min=200, max=1000, signed=False),
            NilanProxySetpointKey.FAN_LEVEL3_EXTRACT_PRESET: NilanProxySetpoint(read_address=65, write_address=65, divider=10, min=200, max=1000, signed=False),
            NilanProxySetpointKey.FAN_LEVEL4_EXTRACT_PRESET: NilanProxySetpoint(read_address=66, write_address=66, divider=10, min=200, max=1000, signed=False),
            NilanProxySetpointKey.FAN_LEVEL: NilanProxySetpoint(read_address=69, write_address=69, divider=1, min=1, max=4, signed=False),
            NilanProxySetpointKey.ENABLE: NilanProxySetpoint(read_address=70, write_address=70, divider=1, min=0, max=1, signed=False),
            NilanProxySetpointKey.FAN_LEVEL_HIGH_CO2: NilanProxySetpoint(read_address=80, write_address=80, divider=1, min=2, max=4, signed=False),
        }

        self.set_default_configs()
        
        #place config modifiers here