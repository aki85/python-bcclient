import blockchain_request as bcr
import sys

bcrequest = bcr.BlockchainRequestClient()
print('--- リクエストを以下の形式で入力してください')
print('request to: port request (option)')
print('--- Example')
print('request to: 5000 mine')
print('request to: 5001 send target=5000 amount=1')
print('--- exitと入力すると終了します。')
request_input = ''
while request_input != 'exit':
    if request_input != '':
        try:
            bcrequest.request(request_input)
        except Exception as err:
            print(err)
            if str(type(err)) == "<class 'requests.exceptions.ConnectionError'>":
                print('Please check server')
            print('リクエストは許可されませんでした。')
        
    request_input = input('request to: ')