# you can use this to sort strings too
def bubble_sort(arr):
    n = len(arr)
    for i in range(n-1):
        swapped = False
        for j in range(n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True

        if not swapped:
            break

if __name__ == '__main__':
    tests = [
        [5,9,2,1,67,34,88,34],
        [1,2,3,4,2],
        ["mona", "dhaval", "aamir", "tina", "chang"]
    ]

    for array in tests:
        bubble_sort(array)
        print(array)

