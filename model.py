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

def load_kmean(train_data, test_data):
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
        knn = KNeighborsClassifier(n_neighbors=10, metric=metric)
        knn.fit(X_train, y_train)

      # k-최근접 이웃의 인덱스를 찾습니다.
        distances, indices = knn.kneighbors(X_test)
        print(i)
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
    print(df)
    food_1 = []
    for i in range(10):
      for j in range(10):
          if df["euclidean"][i] == df["manhattan"][j]:
              food_1.append(i)

    food_last = []
    for i in food_1:
      for j in range(10):
          if df["euclidean"][i] == df["cosine"][j]:
              food_last.append(i)

    print("\neuclidean과 mahantan의 교집합 index : ", food_1)
    print("위의 집합에서 cosie 교집합 index :", food_last)
    print("위에 결과는 euclidean_index기준으로 봐주세요")

    food_index = []

    if len(food_last) == 0:
        for i in food_1:
            food_index.append(df['euclidean'][i])
        print(food_index)

    else:
        for i in food_last:
            food_index.append(df['euclidean'][i])
        print(food_index)


      # 3D 산점도 그리기
    fig = plt.figure(figsize=(15, 20))
    ax = fig.add_subplot(111, projection='3d')

    # 훈련 데이터 포인트를 그립니다.
    ax.scatter(X_train[y_train == 0][:, 0], X_train[y_train == 0][:, 1], X_train[y_train == 0][:, 2], c='r',
             marker='o', label='Class 0')
    ax.scatter(X_train[y_train == 1][:, 0], X_train[y_train == 1][:, 1], X_train[y_train == 1][:, 2], c='g',
             marker='^', label='Class 1')

    # 테스트 데이터 포인트를 그립니다.
    ax.scatter(X_test[:, 0], X_test[:, 1], X_test[:, 2], c='b', marker='x', label='Test Data')

    ax.set_xlabel('Feature 1')
    ax.set_ylabel('Feature 2')
    ax.set_zlabel('Feature 3')

    plt.legend(loc='upper right')
    plt.show()