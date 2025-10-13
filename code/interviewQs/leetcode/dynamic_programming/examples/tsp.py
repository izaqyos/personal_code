def tsp(distances):
    n = len(distances)
    dp = [[float('inf')] * (1 << n) for _ in range(n)]

    # Base case: starting at city 0 with no other cities visited
    dp[0][1] = 0

    for mask in range(1, 1 << n):  # Iterate through all possible sets of cities
        for last in range(n):  # Iterate through possible last cities
            if mask & (1 << last):  # Check if the last city is in the current set
                for prev in range(n):  # Iterate through possible previous cities
                    if mask & (1 << prev):  # Check if the previous city is in the set
                        dp[last][mask] = min(
                            dp[last][mask],
                            dp[prev][mask ^ (1 << last)] + distances[prev][last]
                        )

    # Find the minimum distance returning to city 0
    result = float('inf')
    for i in range(1, n):
        result = min(result, dp[i][(1 << n) - 1] + distances[i][0])

    return result

# Example usage
distances = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]
shortest_distance = tsp(distances)
print(f"Shortest distance: {shortest_distance}")
