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
# Mahabote planetary mapping (Day Index -> Mahabote data)
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

# House mapping: remainder -> house information
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
    H = (Age + Day Value) mod 7
    """
    age_in_years = current_date.year - dob.year - ((current_date.month, current_date.day) < (dob.month, dob.day))
    remainder = (age_in_years + day_value) % 7
    remainder_for_mapping = remainder if remainder != 0 else 0
    house_result = HOUSE_MAP.get(remainder_for_mapping)

    return {
        "age": age_in_years,
        "current_house_remainder": remainder if remainder != 0 else 7,
        "house_info": house_result
    }


def generate_life_journey_map(dob: dt.date, birth_day_idx: int) -> List[Dict[str, Any]]:
    """
    Generates the entire life house cycle map based on the starting planet/period.
    """
    journey = []
    current_date = dob
    start_house_value = MAHABOTE_DATA[birth_day_idx]['value']

    for i in range(7):
        # Adjust value for cycle wraparound and Rahu special case
        if start_house_value == 8 and i == 0:
            current_planet_value = 8
        elif start_house_value == 8:
            current_planet_value = (i) % 7
            if current_planet_value == 0: current_planet_value = 7
        else:
            current_planet_value = (start_house_value + i) % 7
            if current_planet_value == 0: current_planet_value = 7

        data = next((d for d in MAHABOTE_DATA.values() if d['value'] == current_planet_value), None)
        if data:
            start_date_str = current_date.strftime("%Y-%m-%d")
            end_date = current_date.replace(year=current_date.year + data['period'])
            end_date_str = end_date.strftime("%Y-%m-%d")

            journey.append({
                "period": i + 1,
                "house_value": current_planet_value,
                "house_name": data['house_name'],
                "duration": data['period'],
                "start_date": start_date_str,
                "end_date": end_date_str
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
    Calculates the 7 daily temporal blocks based on planetary sequence.
    """
    if birth_day_idx == 3 and 7 in MAHABOTE_DATA:
        birth_day_idx = 7  # Handle Rahu for Wednesday Afternoon

    sequence = MAHABOTE_DATA[birth_day_idx]['sequence']
    day_start = dt.datetime.combine(current_date, sunrise)
    day_end = dt.datetime.combine(current_date, sunset)
    day_length = day_end - day_start
    block_duration = day_length / 7

    time_map = []
    current_time = day_start

    for i, house_value in enumerate(sequence):
        end_time = current_time + block_duration
        if house_value == 8:
            house_name = "Rahu/Extremity"
        else:
            house_name = next((h['name'] for h in HOUSE_MAP.values() if h['planet_value'] == house_value), "N/A")

        time_map.append({
            "block": i + 1,
            "planet_value": house_value,
            "start_time": current_time.strftime("%H:%M:%S"),
            "end_time": end_time.strftime("%H:%M:%S"),
            "mahabote_meaning": house_name
        })
        current_time = end_time

    return time_map


# === 4. MSSAPredictor CLASS FOR FASTAPI INTEGRATION ===

class MSSAPredictor:
    """
    Encapsulates Mahabote and Inga Wizar calculations for API use.
    """

    def generate_guidance(self, name: str, birth_date: str, house_cycle: int) -> Dict[str, Any]:
        dob = dt.datetime.strptime(birth_date, "%Y-%m-%d").date()
        current_date = dt.date.today()
        house_info = calculate_mahabote_house(dob, current_date, house_cycle)
        journey_map = generate_life_journey_map(dob, house_cycle)

        return {
            "guidance": f"Dear {name}, your current Mahabote House is {house_info['house_info']['name']}.",
            "score": house_info['current_house_remainder'],
            "journey": journey_map
        }


# === 5. OPTIONAL TEST USAGE ===
if __name__ == "__main__":
    dob_example = dt.date(1967, 5, 30)
    house_example = calculate_mahabote_house(dob_example, dt.date.today(), 3)
    journey_example = generate_life_journey_map(dob_example, 2)
    print("Current House:", house_example)
    print("Life Journey Map:", journey_example)
