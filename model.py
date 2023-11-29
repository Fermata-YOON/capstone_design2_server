from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import pairwise_distances_argmin_min
import pandas as pd

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

def load_kmean(train_data, test_data, cnt):
  # 예제 데이터 생성
  # 음식 영양소의 data가 들어감
  #X_train = np.random.rand(100, 3)
    X_train = train_data

  # 임의의 값 배정
    y_train = np.random.randint(2, size=train_data.shape[0])

  #X_test = np.array([[1.5, 2.5, 5], [1, 3, 5]])
  #X_test에는 부족한 영양소의 탄,단,지로 3차원 데이터 들어감
  #X_test = np.random.rand(1, 3)
    X_test = test_data

  # 다양한 거리 메트릭을 정의합니다.
    distance_metrics = ['euclidean', 'manhattan', 'cosine']

    predictions = []
    i = 0

  # 각 거리 메트릭에 대한 반복
    for metric in distance_metrics:
        knn = KNeighborsClassifier(n_neighbors=cnt, metric=metric)
        knn.fit(X_train, y_train)

      # k-최근접 이웃의 인덱스를 찾습니다.
        distances, indices = knn.kneighbors(X_test)
        #print(i)
        if i == 0 :
            df = pd.DataFrame({ "euclidean" : indices.flatten() })
            i += 1
        elif i == 1:
            df["manhattan"] = indices.flatten()
            i += 1
        else :
            df["cosine"] = indices.flatten()
        # print(f"{metric} 거리를 사용합니다:")
        # print(f"가장 가까운 이웃의 인덱스: \n{indices}\n")
        # print("가장 가까운 이웃의 index 거리 : \n", distances, '\n')

        y_pred = knn.predict(X_test)

        # print(f"X_test에 대한 예측 클래스: {y_pred}")
        # print("------------------------------------\n")
        # predictions.append(y_pred)

      # 앙상블 방법으로 최종 예측을 수행합니다.
    final_prediction = np.round(np.mean(predictions, axis=0))

      # print("Final Prediction:", final_prediction)
      # print("\n",df)
    #print(df)

    all_index = dict()
    first = []
    second = []

    for i in range(cnt):
        tmp = [df["euclidean"][i], df["manhattan"][i], df["cosine"][i]]
        for x in tmp:
            all_index[x] = all_index.get(x, 0) + 1

    for key, val in all_index.items():
        if val == 3:
            first.append(key)
        elif val == 2:
            second.append(key)

    res = [first, second]

    #print(res)


    #print("euclidean, manhattan, cosine 중 두개에 속하는 index : ", second_recommend)
    #print("euclidean, manhattan, cosine 3개의 교집합 index :", first_recommend)
    #print("위에 결과는 euclidean_index기준으로 봐주세요")


    return res