walking = [
    [0.5, 0.5,  0,  0,  0,  0,  0],
    [0,   0,    0,  0.5,  0.5,  0,  0],
    [0,   0,    0.5,  0,  0,  0.5,  0]
]

teleporting = [
    [0, 0.5,  0.5,  0,  0,  0,  0],
    [0,   0,    0.25,  0.75,  0,  0,  0],
    [0,   0,    0,  0,  0,  0.5,  0.5]
]
rewards = [-0.1, -0.1, -0.1, -4, 2, 5, -2]

N = len(rewards) 

def utility(n, s_idx, y, utility_memo):
    s_idx -= 1
    if n == 0:
        return rewards[s_idx]
    if utility_memo[n][s_idx] is not None:
        return utility_memo[n][s_idx]

    working_sum = 0
    for j in range(N):
        working_sum += walking[s_idx][j] * utility(n-1, j, y, utility_memo)
    walking_utility = rewards[s_idx] + y * working_sum

    teleporting_sum = 0
    for j in range(N):
        teleporting_sum += teleporting[s_idx][j] * utility(n-1, j, y,utility_memo)
    teleporting_utility = rewards[s_idx] + y * teleporting_sum
    ans = max(teleporting_utility, walking_utility)
    memo[n] [s_idx] = ans
    return ans

if __name__ == '__main__':
    memo = defaultdict(lambda : defaultdict(lambda: None))

    utility(1,2,1,memo)
