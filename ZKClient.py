import requests
import json


class ZKClient:
    def __init__(self, network, address):
        '''
        Network (number) 1 -> mainnet, 3 -> ropsten
        '''
        _base = 'https://api.zks.app/'
        _network = network
        self.base = _base + str(network)
        self.address = address

    def request_get(self, endpoint, params={}):
        print(self.base + endpoint)
        return requests.get(self.base + endpoint, params).text

    def request_post(self, endpoint, data=[]):
        print(self.base + endpoint)
        return requests.post(self.base + endpoint, data).text

    def get_contact_address(self):
        return self.request_get('/contract-address')

    def get_token_list(self):
        return self.request_get('/tokens')

    def get_token_prices(self):
        return self.request_get('/tokens/price')

    def get_pair_list(self):
        return self.request_get('/pairs')

    def get_pair_prices(self):
        return self.request_get('/pairs/price')

    def get_account_balance(self):
        return self.request_get('/account/'+ self.address + '/balances')

    def get_account_info(self):
        return self.request_get('/account/' + self.address + '/info')

    def get_account_fee(self):
        return self.request_get('/account/' + self.address + '/fee')

    def get_transaction_list(self):
        return self.request_get('/txs')

    def get_transaction(self, tx_hash):
        return self.request_get('/tx/' + tx_hash)

    def post_submit_transaction(self):
        return self.request_post('/tx')
