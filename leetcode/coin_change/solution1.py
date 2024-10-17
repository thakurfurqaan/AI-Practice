from typing import List


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:

        if amount == 0:
            return 0

        coins = sorted(coins, reverse=True)
        res = 0

        for coin in coins:
            if coin > amount:
                continue
            no_of_coins = amount // coin
            res += no_of_coins
            amount -= no_of_coins * coin
            print(coin, no_of_coins, amount, res, coins)
            if amount == 0:
                return res
        return -1
