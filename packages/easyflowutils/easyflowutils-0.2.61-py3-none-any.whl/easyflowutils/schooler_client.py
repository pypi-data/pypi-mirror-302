from __future__ import annotations
from typing import Any, Optional, List
import requests
from pydantic import BaseModel, Field, EmailStr, HttpUrl


class AuthRequest(BaseModel):
    grant_type: str = "password"
    client_id: str
    client_secret: str
    user_id: EmailStr
    user_secret: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    created_at: str


class StudentData(BaseModel):
    name: str
    email: EmailStr
    password: str
    external_id: Optional[str] = None
    send_welcome_email_course: Optional[bool] = None


class CourseSchema(BaseModel):
    course_id: int = Field(alias='id')
    course_name: str
    course_link: HttpUrl
    course_status: str
    course_type: str
    course_language: str
    teacher_id: int
    teacher_name: str
    price: Optional[float] = None
    payment_gateway: Optional[str] = None
    school_id: Optional[int] = None
    school_name: Optional[str] = None
    student_time_limit_in_days: Optional[int] = None
    part_of_a_school: Optional[bool] = None
    course_description: Optional[str] = None
    course_audience: Optional[str] = None
    teacher_bio: Optional[str] = None


class SchoolSchema(BaseModel):
    id: int
    name: str
    principal_name: str
    status: str
    language: str
    link: HttpUrl
    payment_gateway: Optional[str] = None
    courses: List[CourseSchema]
    courses_count: int


class StudentSchema(BaseModel):
    student_id: int
    student_name: str
    student_email: EmailStr
    student_phone: Optional[str] = None
    student_join_date: str
    unique_link: HttpUrl
    status_in_course: str
    last_login_date: Optional[str] = None
    lessons_complete: int
    lesson_complete_precentage: int
    total_number_of_lessons: int


class SchoolerClient:
    BASE_URL = "https://api.schooler.biz"

    def __init__(self, client_id: str, client_secret: str, user_id: EmailStr, user_secret: str):
        self.auth_request = AuthRequest(
            client_id=client_id,
            client_secret=client_secret,
            user_id=user_id,
            user_secret=user_secret
        )
        self.access_token: Optional[str] = None
        self.headers = {"Content-Type": "application/json"}

    def authenticate(self) -> SchoolerClient:
        url = f"{self.BASE_URL}/oauth/token"
        response = requests.post(url, json=self.auth_request.dict())
        response.raise_for_status()
        auth_data = AuthResponse(**response.json())
        self.access_token = auth_data.access_token
        self.headers["Authorization"] = f"Bearer {self.access_token}"
        return self

    def get(self, endpoint: str, params: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        url = f"{self.BASE_URL}/api/v1/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params or {})
        response.raise_for_status()
        return response.json().get("data", {})

    def post(self, endpoint: str, data: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.BASE_URL}/api/v1/{endpoint}"
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def put(self, endpoint: str, data: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.BASE_URL}/api/v1/{endpoint}"
        response = requests.put(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    # Courses
    def get_courses(self) -> List[CourseSchema]:
        data = self.get("courses")
        return [CourseSchema(**course) for course in data]

    def get_course_details(self, course_id: int) -> CourseSchema:
        data = self.get(f"courses/{course_id}")
        return CourseSchema(**data)

    def get_course_lessons(self, course_id: int) -> dict[str, Any]:
        return self.get(f"courses/{course_id}/lessons")

    def get_course_students(self, course_id: int) -> List[StudentSchema]:
        data = self.get(f"courses/{course_id}/students")
        return [StudentSchema(**student) for student in data.get("students", [])]

    def enroll_students_in_course(self, course_id: int, students_data: List[StudentData]) -> dict[str, Any]:
        return self.post(f"courses/{course_id}/enroll_students", {"students_data": [s.dict() for s in students_data]})

    def update_students_in_course(self, course_id: int, students_data: List[dict[str, Any]]) -> dict[str, Any]:
        return self.put(f"courses/{course_id}/update_students", {"students_data": students_data})

    def delete_students_from_course(self, course_id: int, student_ids: List[int]) -> dict[str, Any]:
        return self.post(f"courses/{course_id}/delete_students", {"student_ids": student_ids})

    # Schools
    def get_schools(self) -> List[SchoolSchema]:
        data = self.get("schools")
        return [SchoolSchema(**school) for school in data]

    def get_school_details(self, school_id: int) -> SchoolSchema:
        data = self.get(f"schools/{school_id}")
        return SchoolSchema(**data)

    def get_school_students(self, school_id: int) -> List[StudentSchema]:
        data = self.get(f"schools/{school_id}/students")
        return [StudentSchema(**student) for student in data.get("students", [])]

    def enroll_students_in_school(self, school_id: int, students_data: List[StudentData]) -> dict[str, Any]:
        return self.post(f"schools/{school_id}/enroll_students", {"students_data": [s.dict() for s in students_data]})

    def update_students_in_school(self, school_id: int, students_data: List[dict[str, Any]]) -> dict[str, Any]:
        return self.put(f"schools/{school_id}/update_students", {"students_data": students_data})

    # Students
    def search_students(self, email: Optional[str] = None, student_id: Optional[int] = None,
                        phone: Optional[str] = None) -> List[StudentSchema]:
        params = {}
        if email:
            params["email"] = email
        if student_id:
            params["id"] = student_id
        if phone:
            params["phone"] = phone
        data = self.get("students/search", params=params)
        return [StudentSchema(**student) for student in data]
