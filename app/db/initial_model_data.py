import requests

login_url = 'http://localhost:8282/api/v1/login/access-token'
request_body = {'username': 'gyrosg_admin@gyrosg.com', 'password': 'gyrosg_admin'}
response_json = requests.post(login_url, data=request_body).json()
token = response_json['access_token']

headers = {'Authorization': 'Bearer ' + token}

# Create bike models
create_model_url = 'http://localhost:8282/api/v1/bike_models'

models = [{'name': "Vespa LX150"},
{'name': "KTM Duke 200"},
{'name': "Vespa GTS300 Super"},
{'name': "KTM Duke 390"},
{'name': "Honda MSX125"},
{'name': "Yamaha RXZ"}]


for model in models:
    response_json = requests.post(create_model_url,json=model,headers=headers).json()
    print(response_json)