import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.dependencies import get_db
from app.main import app
from app.config import settings
from app.core.security import get_password_hash
from app.models.user import User
from app.models.parking_slot import ParkingSlot
from typing import Generator
from app.schemas.user import UserRoleEnum
from app.schemas.parking_slot import SlotStatusEnum
from app.schemas.booking import BookingStatusEnum


# Create test database
SQLALCHEMY_DATABASE_URL = settings.TEST_DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db():
    # Create the database tables
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
    # Tear down the database
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):
    # Dependency override
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    
    # Reset dependency
    app.dependency_overrides = {}


@pytest.fixture
def test_user(db):
    user = User(
        email="user@example.com",
        hashed_password=get_password_hash("password"),
        role=UserRoleEnum.user,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def test_admin(db):
    admin = User(
        email="admin@example.com",
        hashed_password=get_password_hash("password"),
        role=UserRoleEnum.admin,
        is_active=True
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


@pytest.fixture
def test_parking_slot(db):
    slot = ParkingSlot(
        slot_identifier="A1",
        status=SlotStatusEnum.free,
        floor=1,
        label="Test Slot"
    )
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return slot


@pytest.fixture
def user_token_headers(client, test_user):
    response = client.post(
        "/api/auth/token",
        data={"username": test_user.email, "password": "password"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_token_headers(client, test_admin):
    response = client.post(
        "/api/auth/token",
        data={"username": test_admin.email, "password": "password"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}