#Accept a list containing numbers. Sort the list using Insertion sort. Thereafter accept
#a number and display the position where that number is found(Use Binary Search).
#Also display suitable message ,if the number is not found in the list. (use Functions).
n = int(input('enter number of elements - '))
L = []
for i in range(n):
    L.append(int(input('enter number - ')))
search = int(input('enter element to be seacrhed for - '))

def InsertionSort(L, n):
    for i in range(1, n):
        j = i
        while L[j-1] > L[j] and j>0:
            L[j-1], L[j] = L[j], L[j-1]
            j -= 1
    return L

def BinarySearch(L, n, search):
    u , l = n-1, 0
    while l <= u:
        m = (u+l)//2
        if search > L[m]:
            l = m+1
        elif search < L[m]:
            u = m-1
        else:
            print('search item is in', m+1, 'position')
            break
    if search not in L:
        print('number not found in list!')

sorted_L = InsertionSort(L, n)
print('sorted list - ', sorted_L)
BinarySearch(sorted_L, n, search)

    
