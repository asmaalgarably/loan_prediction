import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
import pickle

url='https://raw.githubusercontent.com/subashgandyer/datasets/master/loan_prediction.csv'
data=pd.read_csv(url)
data=data.dropna()
print(data.columns)

x = data.drop('Loan_Status', axis=1)
y = data['Loan_Status']
lb=LabelEncoder()
for col in data.columns:
    if data[col].dtype=='object':
        data[col]=lb.fit_transform(data[col])

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=44)

scaler=StandardScaler()
x_train=scaler.fit_transform(x_train)
x_test=scaler.transform(x_test)

model=LogisticRegression()
model.fit(x_train,y_train)

y_pred=model.predict(x_test)

print("Training",model.score(x_train,y_train)) 
print("Testing",model.score(x_test,y_test)) 

with open('train_model.pkl','wb') as f:
    pickle.dump(model,f)
with open('scaler.pkl','wb') as f:
    pickle.dump(scaler,f)

