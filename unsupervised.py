import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
def unsuperviesd_learning(eat_data):
  standard = np.array([[150,0,0],[0,150,0],[0,0,150]])
  eat_data = np.array(eat_data)
  data = np.concatenate((standard, eat_data))

  x_train = data

  # K-Means Clustering
  kmeans = KMeans(n_clusters=3, init = standard ,n_init='auto')
  kmeans.fit(x_train)
  y = kmeans.labels_

  c_percentage = np.count_nonzero(y == 0)
  p_percentage = np.count_nonzero(y == 1)
  f_percentage = np.count_nonzero(y == 2)
  name = []

  total_percentage = [c_percentage, p_percentage, f_percentage]
  p_index = {0 : "Carbs", 1 : "Protein", 2 : "Fat"}
  #Percentage_index = total_Percentage.index(max(total_Percentage))

  # 가장 큰 값 찾기
  max_value = max(total_percentage)
  # 가장 큰 값의 모든 인덱스 찾기
  max_indices = [index for index, value in enumerate(total_percentage) if value == max_value]

  for i in range(len(max_indices)):

    name.append(p_index[max_indices[i]])


  c_rate = (c_percentage/len(y))*100
  p_rate = (p_percentage/len(y))*100
  f_rate = (f_percentage/len(y))*100

  return [c_rate, p_rate, f_rate]
