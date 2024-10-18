from collections.abc import Callable
from enum import Enum
from typing import Dict, List, TypedDict, NotRequired


class NilanProxyDatapointKey(Enum):
    ALARM_1_CODE = "alarm_1_code"
    ALARM_1_INFO = "alarm_1_info"
    ALARM_2_CODE = "alarm_2_code"
    ALARM_2_INFO = "alarm_2_info"
    ALARM_3_CODE = "alarm_3_code"
    ALARM_3_INFO = "alarm_3_info"
    ALARM_STATUS = "alarm_status"
    """Indicates if an alarm is active"""
    ALARM_BITS = "alarm_bits"
    BYPASS_ACTIVE = "bypass_active"
    CO2_LEVEL = "co2_level"
    DEFROST_ACTIVE = "defrost_active"
    DEFROST_TIME_AGO = "defrost_time_ago"
    """
    (default=days)
    """
    FAN_DUTYCYCLE_EXTRACT = "fan_dutycycle_extract"
    FAN_DUTYCYCLE_SUPPLY = "fan_dutycycle_supply"
    FAN_LEVEL_CURRENT = "fan_level_current" 
    """The fan level currently active"""
    FAN_LEVEL_EXTRACT = "fan_level_extract"
    FAN_LEVEL_SUPPLY = "fan_level_supply"
    FAN_RPM_EXTRACT = "fan_rpm_extract"
    FAN_RPM_SUPPLY = "fan_rpm_supply"
    FILTER_REPLACE_TIME_AGO = "filter_replace_time_ago"
    """
    (default=days)
    """
    FILTER_REPLACE_TIME_REMAIN = "filter_replace_time_remain"
    """
    (default=days)
    """
    FILTER_OK = "filter_ok"
    HUMIDITY = "humidity"
    HUMIDITY_AVG = "humidity_average"
    HUMIDITY_HIGH_ACTIVE = "humidity_high_active"
    HUMIDITY_HIGH_LEVEL = "humidity_high_level"
    HUMIDITY_HIGH_LEVEL_TIME = "humidity_high_level_time"
    """Time the high humidity functionality has been active"""
    SACRIFICIAL_ANODE_OK = "sacrificial_anode_ok"
    STATE_CODE = "state_code"
    TEMP_CONDENSER = "temp_condenser"
    TEMP_EVAPORATOR = "temp_evaporator"
    TEMP_EXHAUST = "temp_exhaust"
    TEMP_EXTRACT = "temp_extract"
    TEMP_HOTWATER_BOTTOM = "temp_hotwater_bottom"
    TEMP_HOTWATER_TOP = "temp_hotwater_top"
    TEMP_OUTSIDE = "temp_outside"
    TEMP_ROOM = "temp_room"
    TEMP_SUPPLY = "temp_supply"
    VOC_LEVEL = "voc_level"
    WINTER_MODE_ACTIVE = "winter_mode_active"
    
    UNKNOWN_VALUE_1 = "unknown_value_1"


class NilanProxySetpointKey(Enum):
    """
    Setpoints that can be read/written.

    If a key has double underscore '__' followed by a number, it contains preset values that can be different from the read value.
    """
    ALARM_RESET = "alarm_reset"

    ANTILEGIONELLA_DAY = "antilegionella_day"
    """
    Day of the week the legionella treatment is performed.
    
    Typically this is used when a hot water tank is installed.
    
    Values:
    - 0: "OFF",
    - 1: "+0",
    - 2: "+1",
    - 3: "+2",
    - 4: "+3",
    - 5: "+4",
    - 6: "+5",
    - 7: "+7",
    - 8: "+10"
    """
    BOOST_ENABLE = "boost_enable"
    """Enable the boost function for the unit."""
    BOOST_TIME = "boost_time"
    """Time the boost function will run when triggered. (default=minutes)."""
    CO2_THRESHOLD = "co2_threshold"
    COOLING_ENABLE = "cooling_enable"
    """Enable the cooling function for the unit.
    
    Typically this will be active cooling, bypass has its own key.
    """
    COMPRESSOR_PRIORITY = "compressor_priority"
    """Priority for the compressor.
    """
    DEFROST_BREAK_TIME = "defrost_break_time"
    DEFROST_MAX_TIME = "defrost_max_time"
    ENABLE = "enable"
    """Enable the unit."""
    FAN_LEVEL = "fan_level"
    """Select the fan level.
    Typically this activates a preset configuration.
    """
    FAN_LEVEL_LOW_HUMIDITY = "fan_level_low_humidity"
    FAN_LEVEL_HIGH_CO2 = "fan_level_high_co2"
    FAN_LEVEL_HIGH_HUMIDITY = "fan_level_high_humidity"
    FAN_LEVEL_HIGH_HUMIDITY_TIME = "fan_level_high_humidity_time"
    FAN_LEVEL1_EXTRACT_PRESET = "fan_level1_extract_preset"
    FAN_LEVEL1_SUPPLY_PRESET = "fan_level1_supply_preset"
    FAN_LEVEL2_EXTRACT_PRESET = "fan_level2_extract_preset"
    FAN_LEVEL2_SUPPLY_PRESET = "fan_level2_supply_preset"
    FAN_LEVEL3_EXTRACT_PRESET = "fan_level3_extract_preset"
    FAN_LEVEL3_SUPPLY_PRESET = "fan_level3_supply_preset"
    FAN_LEVEL4_EXTRACT_PRESET = "fan_level4_extract_preset"
    FAN_LEVEL4_SUPPLY_PRESET = "fan_level4_supply_preset"
    FILTER_REPLACE_INTERVAL = "filter_replace_interval"
    """Time interval between filter replacements/maintenance (default=days)"""
    FILTER_REPLACE_RESET = "filter_replace_reset"
    """Resets/restarts the timer for filter replacements/maintenance."""
    HUMIDITY_CONTROL_ENABLE = "humidity_control_enable"
    """Enable the humidity function for the unit.
    
    Typically this will be extra fan level when showering or alike.
    """
    HUMIDITY_LOW_THRESHOLD = "humidity_low_threshold"
    PREHEAT_ENABLE = "preheat_enable"
    """Enable the preheat function for the unit.
    
    Typically this will be a heating element for the outside air.
    """
    PREHEAT_CYCLE_TIME = "preheat_cycle_time"
    PREHEAT_PID_P = "preheat_pid_p"
    PREHEAT_PID_I = "preheat_pid_i"
    PREHEAT_PID_D = "preheat_pid_d"
    REHEAT_ENABLE = "reheat_enable"
    """Enable the prehet function for the unit.
    
    Typically this will be a heating element for the extract air.
    """
    REHEAT_CYCLE_TIME = "reheat_cycle_time"
    REHEAT_PID_P = "reheat_pid_p"
    REHEAT_PID_I = "reheat_pid_i"
    REHEAT_PID_D = "reheat_pid_d"
    TEMP_BYPASS_OPEN_OFFSET = "temp_bypass_open_offset"
    """Temperature offset for when the bypass function.
    
    Typically the bypass function will be a passive function to keep indoor temperature near the target.
    """
    TEMP_COOLING_START_OFFSET = "temp_cooling_start_offset"
    """Temperature increase amount before cooling is started.
    
    Values:
    - 0: "OFF",
    - 1: "+0",
    - 2: "+1",
    - 3: "+2",
    - 4: "+3",
    - 5: "+4",
    - 6: "+5",
    - 7: "+7",
    - 8: "+10"
    """
    TEMP_DEFROST_LOW_THRESHOLD = "temp_defrost_low_threshold"
    """Temperature below this will start defrost function."""
    TEMP_DEFROST_HIGH_THRESHOLD = "temp_defrost_high_threshold"
    """Temperature above this will stop defrost function."""
    TEMP_HOTWATER = "temp_hotwater"
    """Temperature setpoint for the hot water.
    
    Typically this is used when a hot water container is installed.
    
    This is the main heating element.
    """
    TEMP_HOTWATER_BOOST = "temp_hotwater_boost"
    """Temperature boost setpoint for the hot water.
    
    Typically this is used when a hot water container is installed.
    
    This is the auxiliary (boosting) heating element.
    """
    TEMP_REGULATION_DEAD_BAND = "temp_regulation_dead_band"
    """Temperature dead band for regulation to prevent mode switching oscillations."""
    TEMP_REHEAT_OFFSET = "temp_reheat_offset"
    """Temperature offset relative to indoor for the reheating."""
    TEMP_TARGET = "temp_target"
    """Temperature setpoint for the home."""
    TEMP_SUMMER_SUPPLY_MAX = "temp_summer_supply_max"
    """Temperature limit for summer supply air.
    
    Typically this is used when a heater is heating the air.
    """
    TEMP_SUMMER_SUPPLY_MIN = "temp_summer_supply_min"
    """Temperature limit for summer supply air.
    
    Typically this is used when a heater is heating the air.
    """
    TEMP_SUPPLY_MAX = "temp_supply_max"
    TEMP_SUPPLY_MIN = "temp_supply_min"
    TEMP_WINTER_SUPPLY_MAX = "temp_winter_supply_max"
    """Temperature limit for winter supply air.
    
    Typically this is used when a heater is heating the air.
    """
    TEMP_WINTER_SUPPLY_MIN = "temp_winter_supply_min"
    """Temperature limit for winter supply air.
    
    Typically this is used when a heater is heating the air.
    """
    TEMP_WINTER_MODE_THRESHOLD = "temp_winter_mode_threshold"
    """Temperature for switching between summer and winter modes.
    
    - When outside temperature is above, summer mode is active.
    - When outside temperature is below, winter mode is active.
    """
    VOC_THRESHOLD = "voc_threshold"
    
    
class NilanProxyDatapoint(TypedDict):
    divider: NotRequired[int]
    """Applied to the register value in the order: 1: divider, 2: offset, 3: modifier"""
    offset: NotRequired[int]
    """Applied to the register value in the order: 1: divider, 2: offset, 3: modifier"""
    read_address: int
    read_modifier: NotRequired[Callable[[float|int], float|int]]
    """Modifier applied to value after it has been parsed by the system. can be used to alter hours to days etc. or round floating values
    
    Applied to the register value in the order: 1: divider, 2: offset, 3: modifier"""
    read_obj: NotRequired[int]
    """default is 0"""
    signed: bool
    """indication of the data being signed or unsigned"""

class NilanProxySetpoint(NilanProxyDatapoint):
    max: int
    """max value in the register"""
    min: int
    """min value in the register"""
    step: NotRequired[int]
    """step size in register value, if unset will default to the divider"""
    write_address: int
    write_modifier: NotRequired[Callable[[float|int], float|int]]
    """Modifier applied to value before it has been parsed back to register type. can be used to alter hours to days etc. or round floating values"""
    write_obj: NotRequired[int]
    """default is 0"""

class NilanProxyPointConfig(TypedDict):
    unit_of_measurement: str|None
    read: bool

class NilanProxyUnits:
    SECONDS = "seconds"
    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"
    MONTHS = "months"
    YEARS = "years"
    CELSIUS = "celsius"
    BOOL = "bool"
    BITMASK = "bitmask"
    PPM = "ppm"
    """CONCENTRATION PARTS PER MILLION"""
    RPM = "rpm"
    """REVOLUTIONS PER MINUTE"""
    # INT = "int"
    # FLOAT = "float"
    PCT = "percent"
    TEXT = "text"
    UNDEFINED = None
    
DEFAULT_CONFIGS:Dict[NilanProxyDatapointKey|NilanProxySetpointKey, NilanProxyPointConfig] = {
            NilanProxyDatapointKey.ALARM_1_CODE: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.UNDEFINED, read=True),
            NilanProxyDatapointKey.ALARM_1_INFO: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.TEXT, read=True),
            NilanProxyDatapointKey.ALARM_2_CODE:NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.UNDEFINED, read=True),
            NilanProxyDatapointKey.ALARM_2_INFO: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.TEXT, read=True),
            NilanProxyDatapointKey.ALARM_3_CODE:NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.UNDEFINED, read=True),
            NilanProxyDatapointKey.ALARM_3_INFO: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.TEXT, read=True),
            NilanProxyDatapointKey.ALARM_STATUS:NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.BOOL, read=True),
            NilanProxyDatapointKey.ALARM_BITS:NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.BITMASK, read=True),
            NilanProxyDatapointKey.BYPASS_ACTIVE: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.BOOL, read=True),
            NilanProxyDatapointKey.CO2_LEVEL: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.PPM, read=True),
            NilanProxyDatapointKey.DEFROST_ACTIVE: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.BOOL, read=True),
            NilanProxyDatapointKey.DEFROST_TIME_AGO:NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.DAYS, read=True),
            NilanProxyDatapointKey.FAN_DUTYCYCLE_EXTRACT: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.PCT, read=True),
            NilanProxyDatapointKey.FAN_DUTYCYCLE_SUPPLY: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.PCT, read=True),
            NilanProxyDatapointKey.FAN_LEVEL_CURRENT: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.UNDEFINED, read=True),
            NilanProxyDatapointKey.FAN_LEVEL_EXTRACT: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.UNDEFINED, read=True),
            NilanProxyDatapointKey.FAN_LEVEL_SUPPLY: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.UNDEFINED, read=True),
            NilanProxyDatapointKey.FAN_RPM_EXTRACT: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.RPM, read=True),
            NilanProxyDatapointKey.FAN_RPM_SUPPLY: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.RPM, read=True),
            NilanProxyDatapointKey.FILTER_REPLACE_TIME_AGO: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.DAYS, read=True),
            NilanProxyDatapointKey.FILTER_REPLACE_TIME_REMAIN: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.DAYS, read=True),
            NilanProxyDatapointKey.FILTER_OK: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.BOOL, read=True),
            NilanProxyDatapointKey.HUMIDITY: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.PCT, read=True),
            NilanProxyDatapointKey.HUMIDITY_HIGH_LEVEL: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.UNDEFINED, read=True),
            NilanProxyDatapointKey.HUMIDITY_HIGH_LEVEL_TIME: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.MINUTES, read=True),
            NilanProxyDatapointKey.HUMIDITY_AVG: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.PCT, read=True),
            NilanProxyDatapointKey.HUMIDITY_HIGH_ACTIVE: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.BOOL, read=True),
            NilanProxyDatapointKey.SACRIFICIAL_ANODE_OK: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.BOOL, read=True),
            NilanProxyDatapointKey.STATE_CODE: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.UNDEFINED, read=True),
            NilanProxyDatapointKey.TEMP_CONDENSER:NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.CELSIUS, read=True),
            NilanProxyDatapointKey.TEMP_EVAPORATOR:NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.CELSIUS, read=True),
            NilanProxyDatapointKey.TEMP_EXHAUST:NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.CELSIUS, read=True),
            NilanProxyDatapointKey.TEMP_EXTRACT: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.CELSIUS, read=True),
            NilanProxyDatapointKey.TEMP_HOTWATER_BOTTOM: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.CELSIUS, read=True),
            NilanProxyDatapointKey.TEMP_HOTWATER_TOP: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.CELSIUS, read=True),
            NilanProxyDatapointKey.TEMP_OUTSIDE: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.CELSIUS, read=True),
            NilanProxyDatapointKey.TEMP_ROOM: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.CELSIUS, read=True),
            NilanProxyDatapointKey.TEMP_SUPPLY: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.CELSIUS, read=True),
            NilanProxyDatapointKey.VOC_LEVEL: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.PPM, read=True),
            NilanProxyDatapointKey.WINTER_MODE_ACTIVE:NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.BOOL, read=True),
            
            NilanProxyDatapointKey.UNKNOWN_VALUE_1:NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.UNDEFINED, read=True),
            
            NilanProxySetpointKey.ALARM_RESET: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.BOOL, read=False),
            NilanProxySetpointKey.ANTILEGIONELLA_DAY: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.UNDEFINED, read=True),
            NilanProxySetpointKey.BOOST_ENABLE: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.BOOL, read=True),
            NilanProxySetpointKey.BOOST_TIME: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.MINUTES, read=True),
            NilanProxySetpointKey.CO2_THRESHOLD: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.PPM, read=True),
            NilanProxySetpointKey.COOLING_ENABLE: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.BOOL, read=True),
            NilanProxySetpointKey.COMPRESSOR_PRIORITY: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.UNDEFINED, read=True),
            NilanProxySetpointKey.DEFROST_MAX_TIME: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.MINUTES, read=True),
            NilanProxySetpointKey.DEFROST_BREAK_TIME: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.MINUTES, read=True),
            NilanProxySetpointKey.ENABLE: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.BOOL, read=True),
            NilanProxySetpointKey.FAN_LEVEL: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.UNDEFINED, read=True),
            NilanProxySetpointKey.FAN_LEVEL_LOW_HUMIDITY: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.UNDEFINED, read=True),
            NilanProxySetpointKey.FAN_LEVEL_HIGH_CO2: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.UNDEFINED, read=True),
            NilanProxySetpointKey.FAN_LEVEL_HIGH_HUMIDITY: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.UNDEFINED, read=True),
            NilanProxySetpointKey.FAN_LEVEL_HIGH_HUMIDITY_TIME: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.MINUTES, read=True),
            NilanProxySetpointKey.FAN_LEVEL1_EXTRACT_PRESET:NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.PCT, read=True),
            NilanProxySetpointKey.FAN_LEVEL1_SUPPLY_PRESET: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.PCT, read=True),
            NilanProxySetpointKey.FAN_LEVEL2_EXTRACT_PRESET:NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.PCT, read=True),
            NilanProxySetpointKey.FAN_LEVEL2_SUPPLY_PRESET: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.PCT, read=True),
            NilanProxySetpointKey.FAN_LEVEL3_EXTRACT_PRESET:NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.PCT, read=True),
            NilanProxySetpointKey.FAN_LEVEL3_SUPPLY_PRESET: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.PCT, read=True),
            NilanProxySetpointKey.FAN_LEVEL4_EXTRACT_PRESET:NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.PCT, read=True),
            NilanProxySetpointKey.FAN_LEVEL4_SUPPLY_PRESET: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.PCT, read=True),
            NilanProxySetpointKey.FILTER_REPLACE_INTERVAL: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.DAYS, read=True),
            NilanProxySetpointKey.FILTER_REPLACE_RESET: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.BOOL, read=False),
            NilanProxySetpointKey.HUMIDITY_CONTROL_ENABLE: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.BOOL, read=True),
            NilanProxySetpointKey.HUMIDITY_LOW_THRESHOLD: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.PCT, read=True),
            NilanProxySetpointKey.PREHEAT_ENABLE: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.BOOL, read=True),
            NilanProxySetpointKey.PREHEAT_CYCLE_TIME: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.SECONDS, read=True),
            NilanProxySetpointKey.PREHEAT_PID_D: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.UNDEFINED, read=True),
            NilanProxySetpointKey.PREHEAT_PID_I: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.UNDEFINED, read=True),
            NilanProxySetpointKey.PREHEAT_PID_P: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.UNDEFINED, read=True),
            NilanProxySetpointKey.REHEAT_ENABLE: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.BOOL, read=True),
            NilanProxySetpointKey.REHEAT_CYCLE_TIME: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.SECONDS, read=True),
            NilanProxySetpointKey.REHEAT_PID_D: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.UNDEFINED, read=True),
            NilanProxySetpointKey.REHEAT_PID_I: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.UNDEFINED, read=True),
            NilanProxySetpointKey.REHEAT_PID_P: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.UNDEFINED, read=True),
            NilanProxySetpointKey.TEMP_BYPASS_OPEN_OFFSET: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.CELSIUS, read=True),
            NilanProxySetpointKey.TEMP_COOLING_START_OFFSET: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.CELSIUS, read=True),
            NilanProxySetpointKey.TEMP_DEFROST_LOW_THRESHOLD: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.CELSIUS, read=True),
            NilanProxySetpointKey.TEMP_DEFROST_HIGH_THRESHOLD: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.CELSIUS, read=True),
            NilanProxySetpointKey.TEMP_HOTWATER: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.CELSIUS, read=True),
            NilanProxySetpointKey.TEMP_HOTWATER_BOOST: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.CELSIUS, read=True),
            NilanProxySetpointKey.TEMP_REGULATION_DEAD_BAND: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.CELSIUS, read=True),
            NilanProxySetpointKey.TEMP_REHEAT_OFFSET: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.CELSIUS, read=True),
            NilanProxySetpointKey.TEMP_TARGET: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.CELSIUS, read=True),
            NilanProxySetpointKey.TEMP_SUMMER_SUPPLY_MAX: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.CELSIUS, read=True),
            NilanProxySetpointKey.TEMP_SUMMER_SUPPLY_MIN: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.CELSIUS, read=True),
            NilanProxySetpointKey.TEMP_SUPPLY_MAX: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.CELSIUS, read=True),
            NilanProxySetpointKey.TEMP_SUPPLY_MIN: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.CELSIUS, read=True),
            NilanProxySetpointKey.TEMP_WINTER_SUPPLY_MAX: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.CELSIUS, read=True),
            NilanProxySetpointKey.TEMP_WINTER_SUPPLY_MIN: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.CELSIUS, read=True),
            NilanProxySetpointKey.TEMP_WINTER_MODE_THRESHOLD: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.CELSIUS, read=True),
            NilanProxySetpointKey.VOC_THRESHOLD: NilanProxyPointConfig(unit_of_measurement=NilanProxyUnits.PPM, read=True),
        }

class NilanProxyBaseModel:
    
    _attr_manufacturer:str = ""
    _attr_model_name:str = "Basemodel"
    
    datapoints: Dict[NilanProxyDatapointKey, NilanProxyDatapoint] = {}
    setpoints: Dict[NilanProxySetpointKey, NilanProxySetpoint] = {}
    _configs: Dict[NilanProxyDatapointKey|NilanProxySetpointKey, NilanProxyPointConfig] = {}
    _valueMap: Dict[NilanProxyDatapointKey|NilanProxySetpointKey, Dict[float | int, float | int | str]] = {}

    def __init__(self) -> None:
        return

    def get_model_name(self) -> str:
        return self._attr_model_name

    def get_manufacturer(self) -> str:
        return self._attr_manufacturer

    def model_provides_datapoint(self, datapoint: NilanProxyDatapointKey) -> bool:
        return datapoint in self.datapoints

    def get_datapoints_for_read(self) -> List[NilanProxyDatapointKey]:
        return [key for key, value in self._configs.items() if key in self.datapoints and value.get("read", False) == True]

    def model_provides_setpoint(self, datapoint: NilanProxySetpointKey) -> bool:
        return datapoint in self.setpoints

    def get_setpoints_for_read(self) -> List[NilanProxySetpointKey]:
        return [key for key, value in self._configs.items() if key in self.setpoints and value.get("read", False) == True]

    def get_unit_of_measure(self, key:NilanProxyDatapointKey|NilanProxySetpointKey) -> str|None:
        if key in self._configs: return self._configs[key]["unit_of_measurement"]
        return NilanProxyUnits.UNDEFINED
  
    def set_default_configs(self) -> None:
        """Sets the point configurations to the standard setup, will not override already assigned records"""
    #     # only keep the points supported by the unit
    #     self._configs = {key: value for key, value in DEFAULT_CONFIGS.items() if key in self._setpoints or key in self._datapoints}

    # def addMissingDefaultConfigs(self):
        # Update self._configs with missing items from DEFAULT_CONFIGS
        self._configs.update({
            key: value for key, value in DEFAULT_CONFIGS.items()
            if key not in self._configs and (key in self.setpoints or key in self.datapoints)
        })
    
    @staticmethod
    def modifier_flip_bool(value:float|int) -> float|int:
        """Flips the true/false state 
        - 1 -> 0
        - 0 -> 1"""
        return 1-value
    
    @staticmethod
    def modifier_seconds_to_minutes(value:float|int) -> float|int:
        return round(value/60)
    
    @staticmethod
    def modifier_hours_to_days(value:float|int) -> float|int:
        return round(value/24)