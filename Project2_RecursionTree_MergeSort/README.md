# Recursion Tree for Merge Sort

## Description

This project demonstrates the recursion tree of the Merge Sort
algorithm using an array of 8 elements.

The project shows how Merge Sort recursively divides the array into
smaller subarrays until single-element arrays are obtained and then
merges the subarrays back in sorted order.

Input array:

[8, 3, 2, 9, 7, 1, 5, 4]

Final sorted array:

[1, 2, 3, 4, 5, 7, 8, 9]

## Algorithm

1. Start with the given array.
2. If the array contains one or zero elements, it is already sorted.
3. Find the middle position of the array.
4. Divide the array into two halves.
5. Recursively apply Merge Sort to the left half.
6. Recursively apply Merge Sort to the right half.
7. Merge the two sorted halves.
8. Continue the merging process until the complete array is sorted.

## Pseudocode

MergeSort(A):

    if length(A) <= 1:
        return A

    mid = length(A) / 2

    left = A[0 : mid]
    right = A[mid : end]

    left = MergeSort(left)
    right = MergeSort(right)

    return Merge(left, right)

## Prompt Used

Create a professional recursion tree visualization for Merge Sort
using the array [8, 3, 2, 9, 7, 1, 5, 4].

Show the original array at the root, recursively divide the array
into two halves until single-element arrays are reached, and then
show the merging process from bottom to top until the final sorted
array [1, 2, 3, 4, 5, 7, 8, 9].

Use a clean academic style with clear arrows, labels, and levels.
The visualization should be suitable for a DAA college project report.

## Output

The recursion tree visualization is provided in:

Visualization.png

The visualization shows the recursive division of the 8-element
array and the merging process until the final sorted array is
obtained.

## Learning Outcome

- Understood the recursive nature of Merge Sort.
- Learned how an array is divided recursively.
- Understood the merging process.
- Learned how recursion trees represent algorithm execution.
- Practiced AI-based visualization and GitHub documentation.