import random


def three_way_partition(array, low, high):
    check = low + 1
    pivot = array[low]
    while check <= high:
        if array[check] < pivot:
            temp = array[low]
            array[low] = array[check]
            array[check] = temp
            low += 1
            check += 1
        elif array[check] > pivot:
            temp = array[high]
            array[high] = array[check]
            array[check] = temp
            high -= 1
        else:
            check += 1
    return low, check


def quicksort(array, low, high):
    if low < high:
        left, right = three_way_partition(array, low, high)
        quicksort(array, low, left -1)
        quicksort(array, right, high)


def first_two(array, low, high):
    results = []
    results.append(array[low])
    if low < high:
        results.append(array[low+1])
    return results


def insert_values(array, index, inputs, low, high):
    for i in range(low, high+1):
        array[i] = 0
    for val in inputs:
        array[index] = val
        index += 1
    return index


def copy_used(array, index, left, use_index, right):
    while use_index >= left:
        array[index] = array[use_index]
        use_index -= 1
        index += 1
    if index > left:
        left = index
    while left <= right:
        array[left] = 0
        left += 1
    return index


array = [random.randint(1, 5) for i in range(40)]
print(array)
quicksort(array, 0, len(array)-1)
print(array)

left = 0
index = 0
while left < len(array):
    right = left
    while right < len(array) - 1 and array[left] == array[right+1]:
        right += 1
    print("{} -> {} = {} {}".format(left, right, array[left], array[right]))
    use_index = random.randint(left + 1, right)
    print(index, left, use_index)
    index = copy_used(array, index, left, use_index, right)
    left = right + 1
    print(array)
