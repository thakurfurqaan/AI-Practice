from dataclasses import dataclass

from leetcode.merge_accounts.solution1 import Solution


@dataclass
class TestCase:
    accounts: list[list]
    output: list[list]


s = Solution()


def run_test(tc: TestCase):
    res = s.accountsMerge(tc.accounts, tc.output)
    assert res == tc.output, f"Expected {tc.output}, got {res}"


def test_normal():
    run_test(
        TestCase(
            [
                ["John", "johnsmith@mail.com", "john_newyork@mail.com"],
                ["John", "johnsmith@mail.com", "john00@mail.com"],
                ["Mary", "mary@mail.com"],
                ["John", "johnnybravo@mail.com"],
            ],
            [
                [
                    "John",
                    "john00@mail.com",
                    "john_newyork@mail.com",
                    "johnsmith@mail.com",
                ],
                ["Mary", "mary@mail.com"],
                ["John", "johnnybravo@mail.com"],
            ],
        )
    )


def test_no_accounts_to_merge():
    run_test(
        TestCase(
            [
                ["Gabe", "Gabe0@m.co", "Gabe3@m.co", "Gabe1@m.co"],
                ["Kevin", "Kevin3@m.co", "Kevin5@m.co", "Kevin0@m.co"],
                ["Ethan", "Ethan5@m.co", "Ethan4@m.co", "Ethan0@m.co"],
                ["Hanzo", "Hanzo3@m.co", "Hanzo1@m.co", "Hanzo0@m.co"],
                ["Fern", "Fern5@m.co", "Fern1@m.co", "Fern0@m.co"],
            ],
            [
                ["Ethan", "Ethan0@m.co", "Ethan4@m.co", "Ethan5@m.co"],
                ["Gabe", "Gabe0@m.co", "Gabe1@m.co", "Gabe3@m.co"],
                ["Hanzo", "Hanzo0@m.co", "Hanzo1@m.co", "Hanzo3@m.co"],
                ["Kevin", "Kevin0@m.co", "Kevin3@m.co", "Kevin5@m.co"],
                ["Fern", "Fern0@m.co", "Fern1@m.co", "Fern5@m.co"],
            ],
        )
    )


def test_indirect_dependency_account():
    run_test(
        TestCase(
            [
                ["David", "David0@m.co", "David1@m.co"],
                ["David", "David3@m.co", "David4@m.co"],
                ["David", "David4@m.co", "David5@m.co"],
                ["David", "David2@m.co", "David3@m.co"],
                ["David", "David1@m.co", "David2@m.co"],
            ],
            [
                [
                    "David",
                    "David0@m.co",
                    "David1@m.co",
                    "David2@m.co",
                    "David3@m.co",
                    "David4@m.co",
                    "David5@m.co",
                ],
            ],
        )
    )
