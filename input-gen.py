import random

n = 15000

s = ''.join(random.choices(['a', 'b'], weights=[10000,1], k=n))

f = open("input15000.txt", "w")
f.write(s)
f.close()
