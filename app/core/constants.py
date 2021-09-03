import enum

SUPERUSER_PRIVILEGE_DESC = "Can only be accessed by superusers"
BASIC_USER_DESC = "Can only be accessed by logged-in users."
PUBLIC_DESC = "Can be accessed by everybody, including users who are not logged in."


class DrivingLicenceTypeEnum(enum.Enum):
    LICENCE_2 = "2"
    LICENCE_2A = "2A"
    LICENCE_2B = "2B"


class TransmissionTypeEnum(enum.Enum):
    MANUAL = "Manual"
    AUTOMATIC = "Automatic"
