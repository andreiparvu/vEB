#!/usr/bin/python

import math
import random

def getActualValue(x, nrC, nrN):
  return nrC * nrN + x

class vEB:
  def __init__(self, n):
    self.min, self.max = None, None
    self.n = n

    self.nrN = int(math.ceil(n ** 0.5))

    self.summary, self.clusters = None, None
    if n > 2:
      self.summary = vEB(self.nrN)
      self.clusters = [vEB(self.nrN) for i in xrange(self.nrN)]

  def find(self, x):
    if self.min == x or self.max == x:
      return True

    if self.min == self.max:
      return False

    return self.clusters[x / self.nrN].find(x % self.nrN)


  def add(self, x):
    if self.min == None:
      self.min, self.max = x, x
      return

    if self.min == self.max: # only one element
      if x < self.min:
        self.min = x
      else:
        self.max = x

      return

    # element is less than the minimum, or greater than the maximum
    if x < self.min:
      x, self.min = self.min, x
    elif x > self.max:
      x, self.max = self.max, x
    nrC = x / self.nrN

    self.clusters[nrC].add(x % self.nrN)

    if self.summary.find(nrC) == False:
      self.summary.add(nrC)

  def deleteFromCluster(self, nrC, x):
    self.clusters[nrC].delete(x);
    if self.clusters[nrC].min == None:
      self.summary.delete(nrC)

  def delete(self, x):
    if x == self.min:
      if x == self.max:
        self.min, self.max = None, None
        return

      if self.summary == None or self.summary.min == None:
        self.min = self.max
      else:
        y = self.clusters[self.summary.min].min
        self.min = getActualValue(y, self.summary.min, self.nrN)
        self.deleteFromCluster(self.summary.min, y)

      return

    if x == self.max:
      if self.summary == None or self.summary.max == None:
        self.max = self.min
      else:
        y = self.clusters[self.summary.max].max
        self.max = getActualValue(y, self.summary.max, self.nrN)
        self.deleteFromCluster(self.summary.max, y)

      return

    self.deleteFromCluster(x / self.nrN, x % self.nrN)

  def next(self, x):
    if self.min == None or x >= self.max:
      return None
    if x < self.min:
      return self.min

    if x == self.min:
      if self.summary == None:
        return self.max

    nrC = x / self.nrN

    rez = self.clusters[nrC].next(x % self.nrN)

    if rez == None:
      nrC = self.summary.next(nrC)

      if nrC == None:
        return self.max

      rez = self.clusters[nrC].min

    return getActualValue(rez, nrC, self.nrN)

def main():
  v = vEB(10000)

  l = [False for i in xrange(10000)]

  for i in xrange(1500):
    x = int(random.random() * 10000)
    if l[x] == False:
      v.add(x)
      l[x] = True
      print "add %d" % x

  for i in xrange(100000):
    case = int(random.random() * 4)
    x = int(random.random() * 10000)

    if case == 0:
      if l[x] == False:
        v.add(x)
        l[x] = True
        print "add %d" % x
    elif case == 1:
      if l[x] == v.find(x):
        print "Find ok %d" % l[x]
      else:
        print "Find bad %d" % x
    elif case == 2:
      if l[x] == True:
        l[x] = False
        v.delete(x)
        print "delete %d" % x
    else:
      if l[x] == True:
        found = None
        for i in xrange(x + 1, 10000):
          if l[i] == True:
            found = i
            break

        if found == v.next(x):
          if found != None:
            print "Next ok %d" % found
          else:
            print "Next found None"
        else:
          print "Next bad"


if __name__ == "__main__":
  main()