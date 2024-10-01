from sqlalchemy import ARRAY, Column, Date, Integer, Numeric, String, Boolean, DateTime, ForeignKey, LargeBinary, Text, Enum, UUID
from sqlalchemy.orm import relationship
from .database import Base
import datetime
import enum

class UserRole(enum.Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    ALUMINI = "alumini"
    STUDENT = "student"
    FACULTY = "faculty"

class UserMaster(Base):
    __tablename__ = 'user_master'

    id = Column(UUID, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.STUDENT)

class StudentMaster(Base):
    __tablename__ = 'student_master'

    id = Column(UUID, primary_key=True)
    roll_number = Column(String, index=True, nullable=False)
    enrollment_number = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    department = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    year = Column(Integer, nullable=False)
    admission_year = Column(Integer, nullable=False)
    course_name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    division = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    phone = Column(String, nullable=False)
    blood_group = Column(String, nullable=False)
    secondary_phone = Column(String, nullable=True)
    gender = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    guardian_type = Column(String, nullable=False)
    guardian_name = Column(String, nullable=False)
    guardian_phone = Column(String, nullable=False)
    attendance_sheet = Column(ARRAY(String), nullable=True)

    user_id = Column(UUID, ForeignKey('user_master.id'), nullable=False)

class AdminMaster(Base):
    __tablename__ = 'admin_master'

    id = Column(UUID, primary_key=True)
    name = Column(String, nullable=False)
    about = Column(Text, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=False)

class FacultyMaster(Base):
    __tablename__ = 'faculty_master'

    id = Column(UUID, primary_key=True)  
    name = Column(String, nullable=False)
    qualification = Column(String, nullable=False)
    department = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    phone = Column(String)

    user_id = Column(UUID, ForeignKey('user_master.id'), nullable=False)

class AlumniInfo(Base):
    __tablename__ = 'alumni_info'

    roll_number = Column(String, primary_key=True, index=True)
    enrollment_number = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    department = Column(String, nullable=False)
    graduation_year = Column(Integer, nullable=False)
    current_company = Column(String, nullable=True)
    about = Column(Text, nullable=True)
    specialization = Column(String, nullable=False)
    division = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    phone = Column(String, nullable=False)
    blood_group = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    dob = Column(Date, nullable=False)

    user_id = Column(UUID, ForeignKey('user_master.id'), nullable=False)

class AttendanceMaster(Base):
    __tablename__ = 'attendance'

    sheet_id = Column(UUID, primary_key=True)
    department = Column(String)
    year = Column(Integer)
    specialization = Column(String)
    division = Column(String)
    faculty_id = Column(UUID, ForeignKey('faculty_master.id'))  
    subject_name = Column(String)
    faculty_name = Column(String)
    sheet_link = Column(String)

class ClassroomMaster(Base):
    __tablename__ = 'classroom_master'

    classroom_id = Column(UUID, primary_key=True, index=True) 
    total_credits = Column(Integer)
    faculty_id = Column(UUID, ForeignKey('faculty_master.id')) 
    faculty_name = Column(String)
    department = Column(String)
    year = Column(Integer)
    specialization = Column(String)
    division = Column(String)
    students_count = Column(Integer)
    subject_id = Column(Integer)
    subject_name = Column(String)
    creation_datetime = Column(DateTime)
    expiry_datetime = Column(DateTime)

class ClassPost(Base):
    __tablename__ = 'class_post'

    post_id = Column(Integer, primary_key=True, index=True)
    post_media = Column(String)
    submission_media = Column(String)
    title = Column(String)
    body = Column(Text)
    class_id = Column(Integer, ForeignKey('classroom_master.id'))
    creation_datetime = Column(DateTime)
    deadline_datetime = Column(DateTime)
    total_marks = Column(Integer)

class AssignmentMaster(Base):
    __tablename__ = 'assignment_master'
    id = Column(UUID, primary_key=True)
    creation_datetime = Column(DateTime)
    deadline_datetime = Column(DateTime)
    total_marks = Column(Integer)
    faculty_id = Column(UUID, ForeignKey('faculty_master.id'))  
    faculty_name = Column(String)
    subject_id = Column(Integer)
    subject_name = Column(String)
    title = Column(String)
    body = Column(Text)
    media = Column(String)

class Calendar(Base):
    __tablename__ = 'calendar'  
    id = Column(UUID, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    event = Column(String, nullable=False)
    user_id = Column(UUID, ForeignKey('user_master.id'), nullable=True)

