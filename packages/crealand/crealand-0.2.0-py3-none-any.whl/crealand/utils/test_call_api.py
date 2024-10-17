from utils.utils import call_api, call_api_async

def test_call_api():
    response = call_api('web-ide', 'apis.sayHello', ['hello'])
    print('call_api response: ', response)

def test_call_api_async():
    response = call_api_async('web-ide', 'apis.sayHello', ['hello'])
    if response:
        print('call_api response: True')
    else:
        print('call_api response: False')
