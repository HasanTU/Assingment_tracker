from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    SUBMITTED = "submitted"
    GRADED = "graded"
    OVERDUE = "overdue"