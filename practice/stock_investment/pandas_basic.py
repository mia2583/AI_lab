import pandas as pd

# 1. DataFrame 생성
df = pd.DataFrame()
df["Name"] = ["Jacky", "Steven", "George"]
df["Age"] = [38, 25, 23]
df["Driver"] = [True, False, True]

print("1. DataFrame 생성하기")
print(df)
print()

# 2. 파이썬 dictionary 사용해서 DataFrame 만들기
data = {
    "Name":["Jacky", "Steven", "George"],
    "Age": [38, 25, 23],
    "Driver": [True, False, True]
}

df = pd.DataFrame(data)

print("2. dictionary로 DataFrame 생성하기")
print(df)
print()

# 3. Series 접근
print("3-1. Series 접근하기 - Age")
print(df["Age"])
print()

print("3-2. Series 접근하기 - Age, Driver")
print(df[["Age", "Driver"]])
print()

# 4. index에 이름 설정하기
df.index.name = "index"
print("4. index에 이름 설정하기")
print(df)
print()

# 5. DataFrame 열 추가/수정/삭제
print("5-1. 열 추가")
df["Location"] = ["Area 1", "Area 2", "Area 3"]
print(df)
print()

print("5-2. 열 이름 변경")
df = df.rename(columns={"Name": "Person"})
print(df)
print()

print("5-3. 열 삭제")
df = df.drop(columns="Location")
print(df)
print()

# 6. DataFrame 행 추가/수정/삭제
print("6-1. 행 추가")
data = {
    "Person": ["Harry"],
    "Age": [10],
    "Driver": [False]
}
new_df = pd.DataFrame(data, index=["4"])
df = pd.concat([df, new_df])
print(df)
print()

print("6-1. 행 선택")
print(df[0:2])
print()

print("6-2. 행 선택 - loc")
print(df.loc[2]) # 인덱스가 2인 데이터 접근
print(df.loc[2, "Person"]) # 인덱스 2의 Person 데이터 접근
print()

print("6-3. 행 선택 - iloc")
print(df.iloc[1]) # 1번째 데이터 접근
print(df.iloc[1, 1]) # 1번째의 1번 데이터 접근
print()

print("6-3. 행 선택 - 조건")
print(df["Age"] > 25)
print(df[df["Age"] > 25])
print()
