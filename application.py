from data_storage import FileHandler
from classes import Student, Requests, Programme, Module, Campus


class StudyBuddyApp:
    def __init__(self):
        self.store = FileHandler()

        if self.store.required_campus_data_needed():
            # give required data (campuses)
            self.store.set_required_campus_data()
        if self.store.required_programme_data_needed():
            # give required data (programmes)
            self.store.set_required_programme_data()
        if self.store.required_admin_data_needed():
            # give required data (admin)
            self.store.set_required_admin_data()
        if self.store.sample_students_data_needed():
        # give sample data (students)
            self.store.set_sample_students()

        # Load all data into memory
        self.programmes = self.store.load_programmes()
        self.campuses = self.store.load_campuses()
        self.students = self.store.load_students()
        self.requests = self.store.load_requests()
        self.admin = self.store.load_admin()

        # Find all modules and all module codes
        self.all_modules = []
        self.all_module_codes = []

        for programme in self.programmes.values():
            self.all_modules.extend(programme.modules)

        for module in self.all_modules:
            self.all_module_codes.append(module.module_code)

# Register validations and login authentication
# Students CRUD functionality
    #=========================================================================================================
    def check_register_credentials(self, student_id, password1, password2, campus_code, programme_code, year, name):
        if student_id in self.students:
            return False, "WARNING: \n Student ID already exists within the system."
        if not (student_id.isdigit() and len(student_id) == 10):
            return False, "WARNING: \n Student ID must be 10 digits"
        if not password1:
            return False, "WARNING: \n Password is empty. Please enter."
        if not password2:
            return False, "WARNING: \n Please confirm password."
        if password1 != password2:
            return False, "WARNING: \n Passwords do not match."
        if not programme_code:
            return False, "WARNING: \n Program Code must be provided."
        if not campus_code:
            return False, "WARNING: \n Campus Code must be provided."
        if not year:
            return False, "WARNING: \n Year of Study must be provided via dropdown."
        if not name:
            return False, "WARNING: Name must be provided."

        for programme in self.programmes.values():
            if programme_code == programme.programme_code:
                if campus_code not in programme.campus_codes:
                    return False, "WARNING: \n Campus is not available for this Programme"
        return True, None

    def add_student(self, student_id, name, password1, campus_code, programme_code, year):

        student = Student(student_id, name, programme_code, campus_code, year, password1)
        self.students[student_id] = student
        self.store.save_students(self.students)

    def authenticate(self, student_id, password):
        student = self.students.get(student_id)

        if not student:
            return False, "WARNING:  Student ID does not exist within the system."
        if not password:
            return False, "WARNING:  Password is empty. Please enter."
        if student.password != password:
            return False, "WARNING:  Password does not match."
        else:
            return True, student

    def authenticate_admin(self, username, password):
        admin = self.admin.get(username)

        if not admin:
            return False, "WARNING:  Administrator does not exist within the system."
        if not password:
            return False, "WARNING:  Password is empty. Please enter."
        if admin.password != password:
            return False, "WARNING:  Password does not match."
        else:
            return True, admin

    def delete_profile(self, student_id):

        if student_id in self.students:
            del self.students[student_id]
        requests = self.get_requests_for_student(student_id)

        for r in requests:
            del self.requests[r.request_id]

        self.store.requests_save(self.requests)
        self.store.save_students(self.students)

    # =========================================================================================================
    # Students Update profile functionality
    # =========================================================================================================
    def check_update_credentials(self, student_id, name, password, campus_code, programme_code, year):
        """Validates student profile updates without checking for primary key availability conflicts."""
        if not name:
            return False, "WARNING: \n Name must be provided."
        if not password:
            return False, "WARNING: \n Password is empty. Please enter."
        if not programme_code:
            return False, "WARNING: \n Program Code must be provided."
        if not campus_code:
            return False, "WARNING: \n Campus Code must be provided."
        if not year:
            return False, "WARNING: \n Year of Study must be provided via dropdown."

        # Validate that the selected campus actually runs that specific programme
        for programme in self.programmes.values():
            if programme_code == programme.programme_code:
                if campus_code not in programme.campus_codes:
                    return False, "WARNING: \n Selected Campus is not available for this Programme."

        return True, None

    def update_student(self, student_id, name, password, campus_code, programme_code, year):
        """Updates the student instance fields inside memory storage dictionary and commits changes to files."""
        student = self.students.get(student_id)
        if student:
            # Overwrite properties with new validated form values
            student.name = name
            student.password = password
            student.programme_code = programme_code
            student.campus_code = campus_code
            student.year_of_study = year

            # Commit the dictionary update down to your text/JSON persistent layer
            self.store.save_students(self.students)
            return True
        return False

    # Request lookups by student ID and request ID
# Request CRUD methods
#=======================================================================================================================
    def get_requests_for_student(self, student_id):
        result=[]
        for request in self.requests.values():
            if request.student_id == student_id:
                result.append(request)
        return result

    def get_request_by_id(self, request_id):
        for request in self.requests.values():
            if request.request_id == request_id:
                return request
        return None

    def edit_request(self, request_id, student_id, campus, module, availability):
        request = self.get_request_by_id(request_id)
        if not request:
            return False, "Request not found"

        if request.student_id != student_id:
            return False, "ERROR: You can only edit your own request"

        prog = self.programmes.get(request.programme_code)
        if not prog:
            return False, "ERROR: Associated programme not found"

        year_modules = [m.module_code.upper() for m in prog.modules_for_year(int(request.year))]
        if module.upper().strip() not in year_modules:
            return False, f"ERROR: Module {module} is not valid for your year of study"

        if campus.upper().strip() not in prog.campus_codes:
            return False, "ERROR: Campus is not available for this programme"

        if not availability:
            return False, "ERROR: One availability timeslot at least is required"

        request.module_code = module.upper()
        request.campus_code = campus
        request.availability = list(availability)

        self.store.requests_save(self.requests)
        return True, request

    def add_request(self, student_id, programme, campus, module, availability):
        student = self.students.get(student_id)
        if not student:
            return False, "ERROR: Student profile records not found"

        prog = self.programmes.get(programme.upper())
        if not prog:
            return False, f"ERROR: Programme '{programme}' does not exist"

        student_year = getattr(student, 'year', getattr(student, 'year_of_study', None))
        if student_year is None:
            return False, "ERROR: Student year of study data missing"

        year_modules = [m.module_code.upper().strip() for m in prog.modules_for_year(int(student_year))]
        if module.upper().strip() not in year_modules:
            return False, f"ERROR: Module {module} is not valid for your year of study"

        if campus.upper().strip() not in [c.upper().strip() for c in prog.campus_codes]:
            return False, "ERROR: Campus is not available for this programme"

        if not availability:
            return False, "ERROR: One availability timeslot at least is required"

        # Create and save item structure
        request_id = self.store.next_request_id(self.requests)

        request = Requests(request_id,student_id,campus.upper().strip(),programme.upper(),int(student_year),module.upper().strip(),list(availability))
        self.requests[request_id] = request
        self.store.requests_save(self.requests)

        return True, request

    def delete_request(self, request_id, student_id):
        request = self.get_request_by_id(request_id)
        if not request:
            return False, "ERROR: Request not found"
        if request.student_id != student_id:
            return False, "ERROR: You can only delete your own request"
        if request_id in self.requests:
            del self.requests[request_id]

        self.store.requests_save(self.requests)
        return True, "Request deleted successfully"

# Campus CRUD functionality and lookups
# ======================================================================================================================
    def campus_name(self, campus_code):
        for campus in self.campuses.values():
            if campus.campus_code == campus_code:
                return campus.name
        return None

    def get_campus(self, campus_code):
        for campus in self.campuses.values():
            if campus.campus_code == campus_code:
                return campus
        return None

    def delete_campus(self, code):
        campus = self.get_campus(code)
        if not campus:
            return False, "ERROR: Programme not found", 0, 0

        student_count = 0
        request_count = 0

        if code in self.campuses:
            # Count them first while the dictionaries are intact
            for student in self.students.values():
                if student.campus_code == code:
                    student_count += 1
                    for request in self.requests.values():
                        if request.student_id == student.student_id:
                            request_count += 1

            for programme in list(self.programmes.values()):
                refresh_codes = []
                for campus_code in programme.campus_codes:
                    if code != campus_code:
                        refresh_codes.append(campus_code)
                programme.campus_codes = refresh_codes


            for students in list(self.students.values()):
                if students.campus_code == code:
                    for requests in list(self.requests.values()):
                        if requests.student_id == students.student_id:
                            del self.requests[requests.request_id]
                    del self.students[students.student_id]
            del self.campuses[code]

        self.store.requests_save(self.requests)
        self.store.save_students(self.students)
        self.store.save_campuses(self.campuses)
        self.store.programme_save(self.programmes)

        # Return the counts back to the UI
        return True, student_count, request_count

    def add_campus(self, code, name):
        if code in self.campuses:
            return False, "ERROR: Campus code already exists"
        if len(code) != 3:
            return False, "ERROR: Campus code must be 3 digits"
        campus = Campus(code, name)
        self.campuses[code] = campus
        self.store.requests_save(self.requests)

        return True, "Campus added successfully"

    def edit_campus(self, code, name):
        campus = self.get_campus(code)
        if not campus:
            return False, "Campus not found"
        campus.name = name

        self.store.save_campuses(self.campuses)
        return True, "Campus edited successfully"

# Find Match results and score functionality
#===================================================
    def find_matches(self, request):
        source  = request
        if not source:
            return []

        results = []
        for option in self.requests.values():
            if option.request_id == source.request_id:
                continue
            if option.student_id == source.student_id:
                continue
            score = self.score_match(source, option)
            if score == 0:
                continue

            overlaps = source.overlapping_availability(option)
            results.append({
                "request": option,
                "student": self.students.get(option.student_id),
                "score": score,
                "overlaps": overlaps
            })

        results.sort(key=lambda x: (x["score"], len(x["overlaps"])), reverse=True)

        return results

    @staticmethod
    def score_match(source, option):
        if not source.campus_code or not option.campus_code:
            return 0
        if not source.programme_code or not option.programme_code:
            return 0

        if source.module_code.upper() != option.module_code.upper():
            return 0

        score = 3

        if source.campus_code.upper() == option.campus_code.upper():
            score +=2
        if source.year == option.year:
            score +=1

        overlaps = source.overlapping_availability(option)
        score += len(overlaps)

        return score

# Programme CRUD functionality
#=====================================================
    def get_programme(self, code):
        if not code:
            return None
        for program in self.programmes.values():
            if program.programme_code == code:
                return program
        return None

    def delete_programme(self, code):
        programme = self.get_programme(code)
        if not programme:
            return False, "ERROR: Programme not found", 0, 0

        student_count = 0
        request_count = 0

        if code in self.programmes:
            # Count them first while the dictionaries are intact
            for student in self.students.values():
                if student.programme_code == code:
                    student_count += 1
                    for request in self.requests.values():
                        if request.student_id == student.student_id:
                            request_count += 1

            # Now perform the safe deletions using list() snapshots
            for students in list(self.students.values()):
                if students.programme_code == code:
                    for requests in list(self.requests.values()):
                        if requests.student_id == students.student_id:
                            del self.requests[requests.request_id]
                    del self.students[students.student_id]
            del self.programmes[code]

        self.store.requests_save(self.requests)
        self.store.save_students(self.students)
        self.store.programme_save(self.programmes)

        # Return the counts back to the UI
        return True, student_count, request_count

    def get_module(self, code):
        for programme in list(self.programmes.values()):
            programme_modules = programme.modules
            for module in programme_modules:
                if code == module.module_code:
                    return module
        return None

    def programme_add_edit(self, is_edit, old_code, new_code, name, modules_list, campuses_list):
        if new_code in self.programmes:
            return False, f"Programme code '{new_code}' already exists."

        # Convert the updated module list to module objects
        compiled_modules = [Module(m['module_code'], m['name'], int(m['year'])) for m in modules_list]

        if is_edit:
            prog_obj = self.programmes.get(old_code)
            if not prog_obj:
                return False, "The programme being modified could not be found."

            self.linked_deletion_and_updates(old_code, new_code, compiled_modules, campuses_list)
            prog_obj.name = name
            prog_obj.programme_code = new_code
        else:
            self.programmes[new_code] = Programme(new_code, name, campuses_list, compiled_modules)

        # Save programmes, requests and students and update all modules and module codes
        self.store.programme_save(self.programmes)
        self.store.requests_save(self.requests)
        self.store.save_students(self.students)

        self.all_modules = [m for p in self.programmes.values() for m in p.modules]
        self.all_module_codes = [m.module_code for m in self.all_modules]

        return True, "Saved successfully"

    def linked_deletion_and_updates(self, old_code, new_code, compiled_modules, campuses_list):
        # Directly deletes and updates students and requests
        prog_obj = self.programmes.get(old_code)

        target_modules = {m.module_code.upper() for m in compiled_modules}
        target_campuses = {c.upper() for c in campuses_list}

        # Update programme
        prog_obj.modules = compiled_modules
        prog_obj.campus_codes = [c.upper() for c in campuses_list]

        if old_code != new_code:
            self.programmes[new_code] = self.programmes.pop(old_code)

        # Delete Students if their campus was deleted, otherwise update code link
        for s_id, student in list(self.students.items()):
            if student.programme_code == old_code:
                if student.campus_code.upper() not in target_campuses:
                    self.students.pop(s_id, None)
                else:
                    student.programme_code = new_code

        active_student_ids = {str(s_id) for s_id in self.students.keys()}

        # Delete Requests if student is deleted or if the requested module was deleted
        for r_id, request in list(self.requests.items()):
            if request.programme_code in (old_code, new_code):
                student_alive = str(request.student_id) in active_student_ids and str(r_id) in active_student_ids
                module_still_exists = request.module_code.upper() in target_modules

                if not student_alive or not module_still_exists:
                    self.requests.pop(r_id, None)
                else:
                    request.programme_code = new_code
