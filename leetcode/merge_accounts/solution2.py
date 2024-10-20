from collections import defaultdict
from heapq import merge
from typing import List


class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:

        e2e: dict[str, set] = defaultdict(set)

        for account in accounts:
            name = account[0]
            emails = account[1::]
            first_email = emails[0]

            for email in emails:
                e2e[email].add(first_email)
                e2e[first_email].add(email)

        visited: set[str] = set()

        def dfs(merged_account: list[str], email: str):
            if email in visited:
                return
            visited.add(email)
            merged_account.append(email)
            emails = e2e[email]
            for email in emails:
                dfs(merged_account, email)

        res: list[list] = []
        for account in accounts:
            name = account[0]
            first_email = account[1]
            if first_email in visited:
                continue
            merged_account = [name]
            dfs(merged_account, first_email)
            merged_account[1::] = sorted(merged_account[1::])
            res.append(merged_account)
        return res
