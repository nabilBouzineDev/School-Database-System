# Understand the Problem
## Problem Overview

> **_Problem Definition_**: School Management System for Lessons and Student Management

> **_Current Situation_**:
Schools currently manage lessons and student enrollment manually, using paper-based systems or spreadsheets. This process is time-consuming, error-prone, and inefficient.

> **_Desired Situation_**:
The school needs a database based system to manage lessons and student enrollment efficiently. The system should allow users to view student information, manage enrolled lessons, add, update, and delete student records, and view student information.

## User Stories

<img width="5251" alt="user_stories" src="https://github.com/nabilBouzineDev/School-Database-System/assets/139881384/2c2b9bca-dc4c-43db-a1ec-c38a249a2802">

# Design Solution
## Database Design

<table>
    <tr>
        <td style="text-align:center">Schema Conceptual & Logical Design</td>
        <td style="text-align:center">Schema Markup</td>
    </tr>
    <tr>
        <td>
            <img width="2592" alt="schema" src="https://github.com/nabilBouzineDev/School-Database-System/assets/139881384/17b001a2-bb54-412b-8258-a42370e645ea">
        </td>
        <td>
            <pre>
<details>
<summary>show schema code</summary>
  
```sql
student
---
id PK int
first_name string
last_name string
age int
grade string
enrol_date datetime default=GETUTCDATE()

student_lesson
---
id pk
student_id int FK >- student.id
lesson_id int FK >- lesson.id

lesson
---
id PK int
name string
```
</details>
            </pre>
        </td>
    </tr>
</table>
  
## Algorithm Design

>> [![Algorithm](https://img.shields.io/badge/Feature_01:_Algorithm_&_Pseuodocode_➜-black.svg?logo=thealgorithms&logoColor=fff&style=plastic)](https://github.com/nabilBouzineDev/School-Database-System/tree/main/modeling/feature_one#0)
>
> <img width="6919" alt="f1_flowchart" src="https://github.com/nabilBouzineDev/School-Database-System/assets/139881384/42259a4e-9c9b-4386-a8ba-071ac8408dbf">
---
>> [![Algorithm](https://img.shields.io/badge/Feature_02:_Algorithm_&_Pseuodocode_➜-black.svg?logo=thealgorithms&logoColor=fff&style=plastic)](https://github.com/nabilBouzineDev/School-Database-System/tree/main/modeling/feature_two#0)
>
> <img width="8418" alt="f2_flowchart" src="https://github.com/nabilBouzineDev/School-Database-System/assets/139881384/1295a2af-3114-4791-afbb-de120ddbcac0">
---
>> [![Algorithm](https://img.shields.io/badge/Feature_03:_Algorithm_&_Pseuodocode_➜-black.svg?logo=thealgorithms&logoColor=fff&style=plastic)](https://github.com/nabilBouzineDev/School-Database-System/tree/main/modeling/feature_three#0)
>
> <img width="5254" alt="f3_flowchart" src="https://github.com/nabilBouzineDev/School-Database-System/assets/139881384/8c8dca06-8a98-48ea-a779-b17ae1af3cd1">
---
>> [![Algorithm](https://img.shields.io/badge/Feature_04:_Algorithm_&_Pseuodocode_➜-black.svg?logo=thealgorithms&logoColor=fff&style=plastic)](https://github.com/nabilBouzineDev/School-Database-System/tree/main/modeling/feature_four#0)
>
> <img width="5242" alt="f4_flowchart" src="https://github.com/nabilBouzineDev/School-Database-System/assets/139881384/acbc099e-9748-483c-84d3-6dd69e411f32">
---

# Implement Solution
## Project File Structure

```md
SchoolDbSystem/
│
├── modeling/
│   ├── feature_one/
│   │   ├── add_new_student.pseudo
│   │   └── add_new_student.txt
│   ├── feature_two/
│   │   ├── update_old_student.pseudo
│   │   └── update_old_student.txt
│   ├── feature_three/
│   │   ├── delete_student.pseudo
│   │   └── delete_student.txt
│   ├── feature_four/
│   │   ├── select_student_info.pseudo
│   │   └── select_student_info.txt
│
├── src/
│   ├── db/
│   │   └── data.db
│   ├── utils/
│   │   ├── util_display.py
│   │   └── util_validations.py
│   ├── database.py
│   └── app.py
│
├── tests/
│   └── test_database.py
│
├── readme.md
└── .gitignore
```

## Demo
>>  ***Feature 01: Add Student***
>
> ![feature_01](https://github.com/nabilBouzineDev/School-Database-System/assets/139881384/2582644f-ea17-4d16-ac48-c785ba3d9e16)

---
>>  ***Feature 02: Update Student***
>
> ![feature_02](https://github.com/nabilBouzineDev/School-Database-System/assets/139881384/baee8a81-7270-4aef-bff7-8139834f0a34)

---
>>  ***Feature 03-04: Delete-Display Student***
>
> ![feature_03_04](https://github.com/nabilBouzineDev/School-Database-System/assets/139881384/559ef39f-8309-41f7-8ca5-cb06fd4fb7aa)

---

# Disclaimer

- The project is designed to practice **software engineering** principles and best practices.
- You may found differences between the design and implementation due to language limitations and other factors.

# Links

_**Any Question? Contact Me:**_

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/nabilbdev)
[![github](https://img.shields.io/badge/github-000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/nabilBouzineDev)
