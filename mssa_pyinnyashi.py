# mssa_pyinnyashi.py
# The Core V14 Pyinnyashi Engine (Academic and Mathematicians Friendly)

import datetime as dt
from math import floor

# === 1. MYISM MSSA PYINNYASHI CONFIGURATION CODES ===
# V14-VERIFY: Custom Planetary Values based on user-defined system.
# Key: Day Index (0=Sun, 1=Mon... 6=Sat, 7=Rahu) -> Mahabote Value (D) -> Period in Years (P)
MAHABOTE_DATA = {
    0: {'planet': 'Sun', 'value': 1, 'period': 6, 'house_name': 'Impermanence/Inconstant', 'sequence': [1, 6, 4, 2, 7, 5, 3]},
    1: {'planet': 'Moon', 'value': 2, 'period': 15, 'house_name': 'Extremity/Danger', 'sequence': [2, 7, 5, 3, 1, 6, 4]},
    # NOTE: The user has defined Tuesday's value as 3, not the standard 2.
    2: {'planet': 'Mars', 'value': 3, 'period': 8, 'house_name': 'Fame/Courage', 'sequence': [3, 1, 6, 4, 2, 7, 5]}, 
    3: {'planet': 'Mercury', 'value': 4, 'period': 17, 'house_name': 'Wealth/Respect', 'sequence': [4, 2, 7, 5, 3, 1, 6]}, 
    # Wednesday Afternoon/Rahu is represented by index 7 for the day mapping, but value 8 for Mahabote.
    7: {'planet': 'Rahu', 'value': 8, 'period': 12, 'house_name': 'Extremity/Inconstancy', 'sequence': [8, 5, 3, 1, 6, 4, 2]}, # Rahu Sequence is often 8,5,3,1,6,4,2, or (4,2,7,5,3,1,6) depending on system
    4: {'planet': 'Jupiter', 'value': 5, 'period': 19, 'house_name': 'Kingly Position', 'sequence': [5, 3, 1, 6, 4, 2, 7]}, 
    5: {'planet': 'Venus', 'value': 6, 'period': 21, 'house_name': 'Sickly/Change', 'sequence': [6, 4, 2, 7, 5, 3, 1]},
    6: {'planet': 'Saturn', 'value': 7, 'period': 10, 'house_name': 'Leader/Counselor', 'sequence': [7, 5, 3, 1, 6, 4, 2]}
}

# Mapping Mahabote numerical output (remainder) to House Data
HOUSE_MAP = {
    1: {'planet_value': 1, 'name': 'Impermanence', 'ruler': 'Sun'},
    2: {'planet_value': 2, 'name': 'Extremity', 'ruler': 'Moon'},
    3: {'planet_value': 3, 'name': 'Fame', 'ruler': 'Mars'},
    4: {'planet_value': 4, 'name': 'Wealth', 'ruler': 'Mercury'},
    5: {'planet_value': 5, 'name': 'Kingly Position', 'ruler': 'Jupiter'},
    6: {'planet_value': 6, 'name': 'Sickly/Change', 'ruler': 'Venus'},
    0: {'planet_value': 7, 'name': 'Leader', 'ruler': 'Saturn'} # Remainder 0 is the 7th House
}

# === 2. MAHABOTE CORE CALCULATION FUNCTIONS ===

def calculate_mahabote_house(dob: dt.date, current_date: dt.date, day_value: int) -> dict:
    """
    Calculates the current Mahabote House (H) and Age.
    H = (Age + Day Value) mod 7
    """
    age_in_years = current_date.year - dob.year - ((current_date.month, current_date.day) < (dob.month, dob.day))
    
    # Mathematical Model: H = (Age + D) mod 7
    remainder = (age_in_years + day_value) % 7
    
    # Map the result to the correct House Name/Ruler (0 maps to 7th House)
    house_result = HOUSE_MAP.get(remainder if remainder != 0 else 0)
    
    return {
        "age": age_in_years,
        "current_house_remainder": remainder if remainder != 0 else 7,
        "house_info": house_result
    }

def generate_life_journey_map(dob: dt.date, birth_day_idx: int) -> list:
    """
    Generates the entire life house cycle map based on the starting planet/period.
    """
    journey = []
    current_date = dob
    
    # Determine the start house and period order based on Mahabote rotation
    # (House 1=Sun, 2=Moon... 7=Sat)
    start_house_value = MAHABOTE_DATA[birth_day_idx]['value']
    
    # Adjust for the Rahu/Mercury split: Rahu is treated as a separate starting point (8th)
    # The Houses still rotate 1-7 (Sun to Saturn), but the starting year is based on the birth planet's period (P)
    
    # Use a custom list for the starting order based on the initial D.
    planet_order = []
    # Simplified ordering (D, D+1, D+2...) in the cycle of 7
    for i in range(7):
        # The key for MAHABOTE_DATA is the Day Value (1-7/8), not the list index (0-6/7).
        current_planet_value = (start_house_value + i) 
        
        # Mapping 8 (Rahu) to its correct Mahabote House 
        if start_house_value == 8 and i == 0:
            current_planet_value = 8 # Start with Rahu
        elif start_house_value == 8 and i > 0:
            current_planet_value = (start_house_value + i) % 7 
            if current_planet_value == 0: current_planet_value = 7 # Adjust remainder 0 to 7
        elif current_planet_value > 7:
            current_planet_value = current_planet_value % 7 
            if current_planet_value == 0: current_planet_value = 7
        
        # Locate the corresponding Mahabote Data based on the planet's value (1-7) or 8 for Rahu start
        data = next((d for d in MAHABOTE_DATA.values() if d['value'] == current_planet_value), None)
        if data:
             journey.append({
                "period": i + 1,
                "house_value": current_planet_value,
                "house_name": data['house_name'],
                "duration": data['period'],
                "start_date": current_date.strftime("%Y-%m-%d"),
                "end_date": (current_date.replace(year=current_date.year + data['period'])).strftime("%Y-%m-%d")
            })
             current_date = current_date.replace(year=current_date.year + data['period'])
             
    return journey

# === 3. INGA WIZAR PYINNYAR (TEMPORAL) CALCULATION ===

def calculate_inga_wizar_map(birth_day_idx: int, current_date: dt.date, sunrise: dt.time, sunset: dt.time) -> list:
    """
    Calculates the 7 daily blocks based on the planetary sequence.
    """
    # Use the Rahu data (index 7) for Wednesday Afternoon 
    if birth_day_idx == 3: # Handle ambiguity of Wednesday: Assume Rahu if not specified
        if MAHABOTE_DATA[7]:
            birth_day_idx = 7
        else:
            # Fallback to Mercury if Rahu data is absent
            pass 
            
    sequence = MAHABOTE_DATA[birth_day_idx]['sequence']
    
    # Calculate Day Length and Block Duration
    day_start = dt.datetime.combine(current_date.date(), sunrise)
    day_end = dt.datetime.combine(current_date.date(), sunset)
    day_length = day_end - day_start
    block_duration = day_length / 7
    
    time_map = []
    current_time = day_start
    
    for i in range(7):
        end_time = current_time + block_duration
        
        # Map the sequence value back to the House Name for description
        house_value = sequence[i]
        house_name = next((h['name'] for h in HOUSE_MAP.values() if h['planet_value'] == (house_value if house_value <= 7 else 4)), "N/A")
        
        # Adjust Rahu to the correct Mahabote Name (Wealth/Respect for Rahu's position in the sequence)
        if house_value == 8:
            house_name = "Rahu/Extremity"
            
        time_map.append({
            "block": i + 1,
            "planet_value": house_value,
            "start_time": current_time.strftime("%H:%M:%S"),
            "end_time": end_time.strftime("%H:%M:%S"),
            "mahabote_meaning": house_name
        })
        current_time = end_time
        
    return time_map

# Example Usage (Client Ingar Soe - Tuesday Born Value 3)
# dob_ing = dt.date(1967, 5, 30)
# current_date_ing = dt.date(2025, 10, 20)
# house_ing = calculate_mahabote_house(dob_ing, current_date_ing, 3)
# journey_ing = generate_life_journey_map(dob_ing, 2) # Index 2 for Tuesday
# print(f"Ingar Soe Current House: {house_ing}") 
# print(f"Ingar Soe Journey Map: {journey_ing}")
