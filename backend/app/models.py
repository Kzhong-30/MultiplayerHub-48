from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Text, Boolean, ARRAY, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    avatar = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    pets = relationship("Pet", back_populates="owner", cascade="all, delete-orphan")
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    sent_matches = relationship("Match", foreign_keys="Match.user_id", back_populates="user", cascade="all, delete-orphan")
    received_matches = relationship("Match", foreign_keys="Match.target_user_id", back_populates="target_user", cascade="all, delete-orphan")


class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    species = Column(String, nullable=False)
    breed = Column(String, nullable=False)
    gender = Column(String, nullable=True)
    birthday = Column(Date, nullable=True)
    weight = Column(Float, nullable=True)
    avatar = Column(String, nullable=True)
    bio = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship("User", back_populates="pets")
    weight_records = relationship("WeightRecord", back_populates="pet", cascade="all, delete-orphan")
    vaccine_records = relationship("VaccineRecord", back_populates="pet", cascade="all, delete-orphan")
    photos = relationship("PetPhoto", back_populates="pet", cascade="all, delete-orphan")
    posts = relationship("Post", back_populates="pet")


class WeightRecord(Base):
    __tablename__ = "weight_records"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    weight = Column(Float, nullable=False)
    record_date = Column(Date, nullable=False)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    pet = relationship("Pet", back_populates="weight_records")


class VaccineRecord(Base):
    __tablename__ = "vaccine_records"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    vaccine_name = Column(String, nullable=False)
    vaccine_date = Column(Date, nullable=False)
    next_due_date = Column(Date, nullable=True)
    hospital = Column(String, nullable=True)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    pet = relationship("Pet", back_populates="vaccine_records")


class PetPhoto(Base):
    __tablename__ = "pet_photos"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    url = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    is_avatar = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    pet = relationship("Pet", back_populates="photos")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=True)
    content = Column(Text, nullable=False)
    media_type = Column(String, default="image")
    media_url = Column(String, nullable=True)
    tags = Column(JSON, default=list)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    location_name = Column(String, nullable=True)
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    author = relationship("User", back_populates="posts")
    pet = relationship("Pet", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    likes_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")
    parent = relationship("Comment", remote_side=[id], back_populates="replies")
    replies = relationship("Comment", back_populates="parent", cascade="all, delete-orphan")


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    post = relationship("Post", back_populates="likes")


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    target_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    match_score = Column(Float, nullable=False)
    breed_compatibility = Column(Float, default=0)
    age_similarity = Column(Float, default=0)
    distance_score = Column(Float, default=0)
    status = Column(String, default="pending")
    message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    responded_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", foreign_keys=[user_id], back_populates="sent_matches")
    target_user = relationship("User", foreign_keys=[target_user_id], back_populates="received_matches")


class BreedEncyclopedia(Base):
    __tablename__ = "breed_encyclopedia"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    species = Column(String, nullable=False)
    origin = Column(String, nullable=True)
    lifespan = Column(String, nullable=True)
    weight_range = Column(String, nullable=True)
    height_range = Column(String, nullable=True)
    temperament = Column(Text, nullable=True)
    appearance = Column(Text, nullable=True)
    care_guide = Column(Text, nullable=True)
    health_issues = Column(Text, nullable=True)
    feeding_guide = Column(Text, nullable=True)
    exercise_needs = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class DiseaseGuide(Base):
    __tablename__ = "disease_guides"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    species = Column(String, nullable=True)
    symptoms = Column(Text, nullable=True)
    causes = Column(Text, nullable=True)
    diagnosis = Column(Text, nullable=True)
    treatment = Column(Text, nullable=True)
    prevention = Column(Text, nullable=True)
    severity = Column(String, default="moderate")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    rating = Column(Float, default=0)
    review_count = Column(Integer, default=0)
    price_range = Column(String, nullable=True)
    tags = Column(JSON, default=list)
    business_hours = Column(JSON, default=dict)
    description = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Meetup(Base):
    __tablename__ = "meetups"

    id = Column(Integer, primary_key=True, index=True)
    organizer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    meetup_date = Column(DateTime(timezone=True), nullable=False)
    max_participants = Column(Integer, default=10)
    current_participants = Column(Integer, default=1)
    status = Column(String, default="upcoming")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    organizer = relationship("User", foreign_keys=[organizer_id])
    participants = relationship("MeetupParticipant", back_populates="meetup", cascade="all, delete-orphan")


class MeetupParticipant(Base):
    __tablename__ = "meetup_participants"

    id = Column(Integer, primary_key=True, index=True)
    meetup_id = Column(Integer, ForeignKey("meetups.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=True)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())

    meetup = relationship("Meetup", back_populates="participants")
    user = relationship("User", foreign_keys=[user_id])
    pet = relationship("Pet", foreign_keys=[pet_id])
