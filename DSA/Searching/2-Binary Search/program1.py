def binarySearch(myArray, myTarget):
    left = 0
    right = len(myArray)-1

    while left <= right:
        mid = (left + right)//2

        if myArray[mid] == myTarget:
            return mid
        
        if myArray[mid] < myTarget:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

# example
arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
target = 5

result = binarySearch(arr, target)

if result != -1:
    print("Value", target, "found at index", result)
else:
    print("Value", target, "not found")
