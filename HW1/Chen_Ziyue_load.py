import pandas as pd
import requests

df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")
df = df[df.SeniorCitizen == 1]
data = df.set_index("customerID").to_json(orient = "index")

requests.put('https://dsci551-7645b-default-rtdb.firebaseio.com/.json', data)
