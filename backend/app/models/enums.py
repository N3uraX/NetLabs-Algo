import enum

class DeviceType(str, enum.Enum):
    MIKROTIK = "mikrotik"
    CISCO_IOS = "cisco_ios"
    JUNIPER_JUNOS = "juniper_junos"
    PFSENSE = "pfsense"
    OTHER = "other"

class DeviceStatus(str, enum.Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    UNINITIALIZED = "uninitialized" # Not yet connected or status unknown
    ERROR = "error" # Connection error or other issue 