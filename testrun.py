"""
This is a really fun math question.

You have three random number generators RG2, RG3, RG7 at your disposal.

Given these, how do you create a random number generator RG42 as a mathematical combination of the least number of random number generators possible?

One answer is modeled below.

Think of RG42 as a 3D cube of dimensions 2,3,7. Index into the cube as a function of each of these numbers.

I tested my approach and showed that, for sufficiently large numbers, the probability of each result is approximately equal.

"""




import random

finDict={}
for x in xrange(10000000):
  RG2=random.randint(1,2)
  RG3=random.randint(1,3)
  RG7=random.randint(1,7)
  rand42=2*(RG3-1)+RG2+6*(RG7-1)
  if (rand42 in finDict):
    finDict[rand42]=finDict[rand42]+1
  else:
    finDict[rand42]=1

for x in xrange(1,43):
  t=abs(float(finDict[x]/10000000.0) - 1.0/42.0) < 0.001
  print t
