# Finds & prints all triplets of pairs 
# through which triangular arbitrage can be done 
# 
# IE Prints:
#
# Found Triangular Arbitrage Pairs:
#
# ids:  158 179 206
# ETH / ZKS
# ETH / HT
# HT / ZKS
#
# ids:  158 181 208
# ETH / ZKS
# ETH / REN
# REN / ZKS

from ZKSwapClient import ZKSwapClient

client = ZKSwapClient(network = 1, address = '000x0')
all_pairs = client.get_complete_info_all_pairs()
triangular_pairs = []

# Loop through the dict of pairs trice
for pair_id, pair in all_pairs.items():
    for pair_id_2, pair_2 in all_pairs.items():
      for pair_id_3, pair_3 in all_pairs.items():
          if pair_id != pair_id_2 \
            and pair_id != pair_id_3 \
            and pair_id_2 != pair_id_3:

            # check if the number of unique symbols in these 3 pairs is 3
            all_symbols = set(sorted([
                pair['symbol_a'], pair['symbol_b'], 
                pair_2['symbol_a'], pair_2['symbol_b'], 
                pair_3['symbol_a'], pair_3['symbol_b']]))
            
            # print if new triplet found
            if len(all_symbols) == 3 and all_symbols not in triangular_pairs:
                triangular_pairs.append(all_symbols)
                print('Found Triangular Arbitrage Pairs:')
                print('ids: ', pair_id, pair_id_2, pair_id_3)
                print(pair['symbol_a'], '/', pair['symbol_b'])
                print(pair_2['symbol_a'], '/', pair_2['symbol_b'])
                print(pair_3['symbol_a'], '/', pair_3['symbol_b'])
