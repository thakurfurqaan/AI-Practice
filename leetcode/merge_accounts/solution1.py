from typing import List


class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:

        e2n: dict[str, str] = {}
        e2e: dict[str, set] = {}

        for account in accounts:
            name = account[0]
            emails = account[1::]

            for email in emails:
                if email not in e2n:
                    e2n[email] = name

                if email in e2e:
                    e2e[email].update(emails)
                else:
                    e2e[email] = set(emails)

        cc: dict[int, set] = {}
        visited: set[str] = set()
        c = 1

        def dfs(email):
            if email in visited:
                return
            emails = e2e[email]
            cc[c].add(email)
            visited.add(email)
            for email in emails:
                dfs(email)

        for key, emails in e2e.items():
            if key in visited:
                continue
            cc[c] = set()
            dfs(key)
            c += 1

        res: list[list] = []

        for _, emails in cc.items():
            lemails = list(emails)
            name = e2n[lemails[0]]
            res.append([name] + sorted(lemails))

        return res
