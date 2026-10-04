def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2

    left = arr[:mid]
    right = arr[mid:]

    print("Dividing:", arr)
    print("  Left :", left)
    print("  Right:", right)

    left = merge_sort(left)
    right = merge_sort(right)

    return merge(left, right)


def merge(left, right):
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):

        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


arr = [8, 3, 2, 9, 7, 1, 5, 4]

print("Original array:", arr)

sorted_array = merge_sort(arr)

print("Sorted array:", sorted_array)