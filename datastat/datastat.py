# This codes used to deal with "test.dat"
import sys

if len(sys.argv) < 2:
    print "usage: python do.py filename"
    sys.exit()

testFile = open(sys.argv[1])
count = 0
realCount = 0
maxNum = 0
re = []
for i in range(0, 1000):
    re.append(0)
for line in testFile:
    count += 1
    if (len(line) == 0):
	continue

    lineData = line.split()
    if (len(lineData) < 2 or "total" == lineData[1]):
	continue

    realCount += 1

    num=int(lineData[0])
    if (maxNum < num):
	maxNum = num
    re[num] += 1

testFile.close()

print "count="+str(count)
print "realCount="+str(realCount)

print "maxNum ="+str(maxNum)

total = 0
reFile = open("retest.txt", "w")
reFile.write("tagnum\t\tpics\n")
for i in range(0, maxNum+1):
    if (re[i] > 0):
	reFile.write(str(i)+"\t\t"+str(re[i])+'\n')
	total += re[i] * i
reFile.close()

print "total=" + str(total)
print "average=" + str(total/realCount)
