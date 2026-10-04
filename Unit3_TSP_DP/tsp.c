#include <stdio.h>
#include <limits.h>

#define N 4
#define TOTAL_STATES 16
#define INF 999999

int distance[N][N] = {
    {0, 10, 15, 20},
    {10, 0, 35, 25},
    {15, 35, 0, 30},
    {20, 25, 30, 0}
};

int dp[TOTAL_STATES][N];
int parent[TOTAL_STATES][N];

int main()
{
    int i, j, mask, previousMask;
    int minCost, finalCity;
    int currentCity, previousCity;
    int route[N + 1];
    int routeIndex;

    /* Initialize DP table */
    for (mask = 0; mask < TOTAL_STATES; mask++)
    {
        for (j = 0; j < N; j++)
        {
            dp[mask][j] = INF;
            parent[mask][j] = -1;
        }
    }

    /* Base case: start from city A */
    dp[1][0] = 0;

    /*
       Build DP table.
       Bit 0 = A
       Bit 1 = B
       Bit 2 = C
       Bit 3 = D
    */
    for (mask = 1; mask < TOTAL_STATES; mask++)
    {
        /* Every valid route must contain starting city A */
        if ((mask & 1) == 0)
            continue;

        for (j = 1; j < N; j++)
        {
            /* Check whether city j is in the current subset */
            if ((mask & (1 << j)) == 0)
                continue;

            previousMask = mask ^ (1 << j);

            for (i = 0; i < N; i++)
            {
                /* Check whether city i was visited previously */
                if ((previousMask & (1 << i)) == 0)
                    continue;

                if (dp[previousMask][i] != INF)
                {
                    int newCost;

                    newCost = dp[previousMask][i] + distance[i][j];

                    if (newCost < dp[mask][j])
                    {
                        dp[mask][j] = newCost;
                        parent[mask][j] = i;
                    }
                }
            }
        }
    }

    /* Display DP table */
    printf("\n============================================\n");
    printf("          TSP DYNAMIC PROGRAMMING TABLE\n");
    printf("============================================\n");

    printf("\nSubset\t\tA\tB\tC\tD\n");
    printf("--------------------------------------------\n");

    for (mask = 1; mask < TOTAL_STATES; mask++)
    {
        if ((mask & 1) == 0)
            continue;

        printf("{");

        if (mask & 1)
            printf("A");
        if (mask & 2)
            printf("B");
        if (mask & 4)
            printf("C");
        if (mask & 8)
            printf("D");

        printf("}\t\t");

        for (j = 0; j < N; j++)
        {
            if (dp[mask][j] == INF)
                printf("-\t");
            else
                printf("%d\t", dp[mask][j]);
        }

        printf("\n");
    }

    /* Find the best final city and return to A */
    mask = TOTAL_STATES - 1;
    minCost = INF;
    finalCity = -1;

    for (j = 1; j < N; j++)
    {
        int totalCost;

        totalCost = dp[mask][j] + distance[j][0];

        if (totalCost < minCost)
        {
            minCost = totalCost;
            finalCity = j;
        }
    }

    /* Reconstruct optimal route */
    routeIndex = N;
    route[routeIndex] = 0;

    currentCity = finalCity;

    while (currentCity != 0)
    {
        routeIndex--;
        route[routeIndex] = currentCity;

        previousCity = parent[mask][currentCity];
        mask = mask ^ (1 << currentCity);
        currentCity = previousCity;
    }

    route[0] = 0;

    printf("\n============================================\n");
    printf("              FINAL RESULT\n");
    printf("============================================\n");

    printf("\nMinimum TSP Cost: %d\n", minCost);

    printf("Optimal Route: ");

    for (i = 0; i < N; i++)
    {
        printf("%c", 'A' + route[i]);

        if (i < N)
            printf(" -> ");
    }

    printf("A\n");

    return 0;
}
