# mssa_pyinnyashi.py
"""
MSSA Pyinnyashi System V14 Core Engine
Author: U Ingar Soe
Date: 2025
Academic & Mathematician Friendly Version
"""

import datetime as dt
from typing import List, Dict, Any

# === 1. MSSA PYINNYASHI CONFIGURATION ===
MAHABOTE_DATA: Dict[int, Dict[str, Any]] = {
    0: {'planet': 'Sun', 'value': 1, 'period': 6, 'house_name': 'Impermanence/Inconstant', 'sequence': [1, 6, 4, 2, 7, 5, 3]},
    1: {'planet': 'Moon', 'value': 2, 'period': 15, 'house_name': 'Extremity/Danger', 'sequence': [2, 7, 5, 3, 1, 6, 4]},
    2: {'planet': 'Mars', 'value': 3, 'period': 8, 'house_name': 'Fame/Courage', 'sequence': [3, 1, 6, 4, 2, 7, 5]},
    3: {'planet': 'Mercury', 'value': 4, 'period': 17, 'house_name': 'Wealth/Respect', 'sequence': [4, 2, 7, 5, 3, 1, 6]},
    4: {'planet': 'Jupiter', 'value': 5, 'period': 19, 'house_name': 'Kingly Position', 'sequence': [5, 3, 1, 6, 4, 2, 7]},
    5: {'planet': 'Venus', 'value': 6, 'period': 21, 'house_name': 'Sickly/Change', 'sequence': [6, 4, 2, 7, 5, 3, 1]},
    6: {'planet': 'Saturn', 'value': 7, 'period': 10, 'house_name': 'Leader/Counselor', 'sequence': [7, 5, 3, 1, 6, 4, 2]},
    7: {'planet': 'Rahu', 'value': 8, 'period': 12, 'house_name': 'Extremity/Inconstancy', 'sequence': [8, 5, 3, 1, 6, 4, 2]},
}

HOUSE_MAP: Dict[int, Dict[str, Any]] = {
    1: {'planet_value': 1, 'name': 'Impermanence', 'ruler': 'Sun'},
    2: {'planet_value': 2, 'name': 'Extremity', 'ruler': 'Moon'},
    3: {'planet_value': 3, 'name': 'Fame', 'ruler': 'Mars'},
    4: {'planet_value': 4, 'name': 'Wealth', 'ruler': 'Mercury'},
    5: {'planet_value': 5, 'name': 'Kingly Position', 'ruler': 'Jupiter'},
    6: {'planet_value': 6, 'name': 'Sickly/Change', 'ruler': 'Venus'},
    0: {'planet_value': 7, 'name': 'Leader', 'ruler': 'Saturn'},
}


# === 2. MAHABOTE CORE FUNCTIONS ===

def calculate_mahabote_house(dob: dt.date, current_date: dt.date, day_value: int) -> Dict[str, Any]:
    """
    Calculates the current Mahabote House and age.
    Formula: H = (Age + Day Value) mod 7
    """
    age = current_date.year - dob.year - ((current_date.month, current_date.day) < (dob.month, dob.day))
    remainder = (age + day_value) % 7
    house_key = remainder if remainder != 0 else 0
    house_info = HOUSE_MAP.get(house_key)
    return {
        "age": age,
        "current_house_remainder": remainder if remainder != 0 else 7,
        "house_info": house_info
    }


def generate_life_journey_map(dob: dt.date, birth_day_idx: int) -> List[Dict[str, Any]]:
    """
    Generates a complete life journey map with house cycles.
    Handles Rahu and modular cycle wraparounds correctly.
    """
    journey = []
    current_date = dob
    start_value = MAHABOTE_DATA[birth_day_idx]['value']

    for i in range(7):
        # Determine current house value with modular arithmetic
        if start_value == 8 and i == 0:
            current_house_value = 8  # Rahu first block
        elif start_value == 8:
            current_house_value = (i % 7) or 7
        else:
            current_house_value = ((start_value + i - 1) % 7) + 1

        # Lookup Mahabote data
        house_data = next((d for d in MAHABOTE_DATA.values() if d['value'] == current_house_value), None)
        if house_data:
            start_str = current_date.strftime("%Y-%m-%d")
            # Safely handle year increments (leap years)
            try:
                end_date = current_date.replace(year=current_date.year + house_data['period'])
            except ValueError:
                # February 29 fallback
                end_date = current_date.replace(year=current_date.year + house_data['period'], day=28)
            end_str = end_date.strftime("%Y-%m-%d")

            journey.append({
                "period_index": i + 1,
                "house_value": current_house_value,
                "house_name": house_data['house_name'],
                "duration_years": house_data['period'],
                "start_date": start_str,
                "end_date": end_str
            })
            current_date = end_date

    return journey


# === 3. INGA WIZAR TEMPORAL FUNCTIONS ===

def calculate_inga_wizar_map(
    birth_day_idx: int,
    current_date: dt.date,
    sunrise: dt.time,
    sunset: dt.time
) -> List[Dict[str, Any]]:
    """
    Computes 7 temporal blocks for a single day using planetary sequences.
    """
    if birth_day_idx == 3 and 7 in MAHABOTE_DATA:
        birth_day_idx = 7  # Rahu adjustment

    sequence = MAHABOTE_DATA[birth_day_idx]['sequence']
    day_start = dt.datetime.combine(current_date, sunrise)
    day_end = dt.datetime.combine(current_date, sunset)
    block_length = (day_end - day_start) / 7

    blocks = []
    current_time = day_start

    for idx, value in enumerate(sequence):
        end_time = current_time + block_length
        house_name = "Rahu/Extremity" if value == 8 else next((h['name'] for h in HOUSE_MAP.values() if h['planet_value'] == value), "N/A")
        blocks.append({
            "block_index": idx + 1,
            "planet_value": value,
            "start_time": current_time.strftime("%H:%M:%S"),
            "end_time": end_time.strftime("%H:%M:%S"),
            "house_name": house_name
        })
        current_time = end_time

    return blocks


# === 4. MSSAPredictOR CLASS ===

class MSSAPredictor:
    """
    Core engine for FastAPI integration.
    """

    def generate_guidance(self, name: str, birth_date: str, house_cycle: int) -> Dict[str, Any]:
        dob = dt.datetime.strptime(birth_date, "%Y-%m-%d").date()
        today = dt.date.today()
        house_info = calculate_mahabote_house(dob, today, house_cycle)
        journey = generate_life_journey_map(dob, house_cycle)

        return {
            "guidance": f"Dear {name}, your current Mahabote House is {house_info['house_info']['name']}.",
            "score": house_info['current_house_remainder'],
            "journey_map": journey
        }


# === 5. OPTIONAL TEST RUN ===
if __name__ == "__main__":
    dob_sample = dt.date(1967, 5, 30)
    current_house = calculate_mahabote_house(dob_sample, dt.date.today(), 3)
    journey = generate_life_journey_map(dob_sample, 3)
    print("Current Mahabote House:", current_house)
    print("Life Journey Map:")
    for p in journey:
        print(f"Period {p['period_index']}: {p['house_name']} ({p['start_date']} → {p['end_date']})")
