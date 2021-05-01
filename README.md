# ZKSwap-PythonWrapper

Python wrapper around the [zkswap REST API](https://en.wiki.zks.org/interact-with-zkswap/restful-api)

```py

    def request_get(self, endpoint, params={}):
      ''' GET function '''


    def request_post(self, endpoint, data=[]):
      ''' POST function '''


    def get_contact_address(self):
      ''' Wrapper for the /contract-address endpoint '''


    def get_token_list(self):
      ''' Wrapper for the /tokens endpoint '''


    def get_token_prices(self):
      ''' Wrapper for the /tokens/price endpoint '''


    def get_pairs_list(self):
      ''' Wrapper for the /pairs endpoint '''


    def get_pairs_prices(self):
      ''' Wrapper for the /pairs/prices endpoint '''


    def get_account_balance(self):
      ''' Wrapper for the /account/{address}/balances endpoint'''


    def get_account_info(self):
      ''' Wrapper for the /account/{address}/info endpoint '''


    def get_account_fee(self):
      ''' Wrapper for the /account/{address}/fee endpoint '''


    def get_transaction_list(self):
      ''' Wrapper for the /txs endpoint '''


    def get_transaction(self, tx_hash):
      ''' Wrapper for the /tx/{tx_hash} endpoint '''


    def post_submit_transaction(self):
      ''' Wrapper for the /account/{tx} endpoint '''


    def populate_tokens_by_id(self):
      ''' 
      Populates a dict with all tokens avaiable on zkswap.

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


    def populate_pairs_by_id(self):
      ''' 
      Populates a dict with all pairs avaiable on zkswap.

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


    def get_complete_info_all_pairs(self, update_info=False):
      ''' 
      Calls multiple endpoints to gather comprehensive details
      on all the zkswap pairs. 

          {update_info} - bool  | whether to update the existing info
              in tokens_by_id & pairs_by_id

          Returns - a list dicts containing info about all pair
      '''


    def get_complete_info_pair(self, pair_id):
      ''' 
      Gets comprehensive info on a single zkswap pair.
          
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


    def get_reserves(self, pair_id):
      ''' Gets the current reserves on a pair based on the {pair_id} '''
        

    def _get_amount_out(self, amount_in, reserve_in, reserve_out):
      ''' Given an input amount of an asset and pair reserves, 
      returns the maximum output amount of the other asset.
      
      Based on the Uniswap V2 formula:
      https://github.com/Uniswap/uniswap-v2-periphery/blob/dda62473e2da448bc9cb8f4514dadda4aeede5f4/contracts/libraries/UniswapV2Library.sol#L43
      '''


    def _get_amount_in(self, amount_out, reserve_in, reserve_out):
      ''' Given an output amount of an asset and pair reserves, 
      returns a required input amount of the other asset.
      
      Based on the Uniswap V2 formula:
      https://github.com/Uniswap/uniswap-v2-periphery/blob/dda62473e2da448bc9cb8f4514dadda4aeede5f4/contracts/libraries/UniswapV2Library.sol#L53
      '''


    def get_amount_in(self, amount_out, symbol_in, symbol_out):
      ''' Returns the amount of `symbol_in` required in order for the
      LP to return `amount_out` of `symbol_out`. Raises exceeption in 
      case the pool doesn't exist.
      '''


    def get_amount_out(self, amount_in, symbol_in, symbol_out):
      ''' Returns the amount of `symbol_out` one would receive for
      `amount_in` of `symbol_in` sent to the LP. Raises exceeption 
      in case the pool doesn't exist.
      '''

```
