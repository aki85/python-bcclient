import json
import requests

class BlockchainRequestClient(object):
    json_header = {'Content-Type': 'application/json'}
    root_uri = 'http://localhost'
    addresses = {}
    def __init__(self):
        pass

    def request(self, *request_input):
        valid, port, action, options = self.valid_request(*request_input)
        if valid:
            if action == 'mine':
                self.mine(port)
            elif action == 'chain':
                self.chain(port)
            elif action in ['send', 'transaction']:
                self.send(port, options)
            elif action in ['register', 'know']:
                self.register(port, options)
            elif action in ['resolve', 'load']:
                self.load(port)
            elif action in ['reboot', 'reset', 'restart']:
                self.reboot(port)
            else:
                self.error('Bad action')
        else:
            self.error('Bad request')


    def valid_request(self, *request_input):
        if len(request_input) == 1:
            request_input = request_input[0].split()
            if len(request_input) != 1:
                return self.valid_request(*request_input)
            else:
                # 一つの引数で、分割できなかった
                pass
            
        elif len(request_input) >= 2:
            try:
                port = int(request_input[0])
                action = request_input[1]
                options = {}
                if len(request_input) >= 3:
                    for option in request_input[2:]:
                        key, value = option.split('=')
                        options[key] = value
                return True, port, action, options
            except:
                # 複数の引数だったが、形式があっていなかった
                pass
        return False, None, None, None

        
        
    def mine(self, port):
        response = requests.get(self.make_uri(port) + '/mine').json()
        self.json_print(response)
        self.save_address(port, self.get_miner(response))
        
        
    def send(self, port, options):
        valid, payload = self.resolve_send_options(port, options)
        if valid:
            response = requests.post(self.make_uri(port) + '/transactions/new', json.dumps(payload), headers=self.json_header).json()
            self.json_print(response)
        else:
            self.error('Bad options')


    def resolve_send_options(self, port, options):
        valid = True
        for option in ['target', 'amount']:
            valid = valid if option in options.keys() else False
        if valid:
            target_port = int(options['target'])
            amount = int(options['amount'])
            if port == target_port:
                return False, None
            else:
                try:
                    payload = {
                        'sender': self.addresses[port],
                        'recipient': self.addresses[target_port],
                        'amount': amount
                    }
                except:
                    self.error('No address. Please mine all port.')
                return True, payload
        else:
            return False, None
    
    def chain(self, port):
        response = requests.get(self.make_uri(port) + '/chain').json()
        self.json_print(response)
    
    def register(self, port, options):
        valid, params = self.resolve_register_options(port, options)
        if valid:
            response = requests.post(self.make_uri(port) + '/nodes/register', json.dumps(params), headers=self.json_header).json()
            self.json_print(response)
        else:
            self.error('Bad options')


    def resolve_register_options(self, port, options):
        if 'target' in options.keys():
            target_ports = list(map(int, options['target'].split(',')))
            if port in target_ports:
                return False, None
            else:
                target_nodes = list(map(lambda port: self.make_uri(port), target_ports))
                return True, {'nodes': target_nodes}
        else:
            return False, None

    def load(self, port):
        response = requests.get(self.make_uri(port) + '/nodes/resolve').json()
        self.json_print(response)

    def reboot(self, port):
        response = requests.get(self.make_uri(port) + '/reboot').json()
        self.json_print(response)



    # utility
    def get_miner(self, response):
        return response['transactions'][0]['recipient']

    def save_address(self, port, address):
        self.addresses[port] = address

    def make_uri(self, port):
        return self.root_uri + ':' + str(port)

    def json_print(self, obj):
        print(json.dumps(obj, indent=4))

    def error(self, err):
        raise Exception(err)


if __name__ == '__main__':
    pass