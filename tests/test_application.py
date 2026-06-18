import unittest
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from application import StudyBuddyApp

TEST_DATA = "/tmp/test_data_app"


class TestAuthentication(unittest.TestCase):
    def setUp(self):
        if os.path.exists(TEST_DATA):
            shutil.rmtree(TEST_DATA)

        self.app = StudyBuddyApp.__new__(StudyBuddyApp)
        from data_storage import FileHandler

        self.app.store = FileHandler(TEST_DATA)
        self.app.store.set_required_campus_data()
        self.app.store.set_required_programme_data()
        self.app.store.set_required_admin_data()
        self.app.store.set_sample_students()
        self.app.store.set_sample_requests()
        self.app.programmes = self.app.store.load_programmes()
        self.app.campuses = self.app.store.load_campuses()
        self.app.students = self.app.store.load_students()
        self.app.requests = self.app.store.load_requests()
        self.app.admin = self.app.store.load_admin()
        self.app.all_modules = [m for p in self.app.programmes.values() for m in p.modules]
        self.app.all_module_codes = [m.module_code for m in self.app.all_modules]

    def tearDown(self):
        if os.path.exists(TEST_DATA):
            shutil.rmtree(TEST_DATA)
    def test_valid_login(self):
        ok, result = self.app.authenticate("1110000000", "Password123")
        self.assertTrue(ok)
        self.assertEqual(result.student_id, "1110000000")

    def test_wrong_password(self):
        ok, msg = self.app.authenticate("1110000000", "wrongpass")
        self.assertFalse(ok)
        self.assertIn("WARNING", msg)

    def test_unknown_student_id(self):
        ok, msg = self.app.authenticate("9999999999", "Belly1234")
        self.assertFalse(ok)

    def test_empty_password(self):
        ok, msg = self.app.authenticate("1110000000", "")
        self.assertFalse(ok)

    def test_valid_admin_login(self):
        ok, result = self.app.authenticate_admin("Admin", "1234")
        self.assertTrue(ok)

    def test_invalid_admin_login(self):
        ok, msg = self.app.authenticate_admin("Admin", "wrong")
        self.assertFalse(ok)


class TestRegisterValidation(unittest.TestCase):
    def setUp(self):
        if os.path.exists(TEST_DATA):
            shutil.rmtree(TEST_DATA)

        self.app = StudyBuddyApp.__new__(StudyBuddyApp)
        from data_storage import FileHandler

        self.app.store = FileHandler(TEST_DATA)
        self.app.store.set_required_campus_data()
        self.app.store.set_required_programme_data()
        self.app.store.set_required_admin_data()
        self.app.store.set_sample_students()
        self.app.store.set_sample_requests()
        self.app.programmes = self.app.store.load_programmes()
        self.app.campuses = self.app.store.load_campuses()
        self.app.students = self.app.store.load_students()
        self.app.requests = self.app.store.load_requests()
        self.app.admin = self.app.store.load_admin()
        self.app.all_modules = [m for p in self.app.programmes.values() for m in p.modules]
        self.app.all_module_codes = [m.module_code for m in self.app.all_modules]

    def tearDown(self):
        if os.path.exists(TEST_DATA):
            shutil.rmtree(TEST_DATA)

    def test_duplicate_id_rejected(self):
        ok, msg = self.app.check_register_credentials(
            "1110000000", "pass", "pass", "PCK", "BAENT", "1", "Name")
        self.assertFalse(ok)
        self.assertIn("already exists", msg)

    def test_id_not_10_digits(self):
        ok, msg = self.app.check_register_credentials(
            "123", "pass", "pass", "PCK", "BAENT", "1", "Name")
        self.assertFalse(ok)

    def test_passwords_not_matching(self):
        ok, msg = self.app.check_register_credentials(
            "2000000000", "pass1", "pass2", "PCK", "BAENT", "1", "Name")
        self.assertFalse(ok)

    def test_programme_not_at_campus(self):
        ok, msg = self.app.check_register_credentials(
            "2000000001", "pass", "pass", "NYC", "BANAV", "1", "Name")
        self.assertFalse(ok)
        self.assertIn("not available", msg)

    def test_valid_registration(self):
        ok, msg = self.app.check_register_credentials(
            "2000000002", "pass", "pass", "PCK", "BAENT", "1", "New Student")
        self.assertTrue(ok)
        self.assertIsNone(msg)


class TestRequestCRUD(unittest.TestCase):
    def setUp(self):
        if os.path.exists(TEST_DATA):
            shutil.rmtree(TEST_DATA)

        self.app = StudyBuddyApp.__new__(StudyBuddyApp)
        from data_storage import FileHandler

        self.app.store = FileHandler(TEST_DATA)
        self.app.store.set_required_campus_data()
        self.app.store.set_required_programme_data()
        self.app.store.set_required_admin_data()
        self.app.store.set_sample_students()
        self.app.store.set_sample_requests()
        self.app.programmes = self.app.store.load_programmes()
        self.app.campuses = self.app.store.load_campuses()
        self.app.students = self.app.store.load_students()
        self.app.requests = self.app.store.load_requests()
        self.app.admin = self.app.store.load_admin()
        self.app.all_modules = [m for p in self.app.programmes.values() for m in p.modules]
        self.app.all_module_codes = [m.module_code for m in self.app.all_modules]

    def tearDown(self):
        if os.path.exists(TEST_DATA):
            shutil.rmtree(TEST_DATA)

    def test_add_request_valid(self):
        ok, result = self.app.add_request(
            "1110000000", "BAENT", "PCK", "BENT31", [{"day": "Monday", "period": "Morning"}]
        )
        self.assertTrue(ok)
        self.assertEqual(result.module_code, "BENT31")

    def test_add_request_no_timeslots(self):
        ok, msg = self.app.add_request("1110000000", "BAENT", "PCK", "BENT31", [])
        self.assertFalse(ok)

    def test_add_request_wrong_module_for_year(self):
        # Craig is year 3; BSCS11 is year 1 CS — wrong programme + year
        ok, msg = self.app.add_request(
            "1110000000", "BAENT", "PCK", "BSCS11", [{"day": "Monday", "period": "Morning"}]
        )
        self.assertFalse(ok)

    def test_delete_own_request(self):
        ok, msg = self.app.delete_request(1, "1110000000")
        self.assertTrue(ok)
        self.assertIsNone(self.app.get_request_by_id(1))

    def test_delete_wrong_owner(self):
        ok, msg = self.app.delete_request(1, "1111000000")
        self.assertFalse(ok)
        self.assertIn("own", msg)

    def test_get_requests_for_student(self):
        reqs = self.app.get_requests_for_student("1110000000")
        self.assertTrue(len(reqs) > 0)
        for r in reqs:
            self.assertEqual(r.student_id, "1110000000")


class TestMatchingAlgorithm(unittest.TestCase):
    def setUp(self):
        if os.path.exists(TEST_DATA):
            shutil.rmtree(TEST_DATA)

        self.app = StudyBuddyApp.__new__(StudyBuddyApp)
        from data_storage import FileHandler

        self.app.store = FileHandler(TEST_DATA)
        self.app.store.set_required_campus_data()
        self.app.store.set_required_programme_data()
        self.app.store.set_required_admin_data()
        self.app.store.set_sample_students()
        self.app.store.set_sample_requests()
        self.app.programmes = self.app.store.load_programmes()
        self.app.campuses = self.app.store.load_campuses()
        self.app.students = self.app.store.load_students()
        self.app.requests = self.app.store.load_requests()
        self.app.admin = self.app.store.load_admin()
        self.app.all_modules = [m for p in self.app.programmes.values() for m in p.modules]
        self.app.all_module_codes = [m.module_code for m in self.app.all_modules]

    def tearDown(self):
        if os.path.exists(TEST_DATA):
            shutil.rmtree(TEST_DATA)

    def test_score_different_modules_returns_zero(self):
        from classes import Requests
        r1 = Requests(99, "A", "PCK", "BAENT", "3", "BENT31")
        r2 = Requests(100, "B", "PCK", "BAENT", "3", "BENT21")
        self.assertEqual(self.app.score_match(r1, r2), 0)

    def test_score_module_only_returns_3(self):
        from classes import Requests
        r1 = Requests(99, "A", "PCK", "BAENT", "3", "BENT31")
        r2 = Requests(100, "B", "NYC", "BAENT", "2", "BENT31")
        self.assertEqual(self.app.score_match(r1, r2), 3)

    def test_score_module_plus_campus_returns_5(self):
        from classes import Requests
        r1 = Requests(99, "A", "PCK", "BAENT", "3", "BENT31")
        r2 = Requests(100, "B", "PCK", "BAENT", "2", "BENT31")
        self.assertEqual(self.app.score_match(r1, r2), 5)

    def test_score_full_match_with_timeslot(self):
        from classes import Requests
        r1 = Requests(99, "A", "PCK", "BAENT", "3", "BENT31", [{"day": "Monday", "period": "Morning"}])
        r2 = Requests(100, "B", "PCK", "BAENT", "3", "BENT31", [{"day": "Monday", "period": "Morning"}])
        self.assertEqual(self.app.score_match(r1, r2), 7)

    def test_find_matches_excludes_own_requests(self):
        source = self.app.get_request_by_id(1)
        matches = self.app.find_matches(source)
        for m in matches:
            self.assertNotEqual(m["request"].student_id, source.student_id)

    def test_find_matches_sorted_by_score(self):
        source = self.app.get_request_by_id(1)
        matches = self.app.find_matches(source)
        scores = [m["score"] for m in matches]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_find_matches_only_same_module(self):
        source = self.app.get_request_by_id(1)
        matches = self.app.find_matches(source)
        for m in matches:
            self.assertEqual(m["request"].module_code, source.module_code)


class TestCampusDelete(unittest.TestCase):
    def setUp(self):
        if os.path.exists(TEST_DATA):
            shutil.rmtree(TEST_DATA)

        self.app = StudyBuddyApp.__new__(StudyBuddyApp)
        from data_storage import FileHandler

        self.app.store = FileHandler(TEST_DATA)
        self.app.store.set_required_campus_data()
        self.app.store.set_required_programme_data()
        self.app.store.set_required_admin_data()
        self.app.store.set_sample_students()
        self.app.store.set_sample_requests()
        self.app.programmes = self.app.store.load_programmes()
        self.app.campuses = self.app.store.load_campuses()
        self.app.students = self.app.store.load_students()
        self.app.requests = self.app.store.load_requests()
        self.app.admin = self.app.store.load_admin()
        self.app.all_modules = [m for p in self.app.programmes.values() for m in p.modules]
        self.app.all_module_codes = [m.module_code for m in self.app.all_modules]

    def tearDown(self):
        if os.path.exists(TEST_DATA):
            shutil.rmtree(TEST_DATA)

    def test_delete_campus_removes_campus(self):
        ok, s_count, r_count = self.app.delete_campus("PCK")
        self.assertTrue(ok)
        self.assertNotIn("PCK", self.app.campuses)

    def test_delete_campus_removes_students(self):
        pck_students_before = sum(1 for s in self.app.students.values() if s.campus_code == "PCK")
        self.app.delete_campus("PCK")
        pck_students_after = sum(1 for s in self.app.students.values() if s.campus_code == "PCK")
        self.assertEqual(pck_students_after, 0)
        self.assertGreater(pck_students_before, 0)

    def test_delete_campus_not_found(self):
        result = self.app.delete_campus("ZZZ")
        self.assertFalse(result[0])

    def test_delete_programme_removes_programme(self):
        ok, s_count, r_count = self.app.delete_programme("BAENT")
        self.assertTrue(ok)
        self.assertNotIn("BAENT", self.app.programmes)

    def test_delete_programme_removes_enrolled_students(self):
        baent_before = sum(1 for s in self.app.students.values() if s.programme_code == "BAENT")
        self.app.delete_programme("BAENT")
        baent_after = sum(1 for s in self.app.students.values() if s.programme_code == "BAENT")
        self.assertEqual(baent_after, 0)
        self.assertGreater(baent_before, 0)
