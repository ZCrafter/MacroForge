def calculate_goals(profile: dict) -> list[dict]:
    # Simplified BMR + activity multiplier
    sex = profile.get('sex', 'male').lower()
    weight_lb = profile.get('weight_lb', 180)
    height_in = profile.get('height_in', 70)
    age = profile.get('age', 30)
    activity = profile.get('activity_level', 'moderate')
    
    weight_kg = weight_lb * 0.453592
    height_cm = height_in * 2.54
    
    if sex == 'male':
        bmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)
    
    multipliers = {'sedentary': 1.2, 'light': 1.375, 'moderate': 1.55, 'active': 1.725, 'very_active': 1.9}
    activity_mult = multipliers.get(activity, 1.55)
    
    calories = int(bmr * activity_mult)
    
    return [
        {'nutrient': 'calories', 'target_per_day': calories, 'target_per_week': calories * 7, 'source': 'Harris-Benedict', 'explanation': f'BMR {bmr:.0f} × {activity_mult} activity'},
        {'nutrient': 'protein_g', 'target_per_day': int(weight_kg * 1.6), 'target_per_week': int(weight_kg * 1.6 * 7), 'source': 'ISSN', 'explanation': f'{weight_kg:.0f}kg × 1.6g/kg'},
        {'nutrient': 'carbs_g', 'target_per_day': int(calories * 0.45 / 4), 'target_per_week': int(calories * 0.45 / 4 * 7), 'source': 'AMDR', 'explanation': '45% calories from carbs'},
        {'nutrient': 'fat_g', 'target_per_day': int(calories * 0.30 / 9), 'target_per_week': int(calories * 0.30 / 9 * 7), 'source': 'AMDR', 'explanation': '30% calories from fat'},
        {'nutrient': 'fiber_g', 'target_per_day': 38 if sex == 'male' else 25, 'target_per_week': 266 if sex == 'male' else 175, 'source': 'IOM', 'explanation': f'{sex} adult recommendation'},
    ]
