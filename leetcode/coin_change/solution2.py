from typing import List


class Solution:

    def coinChange(self, coins: List[int], amount: int) -> int:

        memo = {coin: 1 for coin in coins}

        def find(balance, coins_used):
            if balance in memo:
                return coins_used + memo[balance]
            if balance == 0:
                return coins_used

            min_coins_required = balance + 1
            for coin in coins:
                if coin < balance:
                    coins_req = find(balance - coin, coins_used + 1)
                    if coins_req != -1:
                        min_coins_required = min(min_coins_required, coins_req)

            if min_coins_required < balance + 1:
                memo[balance] = min_coins_required
                return min_coins_required
            memo[balance] = -1
            return -1

        return find(amount, 0)
