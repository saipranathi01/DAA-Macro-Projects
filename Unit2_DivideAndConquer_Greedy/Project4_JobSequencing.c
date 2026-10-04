#include <stdio.h>

// Structure to store information about a job
struct Job
{
    char id;
    int deadline;
    int profit;
};

// Function to sort jobs by profit in descending order
void sortJobs(struct Job jobs[], int n)
{
    int i, j;
    struct Job temp;

    for (i = 0; i < n - 1; i++)
    {
        for (j = 0; j < n - i - 1; j++)
        {
            if (jobs[j].profit < jobs[j + 1].profit)
            {
                // Swap the jobs
                temp = jobs[j];
                jobs[j] = jobs[j + 1];
                jobs[j + 1] = temp;
            }
        }
    }
}

// Function to perform Job Sequencing
void jobSequencing(struct Job jobs[], int n)
{
    int i, j;
    int maxDeadline = 0;
    int totalProfit = 0;

    // Find the maximum deadline
    for (i = 0; i < n; i++)
    {
        if (jobs[i].deadline > maxDeadline)
        {
            maxDeadline = jobs[i].deadline;
        }
    }

    // Array to store scheduled jobs
    char slot[maxDeadline + 1];

    // Initially all slots are empty
    for (i = 0; i <= maxDeadline; i++)
    {
        slot[i] = '-';
    }

    // Sort jobs according to profit
    sortJobs(jobs, n);

    // Try to schedule each job
    for (i = 0; i < n; i++)
    {
        // Start from the job's deadline
        // and move backwards
        for (j = jobs[i].deadline; j >= 1; j--)
        {
            if (slot[j] == '-')
            {
                // Schedule the job
                slot[j] = jobs[i].id;

                // Add its profit
                totalProfit = totalProfit + jobs[i].profit;

                // Move to the next job
                break;
            }
        }
    }

    // Display the final schedule
    printf("\nFinal Job Schedule:\n");

    for (i = 1; i <= maxDeadline; i++)
    {
        if (slot[i] != '-')
        {
            printf("Time Slot %d -> Job %c\n", i, slot[i]);
        }
        else
        {
            printf("Time Slot %d -> Empty\n", i);
        }
    }

    // Display maximum profit
    printf("\nMaximum Profit = %d\n", totalProfit);
}

int main()
{
    // Number of jobs
    int n = 4;

    // Job details
    struct Job jobs[4] =
    {
        {'A', 2, 100},
        {'B', 1, 50},
        {'C', 2, 80},
        {'D', 1, 40}
    };

    printf("Greedy Job Sequencing with Deadlines\n");
    printf("------------------------------------\n");

    printf("\nJobs:\n");
    printf("Job\tDeadline\tProfit\n");

    for (int i = 0; i < n; i++)
    {
        printf("%c\t%d\t\t%d\n",
               jobs[i].id,
               jobs[i].deadline,
               jobs[i].profit);
    }

    // Call Job Sequencing
    jobSequencing(jobs, n);

    return 0;
}