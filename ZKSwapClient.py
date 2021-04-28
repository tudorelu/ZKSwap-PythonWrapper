import requests
import json

class ZKSwapClient:
    def __init__(self, network, address):
        '''
            {network} - number  | the network with which to interact
                                |   1 -> mainnet, 3 -> ropsten
            {address} - string  | the address from which to interact
        '''
        _base = 'https://api.zks.app/'
        _network = network
        self.base = _base + str(network)
        self.address = address
        self.tokens_by_id = None
        self.pairs_by_id = None
        self.populate_tokens_by_id()
        self.populate_pairs_by_id()

    ''' GET function '''
    def request_get(self, endpoint, params={}):
        return requests.get(self.base + endpoint, params).text

    ''' POST function '''
    def request_post(self, endpoint, data=[]):
        return requests.post(self.base + endpoint, data).text

    ''' Wrapper for the /contract-address endpoint '''
    def get_contact_address(self):
        return self.request_get('/contract-address')

    ''' Wrapper for the /tokens endpoint '''
    def get_token_list(self):
        return self.request_get('/tokens')

    ''' Wrapper for the /tokens/price endpoint '''
    def get_token_prices(self):
        return self.request_get('/tokens/price')

    ''' Wrapper for the /pairs endpoint '''
    def get_pairs_list(self):
        return self.request_get('/pairs')

    ''' Wrapper for the /pairs/prices endpoint '''
    def get_pairs_prices(self):
        return self.request_get('/pairs/price')

    ''' Wrapper for the /account/{address}/balances endpoint '''
    def get_account_balance(self):
        return self.request_get('/account/'+ self.address + '/balances')

    ''' Wrapper for the /account/{address}/info endpoint '''
    def get_account_info(self):
        return self.request_get('/account/' + self.address + '/info')

    ''' Wrapper for the /account/{address}/fee endpoint '''
    def get_account_fee(self):
        return self.request_get('/account/' + self.address + '/fee')

    ''' Wrapper for the /txs endpoint '''
    def get_transaction_list(self):
        return self.request_get('/txs')

    ''' Wrapper for the /tx/{tx_hash} endpoint '''
    def get_transaction(self, tx_hash):
        return self.request_get('/tx/' + tx_hash)

    ''' Wrapper for the /account/{tx} endpoint '''
    def post_submit_transaction(self):
        return self.request_post('/tx')

    ''' Populates a dict with all tokens avaiable on zkswap.

        Useful to do because this list doesn't change very often. 
        Adds the tokens in a dictionary with the keys being the 
        ids of the tokens as specified by zkswap.

        {
            'address': '0xe4815ae53b124e7263f08dcdbbb757d41ed658c6',
            'decimals': 18,
            'icon': 'https://s.zks.app/icons/ZKS.png',
            'id': 1,
            'pairs': [128 ..., 229], # ids of all pairs this token is part of
            'symbol': 'ZKS'
        }
    '''
    def populate_tokens_by_id(self):
        tokens = json.loads(self.get_token_list())
        self.tokens_by_id = dict()
        for token in tokens['data']:
            # create an empty list of pairs inside the token dict
            token_data = token.copy()
            token_data['pairs'] = []
            # add the tokens to a dict indexable based on token id
            self.tokens_by_id[token['id']] = token_data

    ''' Populates a dict with all pairs avaiable on zkswap.

        Useful to do because this list doesn't change very often. 
        Adds the pairs in a dictionary with the keys being the 
        ids of the pairs as specified by zkswap, together with some 
        extra info.

        
        {
            'address': '0xf005ab93a5ede376de898f0980cc63b460273e3d',
            'anchored': 29,
            'decimals': 18,
            'id': 128,
            'id_a': 1,
            'id_b': 29,
            'symbol': 'liquidity_1_29',
            'symbol_a': 'ZKS',
            'symbol_b': 'USDT'
        }
    '''
    def populate_pairs_by_id(self):
        # request pairs data
        pairs = json.loads(self.get_pairs_list())
        self.pairs_by_id = dict()
        
        for pair in pairs['data']:
            self.pairs_by_id[pair['id']] = pair
            if self.tokens_by_id == None \
                or pair['id_a'] not in self.tokens_by_id.keys() \
                or pair['id_b'] not in self.tokens_by_id.keys():
                self.populate_tokens_by_id()

            # append the pair id to the list of pairs inside the tokens it contains
            self.tokens_by_id[pair['id_a']]['pairs'].append(pair['id'])
            self.tokens_by_id[pair['id_b']]['pairs'].append(pair['id'])
            self.pairs_by_id[pair['id']]['symbol_a'] = self.tokens_by_id[pair['id_a']]['symbol']
            self.pairs_by_id[pair['id']]['symbol_b'] = self.tokens_by_id[pair['id_b']]['symbol']

    ''' 
    Calls multiple endpoints to gather comprehensive details
    on all the zkswap pairs. 

        {update_info} - bool  | whether to update the existing info
            in tokens_by_id & pairs_by_id

        Returns - a list dicts containing info about all pair
    '''
    def get_complete_info_all_pairs(self, update_info=False):
        to_return = dict()

        if self.pairs_by_id == None or update_info:
            self.populate_pairs_by_id()
            self.populate_tokens_by_id()
        
        pairs_prices = json.loads(self.get_pairs_prices())
        for pp in pairs_prices['data']:
            pair = self.pairs_by_id[pp['id']].copy()
            pair['amount_a'] = pp['amount_a']
            pair['amount_b'] = pp['amount_b']
            pair['price'] = pp['price']
            pair['total_supply'] = pp['totalSupply']
            to_return[pp['id']] = pair
        return to_return

    ''' Gets comprehensive info on a single zkswap pair.
        
        {pair_id} - number | the zkswap id of the pair

        Calls the get_pairs_comprehensive_info(). 
        Raises error if {pair_id} not found

        Returns - a dict containing info about the pair
        {
            'address': '0xf005ab93a5ede376de898f0980cc63b460273e3d',
            'amount_a': '5933722.80177120620850816',
            'amount_b': '14764422.084323',
            'anchored': 29,
            'decimals': 18,
            'id': 128,
            'id_a': 1,
            'id_b': 29,
            'price': '14098427.316840369567373',
            'symbol': 'liquidity_1_29',
            'symbol_a': 'ZKS',
            'symbol_b': 'USDT',
            'total_supply': '2.094477880761510055'
        }
    '''
    def get_complete_info_pair(self, pair_id):
        if pair_id not in list(self.pairs_by_id.keys()):
            self.populate_pairs_by_id()
            if pair_id not in list(self.pairs_by_id.keys()):
                raise Exception('Could not find pair id.')  

        to_return = self.get_complete_info_all_pairs(True)

        return to_return[pair_id]

