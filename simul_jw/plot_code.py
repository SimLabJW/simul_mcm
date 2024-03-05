import sys 
import csv 
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd

def get_last_12_columns(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
        
        # 만약 헤더가 있는 경우, 헤더를 포함하고 싶지 않으면 data = data[1:] 을 사용합니다.
        last_12_columns_data = [row[-12:] for row in data]
   
    return last_12_columns_data

# 파일명
csv_file_path = 'NOB_Mixed_512DP_v1_out copy.csv'

# 함수를 호출하여 마지막 12개의 열에 해당하는 데이터를 가져옵니다.
result = get_last_12_columns(csv_file_path)

test_result = []

# 결과 출력
for row in result:
    if row == []:
        pass
    else:
        test_result.append(row)


test_result = test_result[1:]
first_colum = []
last_colum = []

for x in test_result:
    first_colum.append(round(int(float(x[1]))))
    last_colum.append(round(int(float(x[11]))/86400))


print(f"numMines : {first_colum}\n")
print(f"last_colum : {last_colum}")

# plt.plot(last_colum,first_colum)
# plt.xlabel('x last_colum')
# plt.ylabel('y first_colum')

df = pd.DataFrame({'numMines': first_colum, 'completionTime':last_colum})


# plt.style.use('white_background')
sns.set(style="white",palette="bright", font_scale=1.5)

sns.pairplot(df[['completionTime','numMines']], height=4)
plt.show()

#['totalTargets', 'numMines', 'numNonMines', 'numUndetected', 'numDetected', 'numClassified', 'numMILCOS', 'numNOMBOS', 'numNotClassified', 'numFalseNeg', 'numFalsePos', 'completionTime']
