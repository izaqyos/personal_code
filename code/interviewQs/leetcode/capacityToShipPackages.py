"""
LC 1011 - Capacity To Ship Packages Within D Days (Medium)

A conveyor belt has packages that must be shipped from one port to another within `days` days.
The i-th package has weight weights[i]. Each day, we load the ship with packages in the order
given by weights. We may not load more weight than the maximum weight capacity of the ship.

Return the least weight capacity of the ship that will result in all the packages being shipped
within `days` days.

Example 1:
    Input: weights = [1,2,3,4,5,6,7,8,9,10], days = 5
    Output: 15
    Explanation: 1st day: 1,2,3,4,5 · 2nd: 6,7 · 3rd: 8 · 4th: 9 · 5th: 10.
    Packages must be shipped in order (splitting into (2,3,4,5), (1,6,7), ... is not allowed).

Example 2:
    Input: weights = [3,2,2,4,1,4], days = 3
    Output: 6
    Explanation: 1st day: 3,2 · 2nd: 2,4 · 3rd: 1,4

Example 3:
    Input: weights = [1,2,3,1,1], days = 4
    Output: 3
    Explanation: 1st day: 1 · 2nd: 2 · 3rd: 3 · 4th: 1,1

Constraints:
    1 <= days <= weights.length <= 5 * 10^4
    1 <= weights[i] <= 500
"""


def ship_within_days(weights: list[int], days: int) -> int:
    pass


if __name__ == "__main__":
    cases = [
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5, 15),
        ([3, 2, 2, 4, 1, 4], 3, 6),
        ([1, 2, 3, 1, 1], 4, 3),
        ([10], 1, 10),
        ([1, 1, 1, 1], 4, 1),
        ([1, 1, 1, 1], 1, 4),
        ([5, 1, 1, 1], 2, 5),
    ]
    passed = 0
    for weights, days, expected in cases:
        got = ship_within_days(weights, days)
        assert got == expected, f"weights={weights} days={days}: expected {expected}, got {got}"
        passed += 1
    print(f"{passed}/{len(cases)} passed")
