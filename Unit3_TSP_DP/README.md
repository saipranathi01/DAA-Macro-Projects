# Traveling Salesperson Problem using Dynamic Programming

## 1. Project Title

**Traveling Salesperson Problem (TSP) using Dynamic Programming**

## 2. Aim

To solve the Traveling Salesperson Problem for four cities using Dynamic Programming and visualize the DP state transitions.

## 3. Problem Statement

Given a set of cities and the travel cost between every pair of cities, find the minimum-cost tour that:

- Starts from a specified city.
- Visits every other city exactly once.
- Returns to the starting city.

For this project, four cities are considered: **A, B, C, and D**.

## 4. Distance Matrix

The following distance matrix is used:

| From / To | A | B | C | D |
|---|---:|---:|---:|---:|
| **A** | 0 | 10 | 15 | 20 |
| **B** | 10 | 0 | 35 | 25 |
| **C** | 15 | 35 | 0 | 30 |
| **D** | 20 | 25 | 30 | 0 |

## 5. Dynamic Programming Approach

The DP state is represented as:

`DP[S][j]`

where:

- `S` is the subset of cities that have been visited.
- `j` is the city where the current route ends.
- `DP[S][j]` represents the minimum cost of starting from A, visiting all cities in `S`, and ending at city `j`.

The starting state is:

`DP[{A}][A] = 0`

### Recurrence

For every state, the recurrence is:

`DP[S][j] = min(DP[S - {j}][i] + distance[i][j])`

where `i` is a previously visited city.

After all cities have been visited, the cost of returning to A is added.

## 6. Bitmask Representation

The implementation uses bitmasks to represent subsets of cities.

| City | Bit |
|---|---|
| A | 0001 |
| B | 0010 |
| C | 0100 |
| D | 1000 |

For example:

- `0001` represents `{A}`
- `0011` represents `{A,B}`
- `0101` represents `{A,C}`
- `1111` represents `{A,B,C,D}`

Since there are four cities, there are:

`2^4 = 16`

possible subsets.

## 7. Algorithm / Pseudocode

```text
TSP-DP(distance, n)

1. Initialize DP table with infinity.

2. Set the base state:
       DP[{A}][A] = 0

3. For every subset S containing A:
       For every city j in S, except A:
           previousSubset = S - {j}

           For every city i in previousSubset:
               newCost = DP[previousSubset][i] + distance[i][j]

               If newCost is smaller than DP[S][j]:
                   DP[S][j] = newCost
                   Store i as the parent city

4. Consider the complete subset {A,B,C,D}.

5. For every possible final city j:
       totalCost = DP[{A,B,C,D}][j] + distance[j][A]

6. Select the minimum totalCost.

7. Use the stored parent information to reconstruct
   the optimal route.

8. Display the minimum cost and route.
```

## 8. DP Table Obtained

The C implementation produces the following DP values:

| Subset | A | B | C | D |
|---|---:|---:|---:|---:|
| `{A}` | 0 | - | - | - |
| `{A,B}` | - | 10 | - | - |
| `{A,C}` | - | - | 15 | - |
| `{A,B,C}` | - | 50 | 45 | - |
| `{A,D}` | - | - | - | 20 |
| `{A,B,D}` | - | 45 | - | 35 |
| `{A,C,D}` | - | - | 50 | 45 |
| `{A,B,C,D}` | - | 70 | 65 | 75 |

The table shows how solutions for smaller subsets are reused to calculate solutions for larger subsets.

## 9. Final Result

The final DP state is:

- Ending at B: `70 + 10 = 80`
- Ending at C: `65 + 15 = 80`
- Ending at D: `75 + 20 = 95`

Therefore:

**Minimum TSP Cost = 80**

One optimal route obtained from the program is:

`A → C → D → B → A`

Its total cost is:

`15 + 30 + 25 + 10 = 80`

Another route with the same minimum cost is:

`A → B → D → C → A`

with total cost:

`10 + 25 + 30 + 15 = 80`

## 10. Visualization

The visualization shows the progression of DP states from smaller subsets to the complete set of cities.

The major stages are:

```text
{A}
  ↓
{A,B}, {A,C}, {A,D}
  ↓
{A,B,C}, {A,B,D}, {A,C,D}
  ↓
{A,B,C,D}
  ↓
Return to A
  ↓
Minimum Cost = 80
```

The arrows represent the transitions from previously calculated DP states to new states.

The generated visualization is included in:

**`Visualization.png`**

## 11. AI Prompt Used

The prompt used to generate the visualization is included in:

**`Prompt.txt`**

The prompt specifies the distance matrix, DP states, calculated values, recurrence, transitions, and final result so that the generated visualization corresponds to the implemented algorithm.

## 12. C Implementation

The complete implementation is provided in:

**`tsp.c`**

The program:

1. Initializes the distance matrix.
2. Initializes the DP and parent tables.
3. Calculates the DP states using bitmasking.
4. Displays the DP table.
5. Finds the minimum tour cost.
6. Reconstructs and displays an optimal route.

## 13. Time Complexity

The Dynamic Programming solution has a time complexity of:

**O(n² × 2ⁿ)**

This is significantly better than checking all possible tours directly, although TSP remains an exponential-time problem.

## 14. Space Complexity

The DP table requires:

**O(n × 2ⁿ)**

space.

The parent table used for route reconstruction also requires:

**O(n × 2ⁿ)**

space.

## 15. Files in This Project

```text
TSP/
├── tsp.c
├── Prompt.txt
├── Visualization.png
└── README.md
```

### File Description

| File | Description |
|---|---|
| `tsp.c` | C implementation of TSP using Dynamic Programming |
| `Prompt.txt` | AI prompt used to generate the visualization |
| `Visualization.png` | DP state-transition visualization |
| `README.md` | Project documentation |

## 16. Conclusion

The Traveling Salesperson Problem was solved using Dynamic Programming by dividing the problem into overlapping subproblems represented by subsets of cities. The DP table stores the minimum cost for each state and avoids recalculating the same subproblems.

For the given four-city example, the minimum tour cost is **80**, demonstrating how Dynamic Programming can systematically find an optimal TSP tour.
