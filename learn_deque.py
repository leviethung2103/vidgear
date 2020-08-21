import collections

# demostrate working of append(), appendleft(), pop(), pop

# initializing deque
de = collections.deque([1,2,3])
# <class 'collections.deque'>
print (type(de))

de.append(4)
de.appendleft(6)
de.pop()
de.popleft()

print (de)
