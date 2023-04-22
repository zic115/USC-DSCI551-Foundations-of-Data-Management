import sys
import requests

k = sys.argv[1]

url = 'https://dsci551-7645b-default-rtdb.firebaseio.com/.json?orderBy="Churn"&equalTo="Yes"&limitToFirst=' + k
response = requests.get(url)

IDs = response.json().keys()
print(IDs)
