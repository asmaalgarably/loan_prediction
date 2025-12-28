from fastapi  import FastAPI
import pickle
from pydantic import BaseModel
import numpy as np 

model=pickle.load(open('train_model.pkl','rb'))
scale=pickle.load(open('scaler.pkl','rb'))

app=FastAPI()

class loadData(BaseModel):
    Gender: int
    Married: int
    Dependents: int
    Education: int
    Self_Employed: int
    ApplicantIncome: float
    CoapplicantIncome: float
    LoanAmount: float
    Loan_Amount_Term: float
    Credit_History: float
    Property_Area: int


@app.post('/predict', response_model=None)
def load_Data(data:loadData):
    input_data = np.array([[
        data.Gender, data.Married, data.Dependents, data.Education,
        data.Self_Employed, data.ApplicantIncome, data.CoapplicantIncome,
        data.LoanAmount, data.Loan_Amount_Term, data.Credit_History, data.Property_Area
    ]])

    input_scale=scale.transform(input_data)
    predction=model.predict(input_scale)

    status="OK"if predction[0]==1 else "NO"
    return {"loan_sataus":status}
