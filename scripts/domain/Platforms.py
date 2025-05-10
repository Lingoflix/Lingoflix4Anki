from enum import Enum

class Platform(Enum):
    DESKTOP = "Desktop"
    ANDROID = "Android"
    IOS = "iOS"
    WEB = "Web"
    UNKNOWN = "Unknown"
    # Add more platforms as needed
    def __str__(self):
        return self.value
    def __repr__(self):
        return self.value
    def __hash__(self):
        return hash(self.value)
    def __eq__(self, other):
        if isinstance(other, Platform):
            return self.value == other.value
        return False
    def __ne__(self, other):
        if isinstance(other, Platform):
            return self.value != other.value
        return True
