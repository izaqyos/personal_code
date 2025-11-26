"""
Week 8, Day 6: State Machine DP

Learning Objectives:
- Master state machine DP pattern
- Learn stock trading problems
- Practice multi-state transitions
- Understand constraint-based DP
- Solve problems with state tracking

Time: 10-15 minutes
"""

# ============================================================
# EXERCISE 1: Best Time to Buy/Sell Stock (One Transaction)
# ============================================================

def stock_one_transaction():
    """
    Maximum profit with one transaction.
    
    State: holding or not holding stock
    """
    print("--- Exercise 1: Stock (One Transaction) ---")
    
    def max_profit(prices):
        """Max profit with at most one transaction"""
        if not prices:
            return 0
        
        min_price = float('inf')
        max_profit_val = 0
        
        for price in prices:
            min_price = min(min_price, price)
            max_profit_val = max(max_profit_val, price - min_price)
        
        return max_profit_val
    
    def max_profit_dp(prices):
        """DP approach with states"""
        if not prices:
            return 0
        
        # States: not_holding, holding
        not_holding = 0
        holding = -prices[0]
        
        for i in range(1, len(prices)):
            not_holding = max(not_holding, holding + prices[i])
            holding = max(holding, -prices[i])
        
        return not_holding
    
    test_cases = [
        [7, 1, 5, 3, 6, 4],
        [7, 6, 4, 3, 1],
        [1, 2, 3, 4, 5]
    ]
    
    for prices in test_cases:
        profit = max_profit(prices)
        print(f"Prices: {prices}")
        print(f"  Max profit: {profit}\n")
    
    print()

# ============================================================
# EXERCISE 2: Stock (Unlimited Transactions)
# ============================================================

def stock_unlimited():
    """
    Maximum profit with unlimited transactions.
    
    TODO: Can buy/sell multiple times
    """
    print("--- Exercise 2: Stock (Unlimited Transactions) ---")
    
    def max_profit(prices):
        """Max profit with unlimited transactions"""
        if not prices:
            return 0
        
        # Greedy: Buy before every increase
        profit = 0
        for i in range(1, len(prices)):
            if prices[i] > prices[i-1]:
                profit += prices[i] - prices[i-1]
        
        return profit
    
    def max_profit_dp(prices):
        """DP approach"""
        if not prices:
            return 0
        
        not_holding = 0
        holding = -prices[0]
        
        for i in range(1, len(prices)):
            new_not_holding = max(not_holding, holding + prices[i])
            new_holding = max(holding, not_holding - prices[i])
            not_holding, holding = new_not_holding, new_holding
        
        return not_holding
    
    test_cases = [
        [7, 1, 5, 3, 6, 4],
        [1, 2, 3, 4, 5],
        [7, 6, 4, 3, 1]
    ]
    
    for prices in test_cases:
        profit = max_profit(prices)
        print(f"Prices: {prices}")
        print(f"  Max profit: {profit}\n")
    
    print()

# ============================================================
# EXERCISE 3: Stock (K Transactions)
# ============================================================

def stock_k_transactions():
    """
    Maximum profit with at most k transactions.
    
    TODO: Limited number of transactions
    """
    print("--- Exercise 3: Stock (K Transactions) ---")
    
    def max_profit(k, prices):
        """Max profit with at most k transactions"""
        if not prices or k == 0:
            return 0
        
        n = len(prices)
        
        # If k >= n/2, unlimited transactions
        if k >= n // 2:
            profit = 0
            for i in range(1, n):
                profit += max(0, prices[i] - prices[i-1])
            return profit
        
        # dp[t][i] = max profit with at most t transactions by day i
        # States: buy[t] = max profit after buying in transaction t
        #         sell[t] = max profit after selling in transaction t
        buy = [-float('inf')] * (k + 1)
        sell = [0] * (k + 1)
        
        for price in prices:
            for t in range(k, 0, -1):
                sell[t] = max(sell[t], buy[t] + price)
                buy[t] = max(buy[t], sell[t-1] - price)
        
        return sell[k]
    
    test_cases = [
        (2, [2, 4, 1]),
        (2, [3, 2, 6, 5, 0, 3]),
        (1, [1, 2, 3, 4, 5])
    ]
    
    for k, prices in test_cases:
        profit = max_profit(k, prices)
        print(f"K: {k}, Prices: {prices}")
        print(f"  Max profit: {profit}\n")
    
    print()

# ============================================================
# EXERCISE 4: Stock with Cooldown
# ============================================================

def stock_cooldown():
    """
    Stock trading with cooldown period.
    
    TODO: Must wait 1 day after selling
    """
    print("--- Exercise 4: Stock with Cooldown ---")
    
    def max_profit(prices):
        """Max profit with cooldown"""
        if not prices:
            return 0
        
        # States: holding, not_holding, cooldown
        holding = -prices[0]
        not_holding = 0
        cooldown = 0
        
        for i in range(1, len(prices)):
            new_holding = max(holding, cooldown - prices[i])
            new_not_holding = max(not_holding, cooldown)
            new_cooldown = holding + prices[i]
            
            holding = new_holding
            not_holding = new_not_holding
            cooldown = new_cooldown
        
        return max(not_holding, cooldown)
    
    test_cases = [
        [1, 2, 3, 0, 2],
        [1, 2, 4],
        [2, 1, 4]
    ]
    
    for prices in test_cases:
        profit = max_profit(prices)
        print(f"Prices: {prices}")
        print(f"  Max profit: {profit}\n")
    
    print()

# ============================================================
# EXERCISE 5: Stock with Transaction Fee
# ============================================================

def stock_with_fee():
    """
    Stock trading with transaction fee.
    
    TODO: Pay fee on each transaction
    """
    print("--- Exercise 5: Stock with Transaction Fee ---")
    
    def max_profit(prices, fee):
        """Max profit with transaction fee"""
        if not prices:
            return 0
        
        not_holding = 0
        holding = -prices[0]
        
        for i in range(1, len(prices)):
            new_not_holding = max(not_holding, holding + prices[i] - fee)
            new_holding = max(holding, not_holding - prices[i])
            not_holding, holding = new_not_holding, new_holding
        
        return not_holding
    
    test_cases = [
        ([1, 3, 2, 8, 4, 9], 2),
        ([1, 3, 7, 5, 10, 3], 3)
    ]
    
    for prices, fee in test_cases:
        profit = max_profit(prices, fee)
        print(f"Prices: {prices}, Fee: {fee}")
        print(f"  Max profit: {profit}\n")
    
    print()

# ============================================================
# EXERCISE 6: Paint House
# ============================================================

def paint_house():
    """
    Minimum cost to paint houses with color constraints.
    
    TODO: Adjacent houses can't have same color
    """
    print("--- Exercise 6: Paint House ---")
    
    def min_cost(costs):
        """Min cost to paint all houses"""
        if not costs:
            return 0
        
        # States: cost if last house painted with color 0, 1, or 2
        prev = costs[0][:]
        
        for i in range(1, len(costs)):
            curr = [0] * 3
            curr[0] = costs[i][0] + min(prev[1], prev[2])
            curr[1] = costs[i][1] + min(prev[0], prev[2])
            curr[2] = costs[i][2] + min(prev[0], prev[1])
            prev = curr
        
        return min(prev)
    
    test_cases = [
        [[17, 2, 17], [16, 16, 5], [14, 3, 19]],
        [[7, 6, 2]]
    ]
    
    for costs in test_cases:
        min_cost_val = min_cost(costs)
        print(f"Costs: {costs}")
        print(f"  Min cost: {min_cost_val}\n")
    
    print()

# ============================================================
# EXERCISE 7: Real-World Scenario - Job Scheduling
# ============================================================

def job_scheduling():
    """
    Maximum profit from job scheduling with states.
    
    TODO: Can't work on overlapping jobs
    """
    print("--- Exercise 7: Job Scheduling ---")
    
    def job_scheduling_profit(start_time, end_time, profit):
        """Max profit from non-overlapping jobs"""
        jobs = sorted(zip(end_time, start_time, profit))
        n = len(jobs)
        
        # dp[i] = max profit considering jobs 0..i
        dp = [0] * n
        dp[0] = jobs[0][2]
        
        for i in range(1, n):
            # Take current job
            take = jobs[i][2]
            
            # Find latest non-overlapping job
            for j in range(i - 1, -1, -1):
                if jobs[j][0] <= jobs[i][1]:
                    take += dp[j]
                    break
            
            # Don't take current job
            skip = dp[i-1]
            
            dp[i] = max(take, skip)
        
        return dp[n-1]
    
    start = [1, 2, 3, 3]
    end = [3, 4, 5, 6]
    profit = [50, 10, 40, 70]
    
    print("Jobs (start, end, profit):")
    for s, e, p in zip(start, end, profit):
        print(f"  ({s}, {e}, ${p})")
    
    max_profit_val = job_scheduling_profit(start, end, profit)
    print(f"\nMax profit: ${max_profit_val}")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    State Machine DP Complexity:
    
    Pattern:
    - Define states (holding, not_holding, cooldown, etc.)
    - Define transitions between states
    - Track best value for each state
    - Answer is best final state
    
    Time Complexity:
    - O(n × states × transitions)
    - Usually O(n) with constant states
    
    Space Complexity:
    - O(states) with optimization
    - Only need previous state values
    
    Key Characteristics:
    - Clear state definitions
    - Well-defined transitions
    - Constraints encoded in states
    - Often optimizable to O(1) space
    
    Common Problems:
    - Stock trading (various constraints)
    - House painting (color constraints)
    - Job scheduling (time constraints)
    - Game states
    
    Best Practices:
    - Draw state diagram
    - List all transitions
    - Initialize base states
    - Update in correct order
    
    Debugging Tips:
    - Verify state transitions
    - Check initialization
    - Test with small examples
    - Draw state flow
    
    Security Considerations:
    - Validate state values
    - Check transition logic
    - Handle edge cases
    - Prevent invalid states
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 8, Day 6: State Machine DP")
    print("=" * 60)
    print()
    
    stock_one_transaction()
    stock_unlimited()
    stock_k_transactions()
    stock_cooldown()
    stock_with_fee()
    paint_house()
    job_scheduling()
    
    print("=" * 60)
    print("✅ Day 6 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. Define clear states and transitions")
    print("2. Track best value for each state")
    print("3. Often optimizable to O(1) space")
    print("4. Common in constraint-based problems")


