""" HomePilot related constants """

OTHER_TYPE = 0
COVER_TYPE = 1
SENSOR_TYPE = 2
SWITCH_ACTUATOR_TYPE = 3
THERMOSTAT_TYPE = 4
SMOKE_SENSOR_TYPE = 5
CONTACT_SENSOR_TYPE = 6
MOTION_SENSOR_TYPE = 7

# API Capability names
# Common
APICAP_PROT_ID_DEVICE_LOC = "PROT_ID_DEVICE_LOC"
APICAP_ID_DEVICE_LOC = "ID_DEVICE_LOC"
APICAP_NAME_DEVICE_LOC = "NAME_DEVICE_LOC"
APICAP_PROD_CODE_DEVICE_LOC = "PROD_CODE_DEVICE_LOC"
APICAP_VERSION_CFG = "VERSION_CFG"
APICAP_PING_CMD = "PING_CMD"
APICAP_REACHABILITY_EVT = "REACHABILITY_EVT"
APICAP_DEVICE_TYPE_LOC = "DEVICE_TYPE_LOC"
# Cover
APICAP_GOTO_POS_CMD = "GOTO_POS_CMD"
APICAP_SET_SLAT_POS_CMD = "SET_SLAT_POS_CMD"
APICAP_CURR_POS_CFG = "CURR_POS_CFG"
APICAP_CURR_SLAT_POS_CFG = "CURR_SLAT_POS_CFG"
APICAP_STOP_SLAT_CMD = "STOP_SLAT_CMD"
APICAP_STOP_CMD = "STOP_CMD"
APICAP_POS_UP_CMD = "POS_UP_CMD"
APICAP_POS_DOWN_CMD = "POS_DOWN_CMD"
APICAP_VENTIL_POS_MODE_CFG = "VENTIL_POS_MODE_CFG"
APICAP_VENTIL_POS_CFG = "VENTIL_POS_CFG"
# Switch
APICAP_CURR_SWITCH_POS_CFG = "CURR_SWITCH_POS_CFG"
APICAP_TURN_ON_CMD = "TURN_ON_CMD"
APICAP_TURN_OFF_CMD = "TURN_OFF_CMD"
# Sensor
APICAP_SUN_DIRECTION_MEA = "SUN_DIRECTION_MEA"
APICAP_SUN_HEIGHT_DEG_MEA = "SUN_HEIGHT_DEG_MEA"
APICAP_LIGHT_VAL_LUX_MEA = "LIGHT_VAL_LUX_MEA"
APICAP_WIND_SPEED_MS_MEA = "WIND_SPEED_MS_MEA"
APICAP_WIND_DETECTION_MEA = "WIND_DETECTION_MEA"
APICAP_TEMP_CURR_DEG_MEA = "TEMP_CURR_DEG_MEA"
APICAP_TEMP_TARGET_DEG_MEA = "TEMP_TARGET_DEG_MEA"
APICAP_RAIN_DETECTION_MEA = "RAIN_DETECTION_MEA"
APICAP_SUN_DETECTION_MEA = "SUN_DETECTION_MEA"
APICAP_CLOSE_CONTACT_MEA = "CLOSE_CONTACT_MEA"
APICAP_BATTERY_LVL_PCT_MEA = "BATTERY_LVL_PCT_MEA"
APICAP_BATT_VALUE_EVT = "BATT_VALUE_EVT"
APICAP_BATT_LOW_EVT = "BATT_LOW_EVT"
APICAP_BLOCK_DET_EVT = "BLOCK_DET_EVT"
APICAP_OBSTACLE_DET_EVT = "OBSTACLE_DET_EVT"
APICAP_MOTION_DETECTION_MEA = "MOTION_DETECTION_MEA"
APICAP_SMOKE_DETECTION_MEA = "SMOKE_DETECTION_MEA"
# Thermostat
APICAP_TARGET_TEMPERATURE_CFG = "TARGET_TEMPERATURE_CFG"
APICAP_TEMPERATURE_INT_CFG = "TEMPERATURE_INT_CFG"
APICAP_AUTO_MODE_CFG = "AUTO_MODE_CFG"
APICAP_RELAIS_STATE_CFG = "RELAIS_STATE_CFG"
APICAP_TEMPERATURE_THRESH_1_CFG = "TEMPERATURE_THRESH_1_CFG"
APICAP_TEMPERATURE_THRESH_2_CFG = "TEMPERATURE_THRESH_2_CFG"
APICAP_TEMPERATURE_THRESH_3_CFG = "TEMPERATURE_THRESH_3_CFG"
APICAP_TEMPERATURE_THRESH_4_CFG = "TEMPERATURE_THRESH_4_CFG"
# Light
APICAP_RGB_CFG = "RGB_CFG"
APICAP_SET_RGB_CMD = "SET_RGB_CMD"
APICAP_COLOR_TEMP_CFG = "COLOR_TEMP_CFG"
APICAP_SET_COLOR_TEMP_CMD = "SET_COLOR_TEMP_CMD"
APICAP_COLOR_MODE_CFG = "COLOR_MODE_CFG"

SUPPORTED_DEVICES = {
    "35001164": {"name": "DuoFern Switch actuator",
                 "Type": SWITCH_ACTUATOR_TYPE},
    "35000262": {
        "name": "DuoFern Universal actuator 2-channel",
        "Type": SWITCH_ACTUATOR_TYPE,
    },
    "35000462": {"name": "DuoFern Universal dimming actuator",
                 "Type": OTHER_TYPE},
    "36500572_A": {"name": "Troll Comfort DuoFern", "Type": OTHER_TYPE},
    "36500572_S": {"name": "Sun sensor Troll Comfort DuoFern",
                   "Type": SENSOR_TYPE},
    "36501512": {"name": "Troll Comfort DuoFern", "Type": OTHER_TYPE},
    "35002414": {"name": "Z-Wave Repeater with switching function",
                 "Type": OTHER_TYPE},
    "35140462": {"name": "DuoFern Universal dimmer", "Type": OTHER_TYPE},
    "35003064": {"name": "DuoFern Radiator Actuator", "Type": OTHER_TYPE},
    "35003064_A": {"name": "DuoFern Radiator Actuator", "Type": OTHER_TYPE},
    "35003064_S": {
        "name": "Temperature sensor DuoFern Radiator Actuator",
        "Type": SENSOR_TYPE,
    },
    "32501812_A": {"name": "DuoFern Room Thermostat", "Type": THERMOSTAT_TYPE},
    "32501812_S": {
        "name": "Temperature sensor DuoFern Room thermostat",
        "Type": SENSOR_TYPE,
    },
    "35002319": {"name": "Z-Wave radiator actuator", "Type": OTHER_TYPE},
    "35000662": {"name": "DuoFern tubular motor actuator", "Type": COVER_TYPE},
    "35000864": {"name": "DuoFern Connect actuator", "Type": OTHER_TYPE},
    "36500172": {"name": "Troll Basis DuoFern", "Type": OTHER_TYPE},
    "31500162": {"name": "DuoFern tubular motor control B50/B55",
                 "Type": COVER_TYPE},
    "27601565": {"name": "DuoFern tubular motor", "Type": COVER_TYPE},
    "16234511_A": {"name": "RolloTron Comfort DuoFern", "Type": COVER_TYPE},
    "16234511_S": {
        "name": "Sun sensor RolloTron Comfort DuoFern",
        "Type": SENSOR_TYPE,
    },
    "14236011": {"name": "RolloTron radio beltwinder 60 kg",
                 "Type": COVER_TYPE},
    "14234511": {"name": "RolloTron radio beltwinder", "Type": COVER_TYPE},
    "45059071": {"name": "RolloPort SX5 DuoFern", "Type": COVER_TYPE},
    "32000064_A": {
        "name": "DuoFern tubular motor actuator environmental sensor",
        "Type": COVER_TYPE,
    },
    "32000064_S": {
        "name": "Sensor DuoFern Environmental sensor",
        "Type": SENSOR_TYPE,
    },
    "32501772_A": {
        "name": "Actuator DuoFern Motion detector (indoor)",
        "Type": OTHER_TYPE,
    },
    "32501772_S": {
        "name": "Sensor DuoFern Motion detector (indoor)",
        "Type": OTHER_TYPE,
    },
    "32000069": {"name": "DuoFern Sun Sensor", "Type": OTHER_TYPE},
    "32001664": {"name": "DuoFern Smoke Alarm Device",
                 "Type": SMOKE_SENSOR_TYPE},
    "32001464": {"name": "DuoFern Awning monitor", "Type": OTHER_TYPE},
    "32002119": {"name": "Z-Wave window/door contact",
                 "Type": CONTACT_SENSOR_TYPE},
    "32004219": {"name": "HomePilot\xae HD Camera (Indoor)",
                 "Type": OTHER_TYPE},
    "32004329": {"name": "HomePilot\xae HD Camera (Outdoor)",
                 "Type": OTHER_TYPE},
    "32004119": {"name": "IP Camera", "Type": OTHER_TYPE},
    "99999999": {"name": "Android Smartphone (GeoPilot)", "Type": OTHER_TYPE},
    "99999998": {"name": "iOS Smartphone (GeoPilot)", "Type": OTHER_TYPE},
    "32003164": {"name": "DuoFern Window/Door Contact",
                 "Type": CONTACT_SENSOR_TYPE},
    "32480366": {
        "name": "DuoFern Standard manual transmitter 6 groups 48 devices",
        "Type": OTHER_TYPE,
    },
    "32480361": {
        "name": "DuoFern Standard manual transmitter 1 group 48 devices",
        "Type": OTHER_TYPE,
    },
    "32010361": {
        "name": "DuoFern Standard manual transmitter 1 group 1 device",
        "Type": OTHER_TYPE,
    },
    "32060366": {
        "name": "DuoFern Standard manual transmitter 1 group 6 devices",
        "Type": OTHER_TYPE,
    },
    "32000062_S": {"name": "Sensor DuoFern Radio transmitter UP",
                   "Type": OTHER_TYPE},
    "32000062": {"name": "DuoFern radio transmitter UP", "Type": OTHER_TYPE},
    "32501972_A": {
        "name": "Actuator DuoFern Multiple Wall Controller 230V",
        "Type": OTHER_TYPE,
    },
    "32501972_S": {
        "name": "Sensor DuoFern Multiple Wall Controller 230V",
        "Type": OTHER_TYPE,
    },
    "32501974": {"name": "DuoFern Multiple Wall Controller BAT",
                 "Type": OTHER_TYPE},
    "32160211": {"name": "DuoFern Wall Controller", "Type": OTHER_TYPE},
    "34810060": {"name": "DuoFern Central Operating Unit", "Type": OTHER_TYPE},
    "32501371": {"name": "DuoFern HomeTimer", "Type": OTHER_TYPE},
    "35140662": {"name": "DuoFern tubular motor actuator", "Type": COVER_TYPE},
    "32501973": {"name": "DuoFern Wall Controller 1 channel",
                 "Type": OTHER_TYPE},
    "23602075": {"name": "RolloTube S-line DuoFern", "Type": COVER_TYPE},
    "25782075": {"name": "RolloTube S-line Zip DuoFern", "Type": COVER_TYPE},
    "23782076": {"name": "RolloTube S-line Sun DuoFern", "Type": OTHER_TYPE},
    "35274001": {"name": "addZ White + Colour LED E27", "Type": OTHER_TYPE},
    "35144001": {"name": "addZ White + Colour LED E14", "Type": OTHER_TYPE},
    "35104001": {"name": "addZ White + Colour LED GU10", "Type": OTHER_TYPE},
    "99999973": {"name": "Zigbee White LED", "Type": OTHER_TYPE},
    "99999974": {"name": "Zigbee tuneable white LED", "Type": OTHER_TYPE},
    "99999975": {"name": "Zigbee RGBW LED", "Type": OTHER_TYPE},
    "99999976": {"name": "Zigbee RGB LED", "Type": OTHER_TYPE},
    "99999950": {"name": "ONVIF Camera", "Type": OTHER_TYPE},
    "32004464": {"name": "DuoFern Sun/Wind Sensor", "Type": OTHER_TYPE},
    "32320364": {
        "name": "DuoFern Standard manual transmitter 4 groups",
        "Type": OTHER_TYPE,
    },
}
