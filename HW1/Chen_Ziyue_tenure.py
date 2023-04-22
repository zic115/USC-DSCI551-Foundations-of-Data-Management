import sys
import requests

k = sys.argv[1]

url = 'https://dsci551-7645b-default-rtdb.firebaseio.com/.json?orderBy="tenure"&startAt=' + k
response = requests.get(url)

IDs = response.json().keys()
num = len(IDs)
print(num)
