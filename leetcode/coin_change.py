from dataclasses import dataclass
from typing import List


class Solution1:
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


class Solution2:

    def coinChange(self, coins: List[int], amount: int) -> int:

        memo = {coin: 1 for coin in coins}

        def find(balance, coins_used):
            if balance in memo:
                return coins_used + memo[balance]

            min_coins_required = float("inf")
            for coin in coins:
                if coin < balance:
                    coins_req = find(balance - coin, coins_used + 1)
                    min_coins_required = min(min_coins_required, coins_req)

            memo[balance] = min_coins_required

        find(amount, 0)
        if amount in memo:
            return memo[amount]
        return -1


@dataclass
class TestCase:
    coins: list
    amount: int = 0
    output: int = 0


s = Solution1()


def run_test(tc: TestCase):
    res = s.coinChange(tc.coins, tc.amount)
    assert res == tc.output, f"Expected {tc.output}, got {res}"


def test_coin_less_than_amount():
    run_test(TestCase([1, 2, 5], 11, 3))


def test_greedy():
    run_test(TestCase([1, 2, 5], 11, 3))


def test_amount_zero():
    run_test(TestCase([1], 0, 0))


def test_tricky():
    run_test(
        TestCase(
            [186, 419, 83, 408],
            6249,
            20,
        )
    )
