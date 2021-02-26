import math

def add_commas(num):
 num = str(num)
 num = list(reversed(num))
 for l in reversed(range(len(num))):
  if l % 3 == 0 and l != 0:
   num.insert(l, ',')
 return ''.join(reversed(num))

def total(base, mult, level):
 return sum(math.ceil(base*(mult**x)) for x in range(level))
