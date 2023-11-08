def set_kcal(body_type, sex, act, height):
    if body_type == "N": #일반
        nut_ratio = [0.4, 0.4, 0.2]
    elif body_type == "H": #운동
        nut_ratio = [0.5, 0.3, 0.2]
    elif body_type == "D": #다이어트
        nut_ratio = [0.1, 0.1, 0.1]

    #가벼운 활동 - 25, 일상적 업무 - 30 ~ 35, 심한 활동(육체 노동) - 40
    if sex == "M":
        a_weight = ((height/100)**2) * 22
    else:
        a_weight = ((height/100)**2) * 21

    kcal = round(a_weight * act)
    print("하루 권장 칼로리 : ", kcal)

    return kcal

def set_rate(body_type):
    if body_type == "M":
        return [0.4, 0.4, 0.2]
    elif body_type == "H":
        return [0.5, 0.3, 0.2]
    else:
        return [0.1, 0.1, 0.1]

def set_nutrition(kcal, carbohydrate, protein, fat, amount):
    return [kcal*amount, carbohydrate*amount, protein*amount, fat*amount]