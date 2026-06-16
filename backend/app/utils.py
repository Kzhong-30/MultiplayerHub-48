from geopy.distance import geodesic
from datetime import date
from typing import List, Tuple
from . import models


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
        return float('inf')
    return geodesic((lat1, lon1), (lat2, lon2)).kilometers


def calculate_age(birthday: date) -> float:
    today = date.today()
    age = today.year - birthday.year
    if today.month < birthday.month or (today.month == birthday.month and today.day < birthday.day):
        age -= 1
    return age


BREED_COMPATIBILITY = {
    "dog": {
        "金毛寻回犬": {"拉布拉多": 0.9, "边境牧羊犬": 0.85, "萨摩耶": 0.8, "哈士奇": 0.7, "柯基": 0.75},
        "拉布拉多": {"金毛寻回犬": 0.9, "边境牧羊犬": 0.8, "萨摩耶": 0.75, "比熊": 0.7},
        "边境牧羊犬": {"金毛寻回犬": 0.85, "拉布拉多": 0.8, "贵宾犬": 0.85, "柯基": 0.7},
        "哈士奇": {"阿拉斯加": 0.9, "萨摩耶": 0.85, "金毛寻回犬": 0.7},
        "萨摩耶": {"哈士奇": 0.85, "阿拉斯加": 0.8, "金毛寻回犬": 0.8},
        "柯基": {"金毛寻回犬": 0.75, "比熊": 0.8, "贵宾犬": 0.75},
        "贵宾犬": {"边境牧羊犬": 0.85, "比熊": 0.9, "柯基": 0.75},
        "比熊": {"贵宾犬": 0.9, "柯基": 0.8, "拉布拉多": 0.7},
        "阿拉斯加": {"哈士奇": 0.9, "萨摩耶": 0.8},
    },
    "cat": {
        "英国短毛猫": {"美国短毛猫": 0.85, "布偶猫": 0.8, "暹罗猫": 0.7},
        "美国短毛猫": {"英国短毛猫": 0.85, "波斯猫": 0.75, "暹罗猫": 0.75},
        "布偶猫": {"英国短毛猫": 0.8, "波斯猫": 0.85, "缅因猫": 0.8},
        "暹罗猫": {"英国短毛猫": 0.7, "美国短毛猫": 0.75, "孟加拉豹猫": 0.85},
        "波斯猫": {"美国短毛猫": 0.75, "布偶猫": 0.85},
        "缅因猫": {"布偶猫": 0.8, "挪威森林猫": 0.9},
        "孟加拉豹猫": {"暹罗猫": 0.85, "阿比西尼亚猫": 0.8},
    }
}


def get_breed_compatibility(breed1: str, breed2: str, species: str) -> float:
    if breed1 == breed2:
        return 0.95
    
    species_data = BREED_COMPATIBILITY.get(species, {})
    if breed1 in species_data and breed2 in species_data[breed1]:
        return species_data[breed1][breed2]
    if breed2 in species_data and breed1 in species_data[breed2]:
        return species_data[breed2][breed1]
    
    return 0.5


def calculate_age_similarity(age1: float, age2: float) -> float:
    diff = abs(age1 - age2)
    if diff <= 0.5:
        return 1.0
    elif diff <= 1:
        return 0.9
    elif diff <= 2:
        return 0.75
    elif diff <= 3:
        return 0.6
    elif diff <= 5:
        return 0.4
    else:
        return 0.2


def calculate_distance_score(distance_km: float) -> float:
    if distance_km <= 1:
        return 1.0
    elif distance_km <= 3:
        return 0.9
    elif distance_km <= 5:
        return 0.8
    elif distance_km <= 10:
        return 0.6
    elif distance_km <= 20:
        return 0.4
    elif distance_km <= 50:
        return 0.2
    else:
        return 0.0


def calculate_match_score(
    user_pets: List[models.Pet],
    target_pets: List[models.Pet],
    user_lat: float,
    user_lon: float,
    target_lat: float,
    target_lon: float
) -> Tuple[float, float, float, float]:
    if not user_pets or not target_pets:
        return 0, 0, 0, 0
    
    breed_scores = []
    age_scores = []
    
    for user_pet in user_pets:
        for target_pet in target_pets:
            if user_pet.species == target_pet.species:
                breed_compat = get_breed_compatibility(
                    user_pet.breed, target_pet.breed, user_pet.species
                )
                breed_scores.append(breed_compat)
                
                if user_pet.birthday and target_pet.birthday:
                    age1 = calculate_age(user_pet.birthday)
                    age2 = calculate_age(target_pet.birthday)
                    age_sim = calculate_age_similarity(age1, age2)
                    age_scores.append(age_sim)
    
    avg_breed = sum(breed_scores) / len(breed_scores) if breed_scores else 0.5
    avg_age = sum(age_scores) / len(age_scores) if age_scores else 0.5
    
    distance = calculate_distance(user_lat, user_lon, target_lat, target_lon)
    distance_score = calculate_distance_score(distance)
    
    total_score = (avg_breed * 0.4 + avg_age * 0.3 + distance_score * 0.3) * 100
    
    return total_score, avg_breed, avg_age, distance_score
