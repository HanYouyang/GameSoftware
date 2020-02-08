from collections import defaultdict

def accountsMerge(accounts):
    visitedAccounts = [False] * len(accounts)
    emailAccountsMap = defaultdict(list)# 转化成为图的关键步骤
    res = []

    for i, account in enumerate(accounts):
        for j in range(1, len(account)):
            email = account[j]
            emailAccountsMap[email].append(i)
    print(emailAccountsMap)

    def dfs(i, emails):
        if visitedAccounts[i]:
            return 
        visitedAccounts[i] = True
        for j in range(1, len(accounts[i])):
            email = accounts[i][j]
            emails.add(email)
            for neighbor in emailAccountsMap[email]:
                dfs(neighbor, emails)

    for i, account in enumerate(accounts):
        if visitedAccounts[i]:
            continue
        name, emails = account[0], set()
        dfs(i, emails)
        res.append([name] + sorted(emails))
    return res