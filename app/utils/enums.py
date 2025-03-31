from enum import Enum

class CheckoutStatus(int, Enum):
    AVAILABLE = 0  # File is not checked out
    CHECKED_OUT = 1  # File is checked out by someone
