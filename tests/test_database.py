import sqlite3
import unittest

from src import database as db


class TestDatabase(unittest.TestCase):

    # Setup database for testing
    def setUp(self):
        self.connection = sqlite3.connect(':memory:')
        db.create_tables(self.connection)

    # Tear down database, called after each test method
    # Goal: clean up operation
    def tearDown(self):
        self.connection.close()

    # Test adding to db operation
    def test_add_student(self):
        fake_student_detail = [1, "Ali", "Soe", 20, "uni", "01-09-2023"]

        db.add_student(self.connection, fake_student_detail)

        is_fake_student_exist = db.is_student_exist(self.connection, 1)
        self.assertTrue(is_fake_student_exist)

    def test_add_lesson(self):
        fake_enrolled_lesson = "Math"

        db.add_lesson(self.connection, fake_enrolled_lesson)

        is_fake_enrolled_lesson_exist = db.is_lesson_exist(self.connection, fake_enrolled_lesson)
        self.assertTrue(is_fake_enrolled_lesson_exist)

    def test_add_student_lesson(self):
        fake_student_detail = [1, "Ali", "Soe", 20, "uni", "01-09-2023"]
        fake_enrolled_lesson = "Math"

        db.add_student(self.connection, fake_student_detail)
        db.add_lesson(self.connection, fake_enrolled_lesson)
        db.add_student_lesson(self.connection, fake_student_detail[0], fake_enrolled_lesson)

        get_lesson_id = db.get_lesson_id_by_name(self.connection, fake_enrolled_lesson)
        result = db.is_student_lesson_exist(self.connection, fake_student_detail[0], get_lesson_id)

        self.assertTrue(result)

    # Test updating in db operation
    def test_update_student(self):
        fake_student_detail = [1, "Ali", "Soe", 20, "uni", "01-09-2023"]

        db.add_student(self.connection, fake_student_detail)
        update_student_records = {'first_name': 'Ahmed', 'age': 19}
        db.update_student(self.connection, fake_student_detail[0], update_student_records)

        # get student info after updating
        update_fake_student_detail = db.get_student_infos(self.connection, fake_student_detail[0])

        self.assertEqual(update_fake_student_detail[1], 'Ahmed')
        self.assertEqual(update_fake_student_detail[3], 19)

    def test_update_lesson(self):
        fake_student_detail = [1, "Ali", "Soe", 20, "uni", "01-09-2023"]
        fake_lesson_name = 'Math'
        fake_updated_lesson_name = 'Advanced Math'

        db.add_student(self.connection, fake_student_detail)
        db.add_lesson(self.connection, fake_lesson_name)
        db.add_student_lesson(self.connection, fake_student_detail[0], fake_lesson_name)

        updated_lesson_records = {fake_lesson_name: fake_updated_lesson_name}
        db.update_lesson(self.connection, updated_lesson_records, fake_student_detail[0])

        # find lesson id by name
        is_fake_updated_lesson_name_exist = db.is_lesson_exist(self.connection, fake_updated_lesson_name)
        self.assertTrue(is_fake_updated_lesson_name_exist)

    # Test deleting from db operation
    def test_delete_student(self):
        fake_student_detail = [1, "Ali", "Soe", 20, "uni", "01-09-2023"]

        db.add_student(self.connection, fake_student_detail)
        db.delete_student(self.connection, fake_student_detail[0])

        is_fake_student_exist = db.is_student_exist(self.connection, 1)
        self.assertFalse(is_fake_student_exist)

    def test_delete_lesson(self):
        fake_lesson_name = 'MATH'

        db.add_lesson(self.connection, fake_lesson_name)

        fake_lesson_id = db.get_lesson_id_by_name(self.connection, fake_lesson_name)
        db.delete_lesson(self.connection, fake_lesson_id)

        is_fake_lesson_exist = db.is_lesson_exist(self.connection, fake_lesson_name)
        self.assertFalse(is_fake_lesson_exist)

    # Test get information from db operation
    def test_get_student_infos(self):
        fake_student_detail = [1, "Ali", "Soe", 20, "uni", "01-09-2023"]
        fake_enrolled_lesson = "Math"

        db.add_student(self.connection, fake_student_detail)
        db.add_lesson(self.connection, fake_enrolled_lesson)
        db.add_student_lesson(self.connection, fake_student_detail[0], fake_enrolled_lesson)

        get_student_infos = db.get_student_infos(self.connection, fake_student_detail[0])
        self.assertEqual(get_student_infos[1], "Ali")
        self.assertEqual(get_student_infos[2], "Soe")
        self.assertEqual(get_student_infos[3], 20)
        self.assertEqual(get_student_infos[4], "uni")
        self.assertEqual(get_student_infos[5], "01-09-2023")
        self.assertEqual(get_student_infos[6], "Math")

    def test_get_lesson_id_by_name(self):
        fake_lesson_name = "Math"

        db.add_lesson(self.connection, fake_lesson_name)

        fake_lesson_id = db.get_lesson_id_by_name(self.connection, fake_lesson_name)
        self.assertIsNotNone(fake_lesson_id)

    def test_get_lesson_names_by_student_id(self):
        fake_student_detail = [1, "Ali", "Soe", 20, "uni", "01-09-2023"]
        fake_lesson_name = "Math"

        db.add_student(self.connection, fake_student_detail)
        db.add_lesson(self.connection, fake_lesson_name)
        db.add_student_lesson(self.connection, fake_student_detail[0], fake_lesson_name)

        fake_lesson_name_by_sid = db.get_lesson_names_by_student_id(self.connection, fake_student_detail[0])
        self.assertIn((fake_lesson_name,), fake_lesson_name_by_sid)  # Check if lesson name in a list of lessons


if __name__ == '__main__':
    unittest.main()
