from enum import Enum

class Role(Enum):
    ADMIN = "ADMIN"
    TEACHER = "TEACHER"
    STUDENT = "STUDENT"

class ClassEnum(Enum):
    CLASS_1 = "Class 1"
    CLASS_2 = "Class 2"
    CLASS_3 = "Class 3"
    CLASS_4 = "Class 4"
    CLASS_5 = "Class 5"
    CLASS_6 = "Class 6"
    CLASS_7 = "Class 7"
    CLASS_8 = "Class 8"
    CLASS_9 = "Class 9"
    CLASS_10 = "Class 10"
    
def calculate_grade(percentage):
    """Assigns a grade based on percentage."""
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"