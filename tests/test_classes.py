import unittest
from classes import Student, Campus, Module, Programme, Requests

class TestStudent(unittest.TestCase):
    def setUp(self):
        self.student = Student("1110000000", "Craig Grant", "BAENT", "PCK", "3", "Password123")

    def test_student_stored(self):
        self.assertEqual(self.student.student_id, "1110000000")
        self.assertEqual(self.student.name, "Craig Grant")
        self.assertEqual(self.student.programme_code, "BAENT")
        self.assertEqual(self.student.campus_code, "PCK")
        self.assertEqual(self.student.password, "Password123")

    def test_codes_uppercase(self):
        s1 = Student("1111000000", "Test", "baent", "pck", "1", "password123")
        self.assertEqual(s1.programme_code, "BAENT")
        self.assertEqual(s1.campus_code, "PCK")

    def test_to_dict_method(self):
        d = self.student.to_dict()
        for key in ["student_id", "name", "programme_code", "campus_code", "password"]:
            self.assertIn(key, d)

    def test_from_dict_method(self):
        s2 = Student.from_dict(self.student.to_dict())
        self.assertEqual(s2.student_id, "1110000000")
        self.assertEqual(s2.name, "Craig Grant")
        self.assertEqual(s2.programme_code, "BAENT")
        self.assertEqual(s2.campus_code, "PCK")
        self.assertEqual(s2.password, "Password123")

class TestCampus(unittest.TestCase):
    def setUp(self):
        self.campus = Campus("pck", "Peckham")

    def test_code_uppercase(self):
        self.assertEqual(self.campus.campus_code, "PCK")

    def test_to_dict_method(self):
        d = self.campus.to_dict()
        for key in ["campus_code", "name"]:
            self.assertIn(key, d)

    def test_from_dict_method(self):
        c1 = Campus.from_dict(self.campus.to_dict())
        self.assertEqual(c1.campus_code, "PCK")
        self.assertEqual(c1.name, "Peckham")

class TestModule(unittest.TestCase):
    def setUp(self):
        self.module = Module("bscs11", "Introduction to Programing", 1)

    def test_code_uppercase(self):
        self.assertEqual(self.module.module_code, "BSCS11")

    def test_to_dict_method(self):
        d = self.module.to_dict()
        for key in ["module_code", "name"]:
            self.assertIn(key, d)

    def test_from_dict_method(self):
        m = Module.from_dict(self.module.to_dict())
        self.assertEqual(m.module_code, "BSCS11")
        self.assertEqual(m.name, "Introduction to Programing")
        self.assertEqual(m.year, 1)

class TestProgramme(unittest.TestCase):
    def setUp(self):
        self.programme = Programme(
            "BSCSC",
            "BS Computing Science",
            ["PCK", "NYC"],
            [
                Module("BSCS11", "Test1", 1),
                Module("BSCS12", "Test2", 1),
                Module("BSCS13", "Test3", 2)
            ]
        )

    def test_code_uppercase(self):
        self.assertEqual(self.programme.programme_code, "BSCSC")

    def test_campus_codes_uppercase(self):
        self.assertIn("PCK", self.programme.campus_codes)

    def test_modules_for_year_1(self):
        self.assertEqual(len(self.programme.modules_for_year(1)), 2)

    def test_modules_for_year_2(self):
        self.assertEqual(len(self.programme.modules_for_year(2)), 1)

    def test_modules_for_year_empty(self):
        self.assertEqual(len(self.programme.modules_for_year(3)), 0)

    def test_to_dict_method(self):
        d = self.programme.to_dict()
        for key in ["programme_code", "name", "campus_codes", "modules"]:
            self.assertIn(key, d)

    def test_from_dict_method(self):
        d_dict = self.programme.to_dict()
        p1 = Programme.from_dict(d_dict)

        self.assertEqual(p1.programme_code, "BSCSC")
        self.assertEqual(p1.name, "BS Computing Science")
        self.assertEqual(p1.campus_codes, ["PCK", "NYC"])

        self.assertEqual(len(p1.modules), 3)
        self.assertEqual(p1.modules[0].module_code, "BSCS11")
        self.assertEqual(p1.modules[0].name, "Test1")
        self.assertEqual(p1.modules[0].year, 1)

class TestRequests(unittest.TestCase):
    def setUp(self):
        self.request = Requests(1,"1110000000","pck","baent", "3","bent31")

    def test_code_uppercase(self):
        self.assertEqual(self.request.campus_code, "PCK")
        self.assertEqual(self.request.module_code, "BENT31")
        self.assertEqual(self.request.programme_code, "BAENT")

    def test_availability_default_empty(self):
        self.assertEqual(self.request.availability, [])

    def test_add_availability(self):
        self.request.add_availability("Monday", "Morning")
        self.assertEqual(len(self.request.availability), 1)

    def test_add_duplicate(self):
        self.request.add_availability("Monday", "Morning")
        self.assertFalse(self.request.add_availability("Monday","Morning"))

    def test_add_invalid_day(self):
        self.assertFalse(self.request.add_availability("Sunday", "Morning"))

    def test_add_invalid_period(self):
        self.assertFalse(self.request.add_availability("Monday", "Night"))

    def test_remove_availability(self):
        self.request.add_availability("Monday", "Morning")
        self.request.remove_availability("Monday", "Morning")

        self.assertEqual(self.request.availability, [])

    def test_overlapping(self):
        self.request.add_availability("Monday", "Morning")
        other = Requests(2, "1111000000","PCK","BAENT","3","BENT31")

        other.add_availability("Monday", "Morning")
        other.add_availability("Friday", "Evening")

        overlap = self.request.overlapping_availability(other)

        self.assertEqual(len(overlap), 1)
        self.assertEqual(overlap[0]["day"], "Monday")

    def test_to_dict_method(self):
        d = self.request.to_dict()

        for key in ["request_id","student_id","campus_code","programme_code","year", "module_code"]:
            self.assertIn(key, d)

    def test_from_dict_method(self):
        d_dict = self.request.to_dict()
        r1 = Requests.from_dict(d_dict)

        self.assertEqual(r1.request_id, 1)
        self.assertEqual(r1.student_id, "1110000000")
        self.assertEqual(r1.campus_code, "PCK")
        self.assertEqual(r1.programme_code, "BAENT")
        self.assertEqual(r1.year, "3")
        self.assertEqual(r1.module_code, "BENT31")


