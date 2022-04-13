NULL_CHAR = bytes((0,))
CONSUMER_CONTROL_RELEASE = NULL_CHAR*2

keys = {
    "UP": bytes((66,)) + NULL_CHAR,
    "DOWN": bytes((67,))+NULL_CHAR,
    "LEFT": bytes((68,))+NULL_CHAR,
    "RIGHT": bytes((69,))+NULL_CHAR,
    "SELECT": bytes((65,))+NULL_CHAR,
    "HOME": bytes((35,))+bytes((2,)),
    "BACK": bytes((36,))+bytes((2,)),
    "PLAY": bytes((205,))+NULL_CHAR,
    "MUTE": bytes((226,))+NULL_CHAR,
    "MIC": bytes((207,))+NULL_CHAR,
}