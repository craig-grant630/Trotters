# https://medium.com/@idelossantosruiz/mastering-json-in-python-oop-a-practical-guide-65b39e868c33
import os
import json
from classes import Campus, Module, Programme, Student, Requests, Admin

class FileHandler:

    CAMPUS_FILE = 'campuses.json'
    STUDENTS_FILE = 'student.json'
    PROGRAMMES_FILE = 'programmes.json'
    REQUESTS_FILE = 'requests.json'
    ADMIN_FILE = 'admin.json'
#=======================================================================================================================
    # Initialise paths and set read and write methods
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        # make data directory for JSON files if not there else do nothing
        os.makedirs(self.data_dir, exist_ok=True)

    def path(self, filename):
        # create the path to the JSON files
        return os.path.join(self.data_dir, filename)

    def read_file(self, filename):
        # Read the JSON files and return
        filepath = self.path(filename)
        if not os.path.exists(filepath):
            return []
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except ValueError:
            return []

    def write_file(self, filename, data):
        filepath = self.path(filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
#=======================================================================================================================
    # Students save and load
    def save_students(self, students):
        result = []
        for s in students.values():
            students_dict = s.to_dict()
            result.append(students_dict)
        return self.write_file(FileHandler.STUDENTS_FILE, result)

    def load_students(self):
        result = {}
        # Change reading JSON file to a dictionary of objects
        for s_dict in self.read_file(FileHandler.STUDENTS_FILE):
            s_object = Student.from_dict(s_dict)
            s_key = s_object.student_id
            result[s_key] = s_object
        return result

#=======================================================================================================================
    # Campuses save and load
    def save_campuses(self, campuses):
        result = []
        for c in campuses.values():
            # Use method from Campus class to change into a dictionary and append to the list for storage
            campus_dict = c.to_dict()
            result.append(campus_dict)
        return self.write_file(FileHandler.CAMPUS_FILE, result)

    def load_campuses(self):
        result = {}
        # Change reading JSON file to a dictionary of objects
        for c_dict in self.read_file(FileHandler.CAMPUS_FILE):
            c_object = Campus.from_dict(c_dict)
            c_key = c_object.campus_code
            result[c_key] = c_object
        return result
#=======================================================================================================================
    # Programme Save and load
    def programme_save(self, programmes):
        result = []
        for p in programmes.values():
            # Use method from programmes class to change into a dictionary
            programmes_dict = p.to_dict()
            result.append(programmes_dict)
        return self.write_file(FileHandler.PROGRAMMES_FILE, result)
    #
    def load_programmes(self):
        result = {}
        # Change reading JSON file to a dictionary of objects
        for p_dict in self.read_file(FileHandler.PROGRAMMES_FILE):
            p_object = Programme.from_dict(p_dict)
            p_key = p_object.programme_code
            result[p_key] = p_object
        return result
#=======================================================================================================================
    #Requests save and load
    def requests_save(self, requests):
        result = []
        for r in requests.values():
            # Use method from requests class to change into a dictionary
            requests_dict = r.to_dict()
            result.append(requests_dict)
        return self.write_file(FileHandler.REQUESTS_FILE, result)

    def load_requests(self):
        result = {}
        # Change reading JSON file to a dictionary of objects
        for r_dict in self.read_file(FileHandler.REQUESTS_FILE):
            r_object = Requests.from_dict(r_dict)
            r_key = r_object.request_id
            result[r_key] = r_object
        return result

    @staticmethod
    def next_request_id(requests):
        if not requests:
            return 1
        else:
            return max(int(r.request_id) for r in requests.values()) + 1
#=======================================================================================================================
    def admin_save(self, admin):
        result = []
        for a in admin.values():
            # Use method from admin class to change into a dictionary
            admin_dict = a.to_dict()
            result.append(admin_dict)
        return self.write_file(FileHandler.ADMIN_FILE, result)
    #
    def load_admin(self):
        result = {}
        # Change reading JSON file to a dictionary of objects
        for a_dict in self.read_file(FileHandler.ADMIN_FILE):
            a_object = Admin.from_dict(a_dict)
            a_key = a_object.username
            result[a_key] = a_object
        return result
#=======================================================================================================================
    # Check if required data and starting data is required methods
    def required_campus_data_needed(self):
        result = False
        if not os.path.exists(self.path(FileHandler.CAMPUS_FILE)) or len(self.read_file(FileHandler.CAMPUS_FILE)) <= 0:
            result = True
        return result

    def required_programme_data_needed(self):
        result = False
        if not os.path.exists(self.path(FileHandler.PROGRAMMES_FILE)) or len(self.read_file(FileHandler.PROGRAMMES_FILE)) <= 0:
            result = True
        return result

    def required_admin_data_needed(self):
        result = False
        if not os.path.exists(self.path(FileHandler.ADMIN_FILE)) or len(
                self.read_file(FileHandler.ADMIN_FILE)) <= 0:
            result = True
        return result

    def sample_students_data_needed(self):
        result = False
        if not os.path.exists(self.path(FileHandler.STUDENTS_FILE)) or len(
                self.read_file(FileHandler.STUDENTS_FILE)) <= 0:
            result = True
        return result

    def sample_requests_data_needed(self):
        result = False
        if not os.path.exists(self.path(FileHandler.REQUESTS_FILE)) or len(
                self.read_file(FileHandler.REQUESTS_FILE)) <= 0:
            result = True
        return result
#========================================================================================================================
    #Sample Data implemented methods - Required Data (Programmes and Campuses), Testing Data (Students)
    def set_required_campus_data(self):

        campuses = {"PCK": Campus("PCK", "Peckham"),
                    "NYC": Campus("NYC", "New York"),
                    "PAR": Campus("PAR", "Paris")}
        self.save_campuses(campuses)

    def set_required_programme_data(self):

        # campus codes for programmes
        all_campuses = ["PCK", "NYC", "PAR"]
        uk_campuses = ["PCK"]

        # Modules for Programmes
        # baent modules - BA Entrepreneurship
        baent_modules = [Module("BENT11", "Introduction to Entrepreneurship", 1),
                        Module("BENT12", "Planning for Business", 1),
                        Module("BENT13", "Financial Literacy", 1),
                        Module("BENT21", "Business Research", 2),
                        Module("BENT22", "Design Thinking", 2),
                        Module("BENT23", "Business Models", 2),
                        Module("BENT31", "Entrepreneurship Project", 3)]
        # bamkt modules - BA Marketing
        bamkt_modules = [Module("BMKT11", "Marketing Principles", 1),
                         Module("BMKT12", "Customer Behaviors", 1),
                         Module("BMKT13", "Market Research", 1),
                         Module("BMKT21", "Digital Marketing", 2),
                         Module("BMKT22", "Management Methodologies", 2),
                         Module("BMKT23", "Business Analysis", 2),
                         Module("BMKT31", "Marketing Project", 3)]
        # bacat modules - BA Creative Accounting
        bacat_modules = [Module("BCAT11", "Introduction to Accounting", 1),
                         Module("BCAT12", "Report Planning", 1),
                         Module("BCAT12", "Business Essential", 1),
                         Module("BCAT21", "Managing Accounting", 2),
                         Module("BCAT22", "Financial Accounting", 2),
                         Module("BCAT23", "Tax Fundamentals", 2),
                         Module("BCAT31", "Accounting Project", 3),]
        # bccs modules - BS Computing Science
        bscs_modules = [Module("BSCS11", "Introduction to Programming", 1),
                         Module("BSCS12", "Introduction to Software Engineering", 1),
                         Module("BSCS13", "Problem Solving", 1),
                         Module("BSCS21", "Database System", 2),
                         Module("BSCS22", "Data Analysis", 2),
                         Module("BSCS23", "Machine Learning", 2),
                         Module("BSCS31", "Computing Project", 3)]
        # bnaval modules - BA Naval History
        bnaval_modules = [Module("BNAV11", "Royal Navy", 1),
                          Module("BNAV11", "Historic Naval Ships", 1),
                          Module("BNAV11", "Strategic Naval Decisions", 1),
                          Module("BNAV21", "WW2 Commanding Officers", 2),
                          Module("BNAV21", "Historical Research", 2),
                          Module("BNAV21", "Engineering of Naval Ships", 2),
                          Module("BNAV31", "Navy Project", 3),]

        programmes = {
            "BAENT": Programme("BAENT","BA Entrepreneurship", all_campuses, baent_modules),
            "BAMKT": Programme("BAMKT", "BA Marketing", all_campuses, bamkt_modules),
            "BACAT": Programme("BACAT", "BA Creative Accounting", all_campuses, bacat_modules),
            "BSCSC": Programme("BSCSC", "BS Computing Science", all_campuses, bscs_modules),
            "BANAV": Programme("BANAV","BA British Naval History", uk_campuses, bnaval_modules)
        }

        self.programme_save(programmes)

    def set_required_admin_data(self):
        admin = {"Admin":Admin("Admin", "1234")}

        for a in admin.values():
            a.password = a.hash_password(a.password)

        self.admin_save(admin)

    def set_sample_requests(self):

        requests = {
            # 1. Craig Grant - BAENT, Year 3
            "1": Requests(1, "1110000000", "PCK", "BAENT", "3", "BENT31", [{"day": "Monday", "period": "Afternoon"}]),
            "2": Requests(2, "1110000000", "NYC", "BAENT", "3", "BENT31", [{"day": "Wednesday", "period": "Morning"}]),
            "3": Requests(3, "1110000000", "PAR", "BAENT", "3", "BENT31", [{"day": "Friday", "period": "Evening"}]),

            # 2. Iain Grant - BSCSC, Year 1
            "4": Requests(4, "1111000000", "PCK", "BSCSC", "1", "BSCS11", [{"day": "Tuesday", "period": "Morning"}]),
            "5": Requests(5, "1111000000", "NYC", "BSCSC", "1", "BSCS12", [{"day": "Thursday", "period": "Afternoon"}]),
            "6": Requests(6, "1111000000", "PCK", "BSCSC", "1", "BSCS13", [{"day": "Friday", "period": "Afternoon"}]),

            # 3. John Grant - BAMKT, Year 2
            "7": Requests(7, "1111100000", "PAR", "BAMKT", "2", "BMKT21", [{"day": "Monday", "period": "Morning"}]),
            "8": Requests(8, "1111100000", "PAR", "BAMKT", "2", "BMKT22",[{"day": "Wednesday", "period": "Afternoon"}]),
            "9": Requests(9, "1111100000", "PCK", "BAMKT", "2", "BMKT23", [{"day": "Thursday", "period": "Evening"}]),

            # 4. Lyndsay Grant - BANAV, Year 1
            "10": Requests(10, "1111110000", "PCK", "BANAV", "1", "BNAV11", [{"day": "Monday", "period": "Afternoon"}]),
            "11": Requests(11, "1111110000", "PCK", "BANAV", "1", "BNAV11", [{"day": "Tuesday", "period": "Evening"}]),
            "12": Requests(12, "1111110000", "PCK", "BANAV", "1", "BNAV11", [{"day": "Thursday", "period": "Morning"}]),

            # 5. Laura Grant - BACAT, PCK, Year 1
            "13": Requests(13, "1111111000", "PCK", "BACAT", "1", "BCAT12",
                           [{"day": "Wednesday", "period": "Morning"}]),
            "14": Requests(14, "1111111000", "PCK", "BACAT", "1", "BCAT12", [{"day": "Friday", "period": "Afternoon"}]),
            "15": Requests(15, "1111111000", "PCK", "BACAT", "1", "BCAT12", [{"day": "Monday", "period": "Evening"}]),

            # 6. Jamie Lumsden - BAMKT, PCK, Year 2
            "16": Requests(16, "1111111100", "PCK", "BAMKT", "2", "BMKT21",
                           [{"day": "Tuesday", "period": "Afternoon"}]),
            "17": Requests(17, "1111111100", "PCK", "BAMKT", "2", "BMKT22", [{"day": "Thursday", "period": "Morning"}]),
            "18": Requests(18, "1111111100", "PCK", "BAMKT", "2", "BMKT23", [{"day": "Friday", "period": "Evening"}]),

            # 7. Craig Donald - BAENT, PCK, Year 2
            "19": Requests(19, "1111111110", "PCK", "BAENT", "2", "BENT21", [{"day": "Monday", "period": "Morning"}]),
            "20": Requests(20, "1111111110", "PCK", "BAENT", "2", "BENT22",
                           [{"day": "Wednesday", "period": "Afternoon"}]),
            "21": Requests(21, "1111111110", "PCK", "BAENT", "2", "BENT23", [{"day": "Thursday", "period": "Evening"}]),

            # 8. Lewis McCreadie - BANAV, PCK, Year 1
            "22": Requests(22, "1111111111", "PCK", "BANAV", "1", "BNAV11", [{"day": "Tuesday", "period": "Morning"}]),
            "23": Requests(23, "1111111111", "PCK", "BANAV", "1", "BNAV12",[{"day": "Wednesday", "period": "Evening"}]),
            "24": Requests(24, "1111111111", "PCK", "BANAV", "1", "BNAV11", [{"day": "Friday", "period": "Afternoon"}])
        }
        self.requests_save(requests)

    def set_sample_students(self):

        students = {"1110000000":Student("1110000000","Craig Grant","BAENT","PCK","3","Password123"),
                    "1111000000":Student("1111000000","Iain Grant","BSCSC","PCK","1","Password123"),
                    "1111100000":Student("1111100000","John Grant","BAMKT","PAR","2","Password123"),
                    "1111110000":Student("1111110000","Lyndsay Grant","BANAV","PCK","1","Password123"),
                    "1111111000":Student("1111111000","Laura Grant","BACAT","PCK","1","Password123"),
                    "1111111100":Student("1111111100","Jamie Lumsden","BAMKT","PCK","2","Password123"),
                    "1111111110":Student("1111111110","Craig Donald","BAENT","PCK","2","Password123"),
                    "1111111111":Student("1111111111","Lewis McCreadie","BANAV","PCK","1","Password123")}
        for student in students.values():
            student.password = student.hash_password(student.password)

        self.save_students(students)