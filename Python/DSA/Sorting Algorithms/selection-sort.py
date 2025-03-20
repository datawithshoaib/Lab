'''
selection sort Algorithm:
1. find out the minimum value.
2. swap minimum value to 0th position.
3. take sublist(except sorted part) and repeat step 1 and step 2 until list is completely sorted.
'''
# for non-duplicate values
list1 = [3, 5, 60, 30, 20, 40, 0]
print(list1)

for i in range(len(list1)):
    min_val = min(list1[i:])
    min_index = list1.index(min_val)
    list1[i], list1[min_index] = list1[min_index], list1[i]

print(list1)

# for duplicate values
