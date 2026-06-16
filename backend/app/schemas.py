from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional, List, Dict, Any


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserBase(BaseModel):
    username: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    bio: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    bio: Optional[str] = None
    avatar: Optional[str] = None


class User(UserBase):
    id: int
    avatar: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserWithDistance(User):
    distance: Optional[float] = None


class WeightRecordBase(BaseModel):
    weight: float
    record_date: date
    note: Optional[str] = None


class WeightRecordCreate(WeightRecordBase):
    pass


class WeightRecord(WeightRecordBase):
    id: int
    pet_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class VaccineRecordBase(BaseModel):
    vaccine_name: str
    vaccine_date: date
    next_due_date: Optional[date] = None
    hospital: Optional[str] = None
    note: Optional[str] = None


class VaccineRecordCreate(VaccineRecordBase):
    pass


class VaccineRecord(VaccineRecordBase):
    id: int
    pet_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PetPhotoBase(BaseModel):
    url: str
    description: Optional[str] = None
    is_avatar: bool = False


class PetPhotoCreate(PetPhotoBase):
    pass


class PetPhoto(PetPhotoBase):
    id: int
    pet_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PetBase(BaseModel):
    name: str
    species: str
    breed: str
    gender: Optional[str] = None
    birthday: Optional[date] = None
    weight: Optional[float] = None
    bio: Optional[str] = None
    avatar: Optional[str] = None


class PetCreate(PetBase):
    pass


class PetUpdate(BaseModel):
    name: Optional[str] = None
    species: Optional[str] = None
    breed: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[date] = None
    weight: Optional[float] = None
    bio: Optional[str] = None
    avatar: Optional[str] = None


class Pet(PetBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    weight_records: List[WeightRecord] = []
    vaccine_records: List[VaccineRecord] = []
    photos: List[PetPhoto] = []

    class Config:
        from_attributes = True


class PetWithOwner(Pet):
    owner: User


class PostBase(BaseModel):
    content: str
    media_type: str = "image"
    media_url: Optional[str] = None
    tags: List[str] = []
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    location_name: Optional[str] = None
    pet_id: Optional[int] = None


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    content: Optional[str] = None
    tags: Optional[List[str]] = None


class Post(PostBase):
    id: int
    author_id: int
    likes_count: int = 0
    comments_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_liked: bool = False

    class Config:
        from_attributes = True


class PostWithDetails(Post):
    author: User
    pet: Optional[Pet] = None


class CommentBase(BaseModel):
    content: str
    parent_id: Optional[int] = None


class CommentCreate(CommentBase):
    post_id: int


class Comment(CommentBase):
    id: int
    post_id: int
    author_id: int
    likes_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CommentWithAuthor(Comment):
    author: User
    replies: List["CommentWithAuthor"] = []


CommentWithAuthor.model_rebuild()


class MatchBase(BaseModel):
    target_user_id: int
    message: Optional[str] = None


class MatchCreate(MatchBase):
    pass


class MatchResponse(BaseModel):
    id: int
    user_id: int
    target_user_id: int
    match_score: float
    breed_compatibility: float
    age_similarity: float
    distance_score: float
    status: str
    message: Optional[str] = None
    created_at: datetime
    responded_at: Optional[datetime] = None
    user: Optional[User] = None
    target_user: Optional[User] = None

    class Config:
        from_attributes = True


class BreedEncyclopediaBase(BaseModel):
    name: str
    species: str
    origin: Optional[str] = None
    lifespan: Optional[str] = None
    weight_range: Optional[str] = None
    height_range: Optional[str] = None
    temperament: Optional[str] = None
    appearance: Optional[str] = None
    care_guide: Optional[str] = None
    health_issues: Optional[str] = None
    feeding_guide: Optional[str] = None
    exercise_needs: Optional[str] = None
    image_url: Optional[str] = None


class BreedEncyclopediaCreate(BreedEncyclopediaBase):
    pass


class BreedEncyclopedia(BreedEncyclopediaBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class DiseaseGuideBase(BaseModel):
    name: str
    species: Optional[str] = None
    symptoms: Optional[str] = None
    causes: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    prevention: Optional[str] = None
    severity: str = "moderate"


class DiseaseGuideCreate(DiseaseGuideBase):
    pass


class DiseaseGuide(DiseaseGuideBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ServiceBase(BaseModel):
    name: str
    category: str
    address: str
    phone: Optional[str] = None
    latitude: float
    longitude: float
    rating: float = 0
    review_count: int = 0
    business_hours: Dict[str, Any] = {}
    description: Optional[str] = None
    image_url: Optional[str] = None


class ServiceCreate(ServiceBase):
    pass


class Service(ServiceBase):
    id: int
    created_at: datetime
    distance: Optional[float] = None

    class Config:
        from_attributes = True


class MeetupBase(BaseModel):
    title: str
    description: Optional[str] = None
    location: str
    latitude: float
    longitude: float
    meetup_date: datetime
    max_participants: int = 10


class MeetupCreate(MeetupBase):
    pass


class MeetupParticipant(BaseModel):
    id: int
    meetup_id: int
    user_id: int
    pet_id: Optional[int] = None
    joined_at: datetime
    user: Optional[User] = None
    pet: Optional[Pet] = None

    class Config:
        from_attributes = True


class Meetup(MeetupBase):
    id: int
    organizer_id: int
    current_participants: int = 1
    status: str = "upcoming"
    created_at: datetime
    organizer: Optional[User] = None
    participants: List[MeetupParticipant] = []

    class Config:
        from_attributes = True


class MatchResult(BaseModel):
    target_user: UserWithDistance
    target_pets: List[Pet]
    match_score: float
    breed_compatibility: float
    age_similarity: float
    distance_score: float
