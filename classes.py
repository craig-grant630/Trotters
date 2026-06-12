# https://dev.to/dpills/python-secure-password-management-hashing-and-encryption--1246 Encryption of passwords for later
# https://blog.devgenius.io/mastering-python-dictionaries-30896dda7568
class Student:
    def __init__(self, student_id, name, programme_code, campus_code, year_of_study, password):
        self.student_id = student_id
        self.name = name
        self.programme_code = programme_code.upper()
        self.campus_code = campus_code.upper()
        self.year_of_study = year_of_study
        self.password = password

    def to_dict(self):
        return self.__dict__

# Use class method in order to create new students from a dictionary
    @classmethod
    def from_dict(cls, data):
        return cls(data['student_id'], data['name'], data['programme_code'], data['campus_code'],
                   data['year_of_study'], data['password'])

    def __repr__(self):
        return f"Student: ({self.student_id}), {self.name}"

class Campus:
    def __init__(self, campus_code, name):
        self.campus_code = campus_code.upper()
        self.name = name

    def to_dict(self):
        return self.__dict__

    # Use class method in order to create new campus from a dictionary
    @classmethod
    def from_dict(cls, data):
        return cls(data['campus_code'], data['name'])

    def __repr__(self):
        return f"Campus: ({self.campus_code}, {self.name})"

class Module:
    def __init__(self, module_code, name, year):
        self.module_code = module_code.upper()
        self.name = name
        self.year = year

    def to_dict(self):
        return self.__dict__

    # Use class method in order to create new module from a dictionary
    @classmethod
    def from_dict(cls, data):
        return cls(data['module_code'], data['name'], data['year'])

    def __repr__(self):
        return f"Module: ({self.module_code}, {self.name}, year = {self.year})"

class Programme:
    def __init__(self, programme_code, name, campus_codes, modules=None):
        self.programme_code = programme_code.upper()
        self.name = name
        self.campus_codes = []
        # change all campus codes to uppercase
        for code in campus_codes:
            self.campus_codes.append(code.upper())
        if modules is not None:
            self.modules = modules
        else:
            self.modules = []

    def modules_for_year(self, year):
        return [m for m in self.modules if int(m.year) == int(year)]

    def to_dict(self):
            return {
                "programme_code": self.programme_code,
                "name": self.name,
                "campus_codes": self.campus_codes,
                "modules": [m.to_dict() for m in self.modules],
            }

    @classmethod
    def from_dict(cls, data):
        # Turn modules from the data dictionary in the modules key into a list object
        modules = []
        for m in data.get("modules", []):
            m = Module.from_dict(m)
            modules.append(m)

        return cls(
            programme_code = data["programme_code"],
            name=data["name"],
            campus_codes = data["campus_codes"],
            modules = modules,
        )

    def __repr__(self):
        return f"Programme: ({self.programme_code}, {self.name})"
#=======================================================================================================================
#REQUESTS
VALID_DAYS= ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
VALID_PERIODS = ["Morning", "Afternoon", "Evening"]

class Requests:
    def __init__(self, request_id, student_id,campus_code, programme_code,year, module_code,availability=None):
        self.request_id = request_id
        self.student_id = student_id
        self.campus_code = campus_code.upper()
        self.programme_code = programme_code.upper()
        self.year = year
        self.module_code = module_code.upper()
        if availability is not None:
            self.availability = availability
        else:
            self.availability = []

    def add_availability(self, day, period):
        if day not in VALID_DAYS or period not in VALID_PERIODS:
            return False
        timeslot = {"day": day, "period": period}
        if timeslot in self.availability:
            return False
        self.availability.append(timeslot)
        return True

    def remove_availability(self, day, period):
        timeslot = {"day": day, "period": period}
        if timeslot in self.availability:
            self.availability.remove(timeslot)
            return True
        return False

    def overlapping_availability(self, other):
        return [s for s in self.availability if s in other.availability]


    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        return cls(data["request_id"], data["student_id"], data["campus_code"], data["programme_code"], data["year"], data["module_code"], data.get("availability",[]))

class Admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        return cls(data['username'], data['password'])