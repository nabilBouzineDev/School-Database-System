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

# Selecting Query
GET_LESSON_ID_BY_NAME = "SELECT id FROM lesson WHERE name = ?;"
GET_LESSON_NAME_BY_SID = """
SELECT lesson.name
FROM lesson 
JOIN student_lesson ON student_lesson.lesson_id = lesson.id 
WHERE student_lesson.student_id = ?; """
GET_STUDENT_INFOS = """
SELECT 
    student.id,
    student.first_name, 
    student.last_name, 
    student.age, 
    student.grade, 
    student.enrol_date,
    (
        SELECT GROUP_CONCAT(lesson.name, ",")
        FROM lesson
        JOIN student_lesson ON student_lesson.lesson_id = lesson.id
        WHERE student_lesson.student_id = student.id
    ) AS enrolled_lessons
FROM student
WHERE student.id = ?; """

# Check queries
IS_LESSON_EXIST = "SELECT EXISTS (SELECT 1 FROM lesson WHERE name = ?);"
IS_STUDENT_EXIST = "SELECT EXISTS (SELECT 1 FROM student WHERE id = ?);"
IS_STUDENT_LESSON_EXIST = "SELECT EXISTS (SELECT 1 FROM student_lesson WHERE student_id = ? AND lesson_id = ?);"

# Update queries
UPDATE_STUDENT_QUERY = "UPDATE student SET "
UPDATE_LESSON_QUERY = """
Update lesson 
SET name = ? 
WHERE id = (SELECT lesson_id FROM student_lesson WHERE student_id = ? AND lesson_id = ?); """

# DELETE queries
DELETE_FROM_STUDENT_LESSON_BY_LESSON_ID = "DELETE FROM student_lesson WHERE lesson_id = ?; "
DELETE_FROM_LESSON_BY_ID = "DELETE FROM lesson WHERE id = ?; "

DELETE_FROM_STUDENT_LESSON_BY_STUDENT_ID = "DELETE FROM student_lesson WHERE student_id = ?; "
DELETE_FROM_STUDENT_BY_ID = "DELETE FROM student WHERE id = ?; "


def connect():
    return sqlite3.connect('./db/data.db')


def create_tables(connection):
    create_table_queries = [CREATE_STUDENT_TABLE, CREATE_LESSON_TABLE, CREATE_STUDENT_LESSON_TABLE]
    with connection:
        for query in create_table_queries:
            connection.execute(query)


# Name: Functions with syntax like [add_field()]
# Goal: Add records to db.
def add_records(connection, student_detail, lessons_detail):
    add_student(connection, student_detail)

    for lesson_name in lessons_detail:
        add_lesson(connection, lesson_name)
        add_student_lesson(connection, student_detail[0], lesson_name)


def add_student(connection, student_detail):
    with connection:
        if not is_student_exist(connection, student_detail[0]):
            connection.execute(INSERT_STUDENT, (*student_detail,))


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


# Name: Functions with syntax like [update_field()]
# Goal: Update records in db.

# Construct dynamic query and update student records
def update_student(connection, student_id, updated_student_records):
    global UPDATE_STUDENT_QUERY
    with connection:
        if is_student_exist(connection, student_id):
            for field, value in updated_student_records.items():
                UPDATE_STUDENT_QUERY += f'{field} = "{value}", '

            # remove the last two characters
            UPDATE_STUDENT_QUERY = UPDATE_STUDENT_QUERY[:-2]
            UPDATE_STUDENT_QUERY += " WHERE id = ?"

        connection.execute(UPDATE_STUDENT_QUERY, (student_id,))


def update_lesson(connection, updated_lesson_records, student_id):
    with connection:
        for old_lesson, new_lesson in updated_lesson_records.items():
            # we don't have to update if the new lesson already exist
            if is_lesson_exist(connection, new_lesson):
                # delete old lesson
                lesson_id = get_lesson_id_by_name(connection, old_lesson)
                delete_lesson(connection, lesson_id)
            else:
                lesson_id = get_lesson_id_by_name(connection, old_lesson)
                connection.execute(UPDATE_LESSON_QUERY, (new_lesson, student_id, lesson_id))


# Name: Functions with syntax like [delete_field()]
# Goal: Delete records from db.
def delete_student(connection, student_id):
    with connection:
        # Start with student_lesson because it depends on student_id
        connection.execute(DELETE_FROM_STUDENT_LESSON_BY_STUDENT_ID, (student_id,))
        connection.execute(DELETE_FROM_STUDENT_BY_ID, (student_id,))


def delete_lesson(connection, lesson_id):
    with connection:
        # Start with student_lesson because it depends on lesson_id
        connection.execute(DELETE_FROM_STUDENT_LESSON_BY_LESSON_ID, (lesson_id,))
        connection.execute(DELETE_FROM_LESSON_BY_ID, (lesson_id,))


# Name: Functions with syntax like [get_record()]
# Goal: Fetch records from db.
def get_student_infos(connection, student_id):
    with connection:
        student_infos = connection.execute(GET_STUDENT_INFOS, (student_id,)).fetchall()
        return student_infos[0]


def get_lesson_id_by_name(connection, lesson_name):
    with connection:
        lesson_id = connection.execute(GET_LESSON_ID_BY_NAME, (lesson_name,)).fetchone()[0]
        return lesson_id


# show list of available lesson for each student
def get_lesson_names_by_student_id(connection, student_id):
    with connection:
        lesson_names = connection.execute(GET_LESSON_NAME_BY_SID, (student_id,)).fetchall()
        return lesson_names


# Name: Functions with syntax like [is_table_exist()]
# Goal: Check if record exist in this table.
def is_lesson_exist(connection, lesson_name):
    with connection:
        result = connection.execute(IS_LESSON_EXIST, (lesson_name,)).fetchone()[0]
        return True if result == 1 else False


def is_student_exist(connection, student_id):
    with connection:
        result = connection.execute(IS_STUDENT_EXIST, (student_id,)).fetchone()[0]
        return True if result == 1 else False


def is_student_lesson_exist(connection, student_id, lesson_id):
    with connection:
        result = connection.execute(IS_STUDENT_LESSON_EXIST, (student_id, lesson_id)).fetchone()[0]
        return True if result == 1 else False


def cleanup(connection):
    connection.commit()
    connection.close()
