""" [database.py]: this file where the program interact with the database """

import sqlite3

# Create queries
CREATE_STUDENT_TABLE = """
CREATE TABLE IF NOT EXISTS student 
(
id INTEGER PRIMARY KEY,
first_name TEXT,
last_name TEXT,
age INTEGER, 
grade TEXT,
enrol_date datetime DEFAULT NULL
); """

CREATE_LESSON_TABLE = "CREATE TABLE IF NOT EXISTS lesson (id INTEGER PRIMARY KEY, name TEXT);"

CREATE_STUDENT_LESSON_TABLE = """
CREATE TABLE IF NOT EXISTS student_lesson
(
id INTEGER PRIMARY KEY,
student_id INTEGER,
lesson_id INTEGER,
FOREIGN KEY (student_id) REFERENCES student(id),
FOREIGN KEY (lesson_id) REFERENCES lesson(id)
); """

# Insert queries
INSERT_STUDENT = \
    "INSERT OR IGNORE INTO student (id, first_name, last_name, age, grade, enrol_date) VALUES (?, ?, ?, ?, ?, ?);"
INSERT_LESSON = "INSERT INTO lesson (name) VALUES(?);"
INSERT_STUDENT_LESSON = "INSERT OR REPLACE INTO student_lesson (student_id, lesson_id) VALUES (?, ?);"

# Get specific info queries
GET_LESSON_ID_BY_NAME = "SELECT id FROM lesson WHERE name = ?;"

# Check queries
IS_LESSON_EXIST = "SELECT EXISTS (SELECT 1 FROM lesson WHERE name = ?);"
IS_STUDENT_EXIST = "SELECT EXISTS (SELECT 1 FROM student WHERE id = ?);"
IS_STUDENT_LESSON_EXIST = "SELECT EXISTS (SELECT 1 FROM student_lesson WHERE student_id = ? AND lesson_id = ?);"


def connect():
    return sqlite3.connect('./db/data.db')


def create_tables(connection):
    with connection:
        connection.execute(CREATE_STUDENT_TABLE)
        connection.execute(CREATE_LESSON_TABLE)
        connection.execute(CREATE_STUDENT_LESSON_TABLE)


def add_records(connection, student_detail, lessons_detail):
    for student_id, first_name, last_name, age, grade, enrol_date in [student_detail]:
        add_student(connection, student_id, first_name, last_name, age, grade, enrol_date)

    for lesson_name in lessons_detail:
        add_lesson(connection, lesson_name)
        add_student_lesson(connection, student_detail[0], lesson_name)


def add_student(connection, student_id, first_name, last_name, age, grade, enrol_date):
    with connection:
        if not is_student_exist(connection, student_id):
            connection.execute(INSERT_STUDENT, (student_id, first_name, last_name, age, grade, enrol_date))


def add_lesson(connection, lesson_name):
    with connection:
        if not is_lesson_exist(connection, lesson_name):
            connection.execute(INSERT_LESSON, (lesson_name,))


# student_lesson is a [Joining table] used to map each student with his lessons
def add_student_lesson(connection, student_id, lesson_name):
    with connection:
        lesson_id = get_lesson_id_by_name(connection, lesson_name)
        if not is_student_lesson_exist(connection, student_id, lesson_id):
            connection.execute(INSERT_STUDENT_LESSON, (student_id, lesson_id))


def get_lesson_id_by_name(connection, lesson_name):
    lesson_id = connection.execute(GET_LESSON_ID_BY_NAME, (lesson_name,)).fetchone()[0]
    return lesson_id


# Name: Functions with syntax like [is_table_exist()]
# Goal: Used to avoid inserting duplicated data.
def is_lesson_exist(connection, lesson_name):
    result = connection.execute(IS_LESSON_EXIST, (lesson_name,)).fetchone()[0]
    return True if result == 1 else False


def is_student_exist(connection, student_id):
    result = connection.execute(IS_STUDENT_EXIST, (student_id,)).fetchone()[0]
    return True if result == 1 else False


def is_student_lesson_exist(connection, student_id, lesson_id):
    result = connection.execute(IS_STUDENT_LESSON_EXIST, (student_id, lesson_id)).fetchone()[0]
    return True if result == 1 else False


def cleanup(connection):
    connection.commit()
    connection.close()