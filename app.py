import datetime

import pymysql
import uuid
from model import set_kcal, set_rate, set_nutrition, load_kmean
from flask import Flask, request, jsonify
import numpy as np
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

db = pymysql.connect(host='222.107.127.85', port=3307, user='root', password='*terry1605', db='capstone_design2', charset='utf8')

def make_json(key_list, value_list):
    column_list = []
    for i in key_list:
        column_list.append(i[0])

    result_list = []
    for row in value_list:
        data_dict = {}
        for i in range(len(column_list)):
            data_dict[column_list[i]] = row[i]
        result_list.append(data_dict)

    return result_list

# 신규계정 등록
@app.route('/capstone2/post_join', methods=['POST'])
def post_join():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    name_receive = request.form['name_give']
    sex_receive = request.form['sex_give']
    type_receive = request.form['type_give']
    age_receive = request.form['age_give']
    height_receive = request.form['height_give']
    weight_receive = request.form['weight_give']
    act_receive = request.form['act_give']

    print(id_receive, pw_receive, name_receive, sex_receive, type_receive, age_receive, height_receive, weight_receive, act_receive)

    kcal = set_kcal(type_receive, sex_receive, float(act_receive), float(height_receive))
    rate = set_rate(type_receive)

    print(rate)

    cursor = db.cursor()
    cursor.execute("insert into account_tb (id, pw) value (%s, %s)", [id_receive, pw_receive])
    cursor.execute("insert into user_tb (id, name, age, height, weight, body_type, sex, act) values(%s, %s, %s, %s, %s, %s, %s, %s)", [id_receive, name_receive, int(age_receive), int(height_receive), int(weight_receive), type_receive, sex_receive, act_receive])
    cursor.execute("insert into nutrition_tb (id, kcal, carbohydrate, protein, fat) values(%s, %s, %s, %s, %s)", [id_receive, kcal, kcal*rate[0], kcal*rate[1], kcal*rate[2]])
    db.commit()
    cursor.close()
    return "1"

#id 중복 확인
@app.route('/capstone2/get_available', methods=['GET'])
def get_available():
    id_receive = request.args.get('id_give')

    print(id_receive)

    cursor = db.cursor()
    id_status = cursor.execute("select * from account_tb where id = %s", [id_receive])
    cursor.close()
    if id_status > 0:
        return "0"
    else:
        return "1"

# 음식 섭취 기록
@app.route('/capstone2/post_history', methods=['POST'])
def post_history():
    id_receive = request.form['id_give']
    code_receive = request.form['code_give']
    date_receive = request.form['date_give']
    amount_receive = request.form['amount_give']
    total_receive = request.form['total_give']

    num = uuid.uuid1()

    cursor = db.cursor()
    cursor.execute("select KCAL, CARBOHYDRATE, PROTEIN, FAT from food_tb where code  = %s", [code_receive])
    result = cursor.fetchone()
    data = set_nutrition(float(result[0]), float(result[1]), float(result[2]), float(result[3]), float(amount_receive))

    cursor.execute("insert into history_tb (num, id, code, record_date, amount, total) values (%s, %s, %s, %s, %s, %s)",
                   [num, id_receive, code_receive, date_receive, float(amount_receive), float(total_receive)])
    cursor.execute("insert into record_tb (num, record_date, kcal, carbohydrate, protein, fat) values (%s, %s, %s, %s, %s, %s)",
                   [num, date_receive, float(data[0]), float(data[1]), float(data[2]), float(data[3])])

    db.commit()
    cursor.close()
    return "1"

# 로그인
@app.route('/capstone2/get_login', methods=['GET'])
def get_login():
    id_receive = request.args.get("id_give")
    pw_receive = request.args.get("pw_give")

    cursor = db.cursor()
    result = cursor.execute("select *  from account_tb where id = %s  and pw = %s", [id_receive, pw_receive])
    cursor.close()

    print(id_receive, pw_receive, result)

    if result == 1:
        cursor = db.cursor()
        cursor.execute("select json_object('id', U.id, 'name', U.name, 'sex', U.sex, 'type', U.body_type, 'age', U.age, 'height', U.height, 'weight', U.weight, 'act', U.act, 'kcal', N.kcal, 'carbohydrate', N.carbohydrate, 'protein', N.protein, 'fat', N.fat) from user_tb U, nutrition_tb N where U.id = %s and U.id = N.id", [id_receive])
        info_list = cursor.fetchone()
        cursor.close()

        print(info_list[0])
        return info_list[0]
    else: return "0"

# 음식 전체 목록 확인
@app.route('/capstone2/get_food', methods=['GET'])
def get_food():
    cursor = db.cursor()
    cursor.execute("select code, name, amount from food_tb")
    result = cursor.fetchall()
    fields_list = cursor.description
    food_list = make_json(fields_list, result)
    cursor.close()

    return jsonify(food_list)

# 음식 섭취 내역 받기
@app.route('/capstone2/get_history', methods=['GET'])
def get_history():
    id_receive = request.args.get("id_give")

    cursor = db.cursor()
    cursor.execute("select H.id, F.name, date_format(H.record_date, '%%Y-%%m-%%d') as date, H.amount, H.total from history_tb H, food_tb F where id = %s and H.code = F.code order by H.record_date desc", [id_receive])
    result = cursor.fetchall()
    fields_list = cursor.description
    cursor.close()

    history_list = make_json(fields_list, result)

    return jsonify(history_list)

@app.route('/capstone2/get_nutrition', methods=['GET'])
def get_nutrition():
    id_receive = request.args.get("id_give")

    cursor = db.cursor()
    cursor.execute("select * from nutrition_tb where id = %s", [id_receive])
    result = cursor.fetchall()
    fields_list = cursor.description

    my_nutrition = make_json(fields_list, result)

    cursor.close()

    return jsonify(my_nutrition)

@app.route('/capstone2/get_record', methods=['GET'])
def get_record():
    id_receive = request.args.get("id_give")

    cursor = db.cursor()
    cursor.execute(
        "select date_format(R.record_date, '%%Y-%%m-%%d'), sum(R.kcal), sum(R.carbohydrate), sum(R.protein), sum(R.fat) from record_tb R, history_tb H where H.id = %s and H.num = R.num group by R.record_date order by R.record_date desc",
        [id_receive])
    result = cursor.fetchall()
    key_list = (("date", 0), ("kcal", 0), ("carbohydrate", 0), ("protein", 0), ("fat", 0))

    my_record = make_json(key_list, result)
    print(my_record)

    cursor.close()

    return jsonify(my_record)
@app.route('/capstone2/get_model_data', methods=['GET'])
def get_model_data():
    id_receive = request.args.get("id_give")

    ### load train_data
    cursor = db.cursor()
    cursor.execute("select CARBOHYDRATE, protein, fat from food_tb")
    result = cursor.fetchall()
    train_data = np.array(result)

    ### load user nutrition_data
    cursor.execute("select carbohydrate, protein, fat from nutrition_tb where id = %s", [id_receive])
    result1 = cursor.fetchall()
    standard = np.array(result1)

    ### load record_data
    cursor.execute(
        "select sum(R.carbohydrate), sum(R.protein), sum(R.fat) from record_tb R, history_tb H where H.id = 'test1' and H.num = R.num and R.record_date = '2023-11-13'")
    result2 = cursor.fetchall()
    user_data = np.array(result2)

    ### set test_data
    test_data = standard-user_data

    print(train_data)
    print(test_data)

    cursor.close()

    load_kmean(train_data, test_data)

    return "1"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
