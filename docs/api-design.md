# StudySync API Design

## Project Overview

StudySync is an AI-powered student study and performance platform.
It helps students manage subjects, study tasks, study sessions,
and academic performance.

## 1. Entities

### User

Represents a student using the StudySync platform.

Fields:

- id
- name
- email
- password

### Subject

Represents an academic subject belonging to a user.

Fields:

- id
- name
- description
- user_id

### Task

Represents a study task associated with a subject.

Fields:

- id
- title
- description
- due_date
- status
- subject_id

### Performance

Represents a student's academic performance for a subject.

Fields:

- id
- subject_id
- score
- max_score
- exam_type

### StudySession

Represents a study session completed for a subject.

Fields:

- id
- subject_id
- duration_minutes
- session_date

## 2. Entity Relationships

- One User can have many Subjects.
- One Subject can have many Tasks.
- One Subject can have many Performance records.
- One Subject can have many StudySessions.

Relationship summary:

- User 1 → many Subjects
- Subject 1 → many Tasks
- Subject 1 → many Performance records
- Subject 1 → many StudySessions
## 3. REST Endpoint Plan

### User Endpoints

| Method | Endpoint | Purpose | Success | Possible Errors |
|---|---|---|---|---|
| POST | `/users` | Create a new user | 201 Created | 400, 409, 422 |
| GET | `/users/{user_id}` | Get a user by ID | 200 OK | 404 Not Found |

### Subject Endpoints

| Method | Endpoint | Purpose | Success | Possible Errors |
|---|---|---|---|---|
| POST | `/subjects` | Create a subject | 201 Created | 422, 404 |
| GET | `/subjects` | Get all subjects | 200 OK | 404 |
| GET | `/subjects/{subject_id}` | Get a subject by ID | 200 OK | 404 Not Found |
| PUT | `/subjects/{subject_id}` | Update a subject | 200 OK | 404, 422 |
| DELETE | `/subjects/{subject_id}` | Delete a subject | 204 No Content | 404 Not Found |

### Task Endpoints

| Method | Endpoint | Purpose | Success | Possible Errors |
|---|---|---|---|---|
| POST | `/tasks` | Create a study task | 201 Created | 404, 422 |
| GET | `/tasks` | Get all tasks | 200 OK | 404 |
| GET | `/tasks/{task_id}` | Get a task by ID | 200 OK | 404 Not Found |
| PUT | `/tasks/{task_id}` | Update a task | 200 OK | 404, 422 |
| DELETE | `/tasks/{task_id}` | Delete a task | 204 No Content | 404 Not Found |

### Performance Endpoints

| Method | Endpoint | Purpose | Success | Possible Errors |
|---|---|---|---|---|
| POST | `/performance` | Record performance | 201 Created | 404, 422 |
| GET | `/performance/{performance_id}` | Get performance by ID | 200 OK | 404 Not Found |

### Study Session Endpoints

| Method | Endpoint | Purpose | Success | Possible Errors |
|---|---|---|---|---|
| POST | `/study-sessions` | Record a study session | 201 Created | 404, 422 |
| GET | `/study-sessions` | Get study sessions | 200 OK | 404 |
| GET | `/study-sessions/{session_id}` | Get a study session by ID | 200 OK | 404 Not Found |
## 4. Error Handling

The API will use standard HTTP status codes.

| Status Code | Meaning |
|---|---|
| 200 | Request completed successfully |
| 201 | Resource successfully created |
| 204 | Resource successfully deleted |
| 400 | Bad request |
| 404 | Requested resource does not exist |
| 409 | Conflict with existing resource |
| 422 | Request validation failed |