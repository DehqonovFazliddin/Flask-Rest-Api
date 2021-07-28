import requests

url = "http://127.0.0.1:5000/"
# response = requests.put(url+'book/3', {"name":"Algorithm", "author": "N/A", "cost":500, "num_of_book":2})
# print(response.json())
# input()
# response = requests.delete(url+'book/3')
# print(response)
# response = requests.patch(url+'book/1', {"name": "Algorithm"})
# print(response.json())
response = requests.get(url+'book/1')
print(response.json())