import pymysql
from flask import Flask, request, jsonify
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
@app.route('/capstone2/post_account', methods=['POST'])
def post_join():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    name_receive = request.form['name_give']
    sex_receive = request.form['sex_give']
    type_receive = request.form['type_give']
    age_receive = request.form['age_give']
    height_receive = request.form['height_give']
    weight_receive = request.form['weight_give']

    #print(id_receive, pw_receive, name_receive, sex_receive, type_receive, age_receive, height_receive, weight_receive)

    cursor = db.cursor()
    cursor.execute("insert into account_tb (id, pw) value (%s, %s)", [id_receive, pw_receive])
    cursor.execute("insert into user_tb (id, name, age, height, weight, body_type, sex) values(%s, %s, %s, %s, %s, %s, %s)", [id_receive, name_receive, int(age_receive), int(height_receive), int(weight_receive), type_receive, sex_receive])
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

    print(id_receive, code_receive, date_receive, amount_receive, total_receive)

    cursor = db.cursor()
    cursor.execute("insert into record_tb (id, code, date, amount, total) values (%s, %s, %s, %s, %s)",
                   [id_receive, code_receive, date_receive, float(amount_receive), float(total_receive)])
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
        cursor.execute("select json_object('id', id, 'name', name, 'sex', sex, 'type', body_type, 'age', age, 'height', height, 'weight', weight) from user_tb where id = %s", [id_receive])
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

    return jsonify(food_list)

# 음식 섭취 내역 받기
@app.route('/capstone2/get_history', methods=['GET'])
def get_history():
    id_receive = request.args.get("id_give")

    print(id_receive)

    cursor = db.cursor()
    cursor.execute("select R.id, F.name, date_format(R.date, '%%Y-%%m-%%d') as date, R.amount, R.total from record_tb R, food_tb F where id = %s and R.code = F.code", [id_receive])
    result = cursor.fetchall()
    fields_list = cursor.description

    history_list = make_json(fields_list, result)

    print(history_list)

    return jsonify(history_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0')