from ZKClient import ZKClient



# response = requests.get("https://api.zks.app/3/tokens")
# print(json.dumps(response.json(), sort_keys = False, indent = 4))
# print(response.json())


# TESTING CLASS

client = ZKClient(network = 3, address = '000x0')

# GET CONTRACT ADDRESS
print('get_contact_address ', client.get_contact_address())
print('get_token_list ', client.get_token_list())
print('get_token_prices', client.get_token_prices())
print('get_pair_list', client.get_pair_list())
print('get_pair_prices', client.get_pair_prices())
print('get_account_balance', client.get_account_balance())
print('get_account_info', client.get_account_info())
print('get_account_fee', client.get_account_fee())
print('get_transaction_list', client.get_transaction_list())
print('get_transaction', client.get_transaction(tx_hash = '000x0'))
print('post_submit_transaction', client.post_submit_transaction())
