# Exercise: Load Balancing Algorithms

## Objective
Understand and compare different load balancing algorithms.

## Problem Statement
You have 3 web servers with the following specifications:
- Server A: 4 CPU cores, handles up to 1000 req/s
- Server B: 2 CPU cores, handles up to 500 req/s  
- Server C: 8 CPU cores, handles up to 2000 req/s

You receive 10 sequential requests.

## Tasks

### Task 1: Round Robin
Distribute the 10 requests using Round Robin. Where does each request go?

```
Request 1: ___
Request 2: ___
Request 3: ___
Request 4: ___
Request 5: ___
Request 6: ___
Request 7: ___
Request 8: ___
Request 9: ___
Request 10: ___
```

### Task 2: Weighted Round Robin
Given the server capacities, assign appropriate weights and distribute the same 10 requests.

What weights would you assign?
- Server A weight: ___
- Server B weight: ___
- Server C weight: ___

Distribute the 10 requests with these weights:
```
Request 1: ___
Request 2: ___
... (continue for all 10)
```

### Task 3: Analysis Questions

1. If Server B goes down, how would each algorithm handle this?

2. If requests have varying complexity (some take 10ms, others take 1000ms), which algorithm would perform better?

3. What additional information would you need to implement "Least Connections" algorithm?

---

<details>
<summary>Hints</summary>

- For weighted round robin, consider capacity ratios: A:B:C = 1000:500:2000 = 2:1:4
- Total weight = 7, so in 7 requests: A gets 2, B gets 1, C gets 4

</details>

<details>
<summary>Solution</summary>

### Task 1: Round Robin
```
Request 1: A
Request 2: B
Request 3: C
Request 4: A
Request 5: B
Request 6: C
Request 7: A
Request 8: B
Request 9: C
Request 10: A
```

Distribution: A=4, B=3, C=3 (nearly equal, ignoring capacity)

### Task 2: Weighted Round Robin
Weights: A=2, B=1, C=4 (based on capacity ratio)

```
Request 1: C (weight 4)
Request 2: C
Request 3: C
Request 4: C
Request 5: A (weight 2)
Request 6: A
Request 7: B (weight 1)
Request 8: C (cycle restarts)
Request 9: C
Request 10: C
```

This better utilizes available capacity.

### Task 3: Analysis
1. Both would simply remove B from the pool after health check fails
2. Least Connections would perform better as it considers actual load
3. Need: current active connections per server, connection completion tracking

</details>
