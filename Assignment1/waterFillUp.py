#  assignment 1

#  brute force first

# for every element
    # find max left height and max right height
    #using those, add min(left,right)-height of element to running total
""" 
inputt = [3,0,2,0,4]

res=0


for i in range(len(inputt)):
   # print(str(i) + "asdfasdf")

    left = inputt[i]
    for le in range(i):
        left = max(left, inputt[le])
    #print(left)

    right = inputt[i]
    for ri in range(i+1,len(inputt)):
        right = max(right, inputt[ri])
    #print(right)

    res+=min(left,right)-inputt[i]
    #print("res", res)


print(res)
 """

#
#   This is the closest thing I could get to dynamic programming. I couldn't think of a method to store / design sub problems other than precalculating highest left wall and highest right wall at each index.
#

#inputt = [3,0,2,0,4]
#inputt = [1,0,1]
def waterFillUp(inputt):
    res=0
    n = len(inputt)

    leftHigh = [0]*n
    rightHigh = [0]*n

    leftHigh[0] = inputt[0]
    for i in range(1,n):
    
        leftHigh[i]=max(leftHigh[i-1], inputt[i])


    rightHigh[n-1] = inputt[n-1]
    for i in reversed(range(n-1)):#len(inputt),0, -1):
    
        rightHigh[i]=max(rightHigh[i+1], inputt[i])
    

    for i in range(n):

        res+=min(leftHigh[i],rightHigh[i])-inputt[i]
        #print("res", res)

    #print(leftHigh, rightHigh)
    return(res)


print(waterFillUp([1,0,1]),"     ----   Expected Answer: 1.    Input:[1,0,1]")
print(waterFillUp([4,1,2,6]),"     ----   Expected Answer: 5.    Input:[4,1,2,6]")
print(waterFillUp([6,5,4,3,2,1]),"     ----   Expected Answer: 0.    Input:[6,5,4,3,2,1]")

