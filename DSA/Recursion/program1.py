# 1. Recursive function to count down from a given number to 1
def countdown(i):
    print(i)
    if i <= 1: # base case
        return
    countdown(i - 1) # recursive case

# countdown(5)

# 2. Recursive function to count the number of items in a list
def count_items(list):
    if list == []:
        return 0
    return 1 + count_items(list[1:])
    
# res = count_items([1, 2, 3, 4, 5])
# print("No. of items:", res)

# 3. Recursive function to find the maximum number in a list
def find_max(list):
    # base case
    if len(list) == 1:
        return list[0]
    
    # recursive case
    max_rest = find_max(list[1:])
    
    if list[0] > max_rest:
        return list[0]
    else:
        return max_rest

# res = find_max([1, 2, 3, 50, 30])

# print("Max number:", res)

#  4. Binary search is a D&C algorithm. Can you come up with the base case and recursive case for binary search?
def bin_srch(arr, left, right, tar):
    # base case: element not found
    if left > right:
        return -1
    
    mid = (left + right)//2

    # base case: element found
    if arr[mid] == tar:
        return mid

    # recursive case
    if tar < arr[mid]:
        return bin_srch(arr, left, mid-1, tar)
    else:
        return bin_srch(arr, mid+1, right, tar)

arr = [1, 3, 40, 60, 80, 120]
res = bin_srch(arr, 0, len(arr)-1, 120)
print("Binary Search result: ", res)


# 5. Recursive function to do the sum of items in a list
def sum_items(arr):
    if arr == []:
        return 0
    return arr[0] + sum_items(arr[1:])

# res = sum_items([1, 5, 6, 8])
# print("Sum of items:", res)
