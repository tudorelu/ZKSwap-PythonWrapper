import requests
import json
from decimal import Decimal

class ZKSwapClient:

    def __init__(self, network, address):
        '''Constructor

                `network` - number  | the network with which to interact
                                    |   1 -> mainnet, 3 -> ropsten
                
                `address` - string  | the address from which to interact
        '''
        _base = 'https://api.zks.app/'
        _network = network
        self.base = _base + str(network)
        self.address = address
        self.tokens_by_id = None
        self.pairs_by_id = None
        self.populate_tokens_by_id()
        self.populate_pairs_by_id()


    def request_get(self, endpoint, params={}):
        ''' GET function '''
        return requests.get(self.base + endpoint, params).text


    def request_post(self, endpoint, data=[]):
        ''' POST function '''
        return requests.post(self.base + endpoint, data).text


    def get_contact_address(self):
        ''' Wrapper for the /contract-address endpoint '''
        return self.request_get('/contract-address')


    def get_token_list(self):
        ''' Wrapper for the /tokens endpoint '''
        return self.request_get('/tokens')


    def get_token_prices(self):
        ''' Wrapper for the /tokens/price endpoint '''
        return self.request_get('/tokens/price')


    def get_pairs_list(self):
        ''' Wrapper for the /pairs endpoint '''
        return self.request_get('/pairs')


    def get_pairs_prices(self):
        ''' Wrapper for the /pairs/prices endpoint '''
        return self.request_get('/pairs/price')


    def get_account_balance(self):
        ''' Wrapper for the /account/{address}/balances endpoint '''
        return self.request_get('/account/'+ self.address + '/balances')


    def get_account_info(self):
        ''' Wrapper for the /account/{address}/info endpoint '''
        return self.request_get('/account/' + self.address + '/info')


    def get_account_fee(self):
        ''' Wrapper for the /account/{address}/fee endpoint '''
        return self.request_get('/account/' + self.address + '/fee')


    def get_transaction_list(self):
        ''' Wrapper for the /txs endpoint '''
        return self.request_get('/txs')


    def get_transaction(self, tx_hash):
        ''' Wrapper for the /tx/{tx_hash} endpoint '''
        return self.request_get('/tx/' + tx_hash)


    def post_submit_transaction(self):
        ''' Wrapper for the /account/{tx} endpoint '''
        return self.request_post('/tx')


    def populate_tokens_by_id(self):
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
        tokens = json.loads(self.get_token_list())
        self.tokens_by_id = dict()
        for token in tokens['data']:
            # create an empty list of pairs inside the token dict
            token_data = token.copy()
            token_data['pairs'] = []
            # add the tokens to a dict indexable based on token id
            self.tokens_by_id[token['id']] = token_data


    def populate_pairs_by_id(self):
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
            self.pairs_by_id[pair['id']]['symbol_a'] = \
                self.tokens_by_id[pair['id_a']]['symbol']
            self.pairs_by_id[pair['id']]['symbol_b'] = \
                self.tokens_by_id[pair['id_b']]['symbol']


    def get_complete_info_all_pairs(self, update_info=False):
        ''' Calls multiple endpoints to gather comprehensive details
        on all the zkswap pairs. 

            `update_info` - bool  | whether to update the existing info
                in `self.tokens_by_id` & `self.pairs_by_id` or not

        Returns a list dicts containing info about all pair
        '''
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


    def get_complete_info_pair(self, pair_id):
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
        if pair_id not in list(self.pairs_by_id.keys()):
            self.populate_pairs_by_id()
            if pair_id not in list(self.pairs_by_id.keys()):
                raise Exception('Could not find pair id.')  

        to_return = self.get_complete_info_all_pairs(True)

        return to_return[pair_id]


    def get_complete_info_pair(self, symbol_a, symbol_b):
        ''' Gets comprehensive info on a single zkswap pair.
        
            `symbol_a` - string | one of the symbols of the pair
            `symbol_b` - string | the other symbol of the pair

            Calls the get_pairs_comprehensive_info(). 
            Raises error if `symbol_a` and `symbol_b` not found in the same pair

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
        
        all_pairs = self.get_complete_info_all_pairs(True)
        for pair_id in all_pairs.keys():
            pair = all_pairs[pair_id]
            if (symbol_a.lower() == pair['symbol_a'].lower() and \
                symbol_b.lower() == pair['symbol_b'].lower()) or \
                (symbol_b.lower() == pair['symbol_a'].lower() and \
                symbol_a.lower() == pair['symbol_b'].lower()):
                return pair

        raise Exception('Could not find pair containing both symbols.')


    def get_reserves(self, pair_id):
        ''' Gets the current reserves on a pair based on the {pair_id} '''
        pair = self.get_complete_info_pair(pair_id)
        return [pair['amount_a'], pair['amount_b']]


    def _get_amount_out(self, amount_in, reserve_in, reserve_out):
        ''' Given an input amount of an asset and pair reserves, 
        returns the maximum output amount of the other asset.
        
        Based on the Uniswap V2 formula:
        https://github.com/Uniswap/uniswap-v2-periphery/blob/dda62473e2da448bc9cb8f4514dadda4aeede5f4/contracts/libraries/UniswapV2Library.sol#L43
        '''
        assert amount_in > 0, 'UniswapV2Library: INSUFFICIENT_INPUT_AMOUNT'
        assert reserve_in > 0 and reserve_out > 0, 'UniswapV2Library: INSUFFICIENT_LIQUIDITY'
        amount_in_with_fee = amount_in * 997
        numerator = amount_in_with_fee * reserve_out
        denominator = reserve_in * 1000 + amount_in_with_fee
        amount_out = numerator / denominator
        return amount_out


    def _get_amount_in(self, amount_out, reserve_in, reserve_out):
        ''' Given an output amount of an asset and pair reserves, 
        returns a required input amount of the other asset.
        
        Based on the Uniswap V2 formula:
        https://github.com/Uniswap/uniswap-v2-periphery/blob/dda62473e2da448bc9cb8f4514dadda4aeede5f4/contracts/libraries/UniswapV2Library.sol#L53
        '''
        assert amount_out > 0, 'UniswapV2Library: INSUFFICIENT_OUTPUT_AMOUNT'
        assert reserve_in > 0 and reserve_out > 0, 'UniswapV2Library: INSUFFICIENT_LIQUIDITY'
        numerator = reserve_in * amount_out * 1000
        denominator = (reserve_out - amount_out) * 997
        amount_in = (numerator / denominator) + 1
        return amount_in


    def get_amount_in(self, amount_out, symbol_in, symbol_out):
        ''' Returns the amount of `symbol_in` required in order for the
        LP to return `amount_out` of `symbol_out`. Raises exceeption in 
        case the pool doesn't exist.
        '''
        pair = self.get_complete_info_pair(symbol_in, symbol_out)
        if symbol_in.lower() == pair['symbol_a'].lower():
            return self._get_amount_in(
                amount_out, 
                Decimal(pair['amount_a']), 
                Decimal(pair['amount_b']))
        else:
            return self._get_amount_in(
                amount_out, 
                Decimal(pair['amount_b']), 
                Decimal(pair['amount_a']))


    def get_amount_out(self, amount_in, symbol_in, symbol_out):
        ''' Returns the amount of `symbol_out` one would receive for
        `amount_in` of `symbol_in` sent to the LP. Raises exceeption 
        in case the pool doesn't exist.
        '''
        pair = self.get_complete_info_pair(symbol_in, symbol_out)
        to_return = None
        if symbol_in.lower() == pair['symbol_a'].lower():
            return self._get_amount_out(
                amount_in, 
                Decimal(pair['amount_a']), 
                Decimal(pair['amount_b']))
        else:
            return self._get_amount_out(
                amount_in, 
                Decimal(pair['amount_b']),
                Decimal(pair['amount_a']))
