from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    TIMESTAMP,
    ForeignKey,
    func,
    Text,
    Boolean,
    Date,Numeric,
    Float,BigInteger ,
    UniqueConstraint,CheckConstraint
)
from sqlalchemy.orm import relationship
from database.database import Base
from enum import Enum as PyEnum
from sqlalchemy import Enum
from datetime import date as DateType, datetime


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(100), nullable=False)
    org_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    created_at = Column(TIMESTAMP(), server_default=func.now())
    organization = relationship("Organization", back_populates="roles")
    users = relationship("User", back_populates="role")
    # Check Constraint for allowed roles
    __table_args__ = (
        CheckConstraint(
            "role_name IN ('Owner', 'Admin', 'HR', 'Manager', 'Employee')",
            name="check_valid_role_name"
        ),
    )

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    work_email = Column(String(255), nullable=False, unique=True, index=True)
    username = Column(String(100), nullable=False, unique=True)
    title = Column(String(100), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    org_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    department = Column(String(100), nullable=True)
    created_at = Column(TIMESTAMP(), server_default=func.now())
    updated_at = Column(TIMESTAMP(), server_default=func.now(), onupdate=func.now())
    session_id = Column(String(255), nullable=True)  # for storing session info

    organization = relationship("Organization", back_populates="users")
    role = relationship("Role", back_populates="users")
    manager = relationship("User", remote_side=[id])
    details = relationship("UserDetails", back_populates="user", uselist=False)
    educations = relationship(
        "Education",
        back_populates="user",
        cascade="all,delete-orphan",
    )
    leaves = relationship(
        "Leave",
        back_populates="user",
        cascade="all,delete-orphan",
    )

class UserDetails(Base):
    __tablename__ = "users_details"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key → User
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)

    personal_email = Column(String(255), nullable=True)
    dob = Column(Date, nullable=True)
    pwd_flag = Column(Boolean, default=False)
    maritalstatus_flag = Column(Boolean, default=False)
    gender = Column(String(50), nullable=True)
    nationality = Column(String(100), nullable=True)
    address = Column(String(255), nullable=True)
    blood_group = Column(String(10), nullable=True)

    created_at = Column(TIMESTAMP(), server_default=func.now(), nullable=False)
    updated_at = Column(
        TIMESTAMP(),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user = relationship("User", back_populates="details")

class Organization(Base):
    __tablename__ = "organization"

    id = Column(Integer, primary_key=True, index=True)
    org_prefix = Column(String(50), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    logo_url = Column(String(500), nullable=True)
    industry = Column(String(255), nullable=True)
    company_size = Column(Integer, nullable=True)
    website = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP(), server_default=func.now(), nullable=False)
    updated_at = Column(
        TIMESTAMP(),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    users = relationship("User", back_populates="organization", cascade="all,delete")
    roles = relationship("Role", back_populates="organization", cascade="all,delete")



class EducationLevel(str, PyEnum):
    UNDERGRADUATE = "undergraduate"
    POSTGRADUATE = "postgraduate"
    OTHER = "other"   # for diploma etc.

class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    level = Column( Enum(EducationLevel), nullable=False)
    institution = Column(String(255), nullable=False)
    degree = Column(String(255), nullable=False)          # e.g. "B.Tech", "MBA"
    field_of_study = Column(String(255), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    grade = Column(String(50), nullable=True)
    created_at = Column(TIMESTAMP(), server_default=func.now(), nullable=False)


    user = relationship("User", back_populates="educations")
    # Optional: one record per level per user (1 UG, 1 PG, 1 OTHER)
    # __table_args__ = (
    #     UniqueConstraint("user_id", "level", name="uq_user_level"),
    # )



class Achievement(Base):
    __tablename__ = "achievements"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    awarded_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    awarded_date = Column(Date, nullable=True)
    created_at = Column(TIMESTAMP(), server_default=func.now(), nullable=False)

class Certification(Base):
    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String(200), nullable=False)
    provider = Column(String(200), nullable=False)
    status = Column(String, nullable=False)  # upcoming, completed,expired
    completed_date = Column(Date, nullable=True)
    expiry_date = Column(Date, nullable=True)
    planned_date = Column(Date, nullable=True)
    created_at = Column(Date, server_default=func.current_date(), nullable=False)


class LeaveStatus(str, PyEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"



class Leave(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    leave_name = Column(Text, nullable=True)
    max_days_per_year = Column(Integer, nullable=True)
    is_paid = Column(Boolean, default=True)
    allow_half_day = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(), server_default=func.now(), nullable=False)
    updated_at = Column(
        TIMESTAMP(),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user = relationship("User", back_populates="leaves")


class LeaveRequests(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    leave_id= Column(Integer,ForeignKey("leaves.id"),nullable=True)
    leave_type = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    total_days = Column(Integer, nullable=False)
    reason = Column(Text, nullable=True)
    status = Column(Enum(LeaveStatus), default="pending")  # pending, approved, rejected
    applied_on = Column(TIMESTAMP, server_default=func.now())
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    approved_on = Column(TIMESTAMP, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    #half day storage
    half_day = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(), server_default=func.now())
    updated_at = Column(TIMESTAMP(),server_default=func.now(),onupdate=func.now())

        # half_day_type = Column(String, nullable=True)  # 'first_half' or 'second_half'


class Timesheet(Base):
    __tablename__ = "timesheets"

    timesheet_id = Column(Integer, primary_key=True, index=True)
    user_project_mapping_id = Column(
        Integer,
        ForeignKey("user_project_mapping.id"),
        nullable=False
    )
    work_date = Column(DateTime, nullable=False) #dynamic date
    hours_worked = Column(Float,nullable=False)
    description = Column(String(500))
    status = Column(String(50), default="Pending")#draft,submitted,approve,reject
    submitted_at = Column(DateTime, default=datetime.now)
    approved_by = Column(Integer, ForeignKey("users.id"),nullable=True)
    approved_at = Column(DateTime,nullable=True)
    

class Project(Base):
    __tablename__ = "projects"

    project_id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    org_id = Column(Integer,  nullable=False)
    project_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    project_type= Column(String(100), nullable=True)
    billable_flag= Column(Boolean, default=False)
    internal_project_flag= Column(Boolean, default=False)
    client_id= Column(Integer, nullable=True)
    org_id= Column(Integer, ForeignKey("organization.id"), nullable=False)
    status = Column(String(50), default="Active")
    created_at = Column(TIMESTAMP(), server_default=func.now())
    updated_at = Column(
        TIMESTAMP(),
        server_default=func.now(),
        onupdate=func.now(),
    )
    started_at= Column(Date, nullable=True)
    end_at= Column(Date, nullable=True)
    
  

class UserProjectMapping(Base):
    __tablename__ = "user_project_mapping"

    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    project_id = Column(BigInteger, ForeignKey("projects.project_id"), nullable=False)
    role = Column(String(50), nullable=False)
    billable = Column(Boolean, nullable=False, default=False)
    allocation_percent = Column(
        Numeric(5, 2),
        nullable=False
    )
    start_date = Column(Date, nullable=False, server_default=func.current_date())
    end_date = Column(Date, nullable=True)
    created_at = Column(
        TIMESTAMP,
        server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "allocation_percent >= 0 AND allocation_percent <= 100",
            name="check_allocation_percent_range"
        ),
    )

class PerformanceReview(Base):
    __tablename__ = "performance_reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    review_period = Column(String, nullable=False)
    overall_rating = Column(Float, nullable=False)
    strengths = Column(Text)
    improvements = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Goals(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    goal_type = Column(String(50), nullable=True)  # e.g. "Individual", "Team", "Organizational"
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    progress=Column(Integer, default=0) # 0 to 100
    #target_date = Column(Date, nullable=True)
    status = Column(String(50), default="Active")
    created_at = Column(TIMESTAMP, server_default=func.now())
    #updated_at = Column(
     #   TIMESTAMP,
      #  server_default=func.now(),
       # onupdate=func.now(),
    #)

class Feedback(Base):
    __tablename__ ="feedback"

    id=Column(Integer, primary_key=True, index=True)
    user_id =Column(Integer,ForeignKey("users.id"),nullable=False)
    given_by=Column(Integer,ForeignKey("users.id"),nullable=False)
    feedback_type=Column(String(50),nullable=True) #e.g. "Peer", "Manager", "Direct Report"
    comments=Column(Text,nullable=False)
    rating=Column(Float,nullable=True)
    #feedback_provider_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    #feedback_text=Column(Text,nullable=False)
    created_at=Column(TIMESTAMP,server_default=func.now())

