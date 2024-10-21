from dataclasses import dataclass

from leetcode.coin_change.solution2 import Solution


@dataclass
class TestCase:
    coins: list
    amount: int = 0
    output: int = 0


s = Solution()


def run_test(tc: TestCase):
    res = s.coinChange(tc.coins, tc.amount)
    assert res == tc.output, f"Expected {tc.output}, got {res}"


def test_coin_less_than_amount():
    run_test(TestCase([2], 3, -1))


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
