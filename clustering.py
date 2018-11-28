# kmeans.py


# CS 451 HW 5

# Names: Julia Jaschke and Mira Chugh

import csv
import numpy as np
import random

filename = '37-00027_UOF-P_2014-2016_prepped.csv'

filename2 = 'interest_prepped.csv'


def main():
    """Main Program"""

    x = ReadFile(filename2)
    #
    incidences = getCountries(filename)
    #print(len(incidences)) #9483
    #print(incidences)


    #
    #KMeans(x , 20)
    #
    runKMeans(x, 25 , 1 , incidences)
    #toFile(x , 25 , 1 , incidences, "FPTRIAL.csv")

    #convertToNumerical(filename2)



def convertToNumerical(file):

    cols = {}
    for i in range(1,19):
        cols[i] = set()

    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        headers = (next(reader))[1:]                    # headers of the columns x1 - xn
        for line in reader:
            for j in range(1,19):
                (cols[j]).add(line[j])

    for k in range(1,19):
        cols[k] = list(cols[k])


    print(cols)
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        headers = (next(reader))[1:]                    # headers of the columns x1 - xn
        for line in reader:
            for j in range(1,19):
                curr = cols[j]
                line[j] = curr.index(line[j])





def ReadFile(filename):
    """Read in CSV file,
    output a list x for all the datapoints,
    each element of x is a NumPy vector with 16
    elements, one for each country"""

    x = []                                                                      # initialize x


    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        #headers = (next(reader))[1:]
        #print(headers)                                         # remove headers
        for line in reader:

            line = [float(i) for i in line]                                 # get line of country data
            x.append(np.array(line))                                            # add to x
    return x


def getCountries(filename):
    """Get list of countries from filename"""
    country = []                                                                #initialize country list
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)                                            # read csv file
        #headers = (next(reader))[1:]                                            # remove headers
        for line in reader:
            if line[0] != "RIN":
                country.append(line[0])                                             # add country

    return country



def squaredDis(vector1 , vector2):
    """return squared distance between vector1 and vector2"""
    distance = np.sum(np.subtract(vector1,vector2)**2)                          # calc the distance
    return distance


def IndexClosestCluster(xi, listCentroids):
    """Returns the index of the closest cluster centroid for xi"""
    #list centroids = mu
    #xi should be one of those things with 16 numbers in it
    minD = squaredDis(xi, listCentroids[0])                                     # initialize the minimum distance to the distance between first centroid and xi
    index = 0                                                                   # set index to zero
    for i in range(1, len(listCentroids)):                                      # now iterate starting at 1
        centroidDis = squaredDis(xi, listCentroids[i])                          # calculate the distance
        if centroidDis < minD:                                                  # if new distance is less than min distance
            minD = centroidDis                                                  # update minD
            index = i                                                           # update index

    return index                                                                # return index of centroid with minD from xi


def IndexListClusters(ListX , listCentroids):
    """Returns list c containing the indices of the closest cluster center
    for each data point"""
    #listCentroids = mu
    #listX = list of data points
    c = []                                                                      # initialize c
    for dataPoint in ListX:                                                     # for each point in x
        c.append(IndexClosestCluster(dataPoint, listCentroids))                 # append the index of the closest cluster between the datapoint and one
                                                                                #of the centroids
    return c


def KCentroids(ListX , ListClusterIndices, K):
    """returns list mu containing the K centroids based on current assignment c"""
    #c = list of cluster indices
    #listX is the list of all the country points
    #k = k centroids
    # need to find all the (mu should have k entries) - mu is a list of np arrays (just like x) - x has n points - mu has only k points
    #compute the average of all the points that were assigned to that clusters
    # iterate through range of k (want that many mus)
    #inner loop for range of c (that is how many different indexes there are)
    #add each from the country data that have been assigned to the c index centroid and add all those points to
    #the points average and keep track of how many countries and do the average and append that average to mu and shoud
    # have k number of averages that you have appended

    mu = []                                                                     # initialze mu
    for j in range(K):                                                          # iterate through K
        sum = np.zeros(len(ListX[0]))                                           # initialze sum array
        m = 0                                                                   # initialize m (count)
        for i in range(len(ListClusterIndices)):                                # iterate through list of cluster indices (c)
            if ListClusterIndices[i] == j :                                     # if indice == cluster number
                sum += ListX[i]                                                 # increment sum
                m += 1                                                          # add 1 to the count
            if m != 0:                                                          # if m does not = zero
                average = sum / m                                               # calc the average
            if m == 0:
                average = sum                                                   # average will be the zero array
        mu.append(average)                                                      #append average to mu
    return mu                                                                   # return mu




def CurrentCost(x , c , mu):
    """Computes the current cost J"""
    #c = list containing closest cluster index
    #x = list of data datapoints
    #mu = list containing k centroids
    #iterate over x and c by index and use that index to get the mu and compute squared dif on those two things

    J = 0                                                               # initialize cost
    m = len(x)                                                          # get length of x
    for i in range(len(x)):                                             # iterate through x and m[c[i]]
        J += squaredDis(x[i], mu[c[i]])                                 # add squared distance to J
    J = (1/m) * J
    return J                                                            # return cost

def KMeans(x , K):
    """Runs the k-means algorithm"""

    #initialize the cluster centers mu simply to the first K elements of x
    max_iterations = 500                                            # initialize the max number of iterations
    num_it = 0                                                      # initialize iterations
    mu =[]                                                          # initialize mu
    c=[]                                                            # initialize c
    m = len(x)                                                      # set m to the length of x
    toReturn = []                                                   # initialize return list

    # initialize mu to the first k elements in x
    #mu = x[:K]

    #now, initialize mu to K random samples from x
    mu = random.sample(x , K)

    print("k = " + str(K) + " " + "n = " + str(len(x[0])) + " " + "m = " + str(m))
    c = IndexListClusters(x , mu)                                   # list of index to assigned clusters
    print("Cost after cluster assignment: " + str(CurrentCost(x , c, mu)))
    mu = KCentroids(x , c, K)                                       # update centroids
    print("Cost after updating centroids: " + str(CurrentCost(x , c, mu)))

    while num_it < max_iterations:                                  # do this loop until it hits the max number of iterations
        new_c = IndexListClusters(x , mu)                           # get new list of index assigned to clusters
        if new_c == c:                                              # if this new assignment = previous assignment it has converged
            num_it += 1

            print("Cost after cluster assignment: " + str(CurrentCost(x , c, mu)))
            print("converged after " + str(num_it) + " iterations")

            toReturn.append(CurrentCost(x , c, mu))                # first item in list is the minimum cost
            toReturn.append(c)                                     # second item in list is c
            toReturn.append(mu)
            return toReturn                                        # return list
            break
        c = new_c                                                   # update c to the new c

        print("Cost after cluster assignment: " + str(CurrentCost(x , c, mu)))

        mu = KCentroids(x , c , K)                                 # update centroids

        print("Cost after updating centroids: " + str(CurrentCost(x , c, mu)))

        num_it += 1                                                # increase the number of iterations

    toReturn.append(CurrentCost(x , c, mu))                         # first item in list is the minimum cost
    toReturn.append(c)                                              # second item in list is c
    toReturn.append(mu)                                             # third item in list is mu
    return toReturn




def runKMeans(x, K , numTimes , countryList):
    """runs the KMeans algorithm numTimes number of times"""
    returned = KMeans(x , K)                                                # get the cost and c of the kmeans alg
    lowestCost = returned[0]                                                # get the cost
    c = returned[1]                                                         # get the c
    mu = returned[2]                                                        # get the mu
    numGetLow = 1                                                           # set the number of times you have seen that low cost to 1
    for time in range(numTimes - 1):                                        # run this numtimes - 1 times because already ran it once
        returned = KMeans(x , K)                                            # run kmeans again and get cost and c
        TemplowestCost = returned[0]                                        # get cost from this run
        tempc = returned[1]                                                 # get c from this run
        tempmu = returned[2]                                                # get mu from this run
        if TemplowestCost < lowestCost:                                     # if new run cost is less then previous run cost
            lowestCost = TemplowestCost                                     # update cost
            c = tempc                                                       # update c
            mu = tempmu                                                     # update mu
            numGetLow = 1                                                   # reset number of times we have seen lowest cost
        if TemplowestCost == lowestCost:                                    # if it is the same lowest cost as previously
            numGetLow += 1                                                  # increment the number of times we have seen the lowest cost


    #stateIndex = c[countryList.index("United States of America")]          #get index of the united state (to match print statement in hw comparison file)

    for i in range(K):                                                     #Use this to print the countries in each cluster
        printClusters(countryList, c , i)


    #print("k = " + str(K) + ",  " + "cost: " + str(lowestCost) + "  " + str(numGetLow) + "/" + str(numTimes) + " , size of USA's Cluster: " + str(c.count(stateIndex)))
    #print statement to match the sample output in the hw5

    toReturn = []                                                           # create list with return value
    toReturn.append(lowestCost)                                             # add lowest cost to return list
    toReturn.append(c)                                                      # add c to the return list
    toReturn.append(mu)                                                     # add mu to the return list
    return toReturn                                                         # return lowest cost and c


def printClusters(countryList , c , Kval):
    """prints the list of countries belonging in cluster Kval"""
    print(len(c))
    print("cluster " + str(Kval))                                       # print the kval (to know which cluster)
    for countries in countryList:                                       # iterate through the country list
        if c[countryList.index(countries)] == Kval:                     # if country assigned index in c is = kVal
            print(countries)

def toFile(x , K , numberRuns, countries , filename):
    """runs the KMeans algorithm 100 times to find the lowest cost on K from 1-K (inclusive)
    and outputs the min cost for each K in a csv named hw5File2.csv"""
    file = open(filename , 'w')                                       # open it in append mode
    with file:
        for i in range(1 , K + 1):
            returned = runKMeans(x , i , numberRuns, countries)               #returns min cost and c
            cost = returned[0]                              # get min cost for that k value after 100 runs
            writer = csv.writer(file)
            costarray = []                                  #create array to write to csv
            costarray.append(cost)                          #append the cost to the array
            costarray.append(i)                             #append the k value to the array
            writer.writerow(costarray)                      # write to csv file

if __name__ == '__main__':
    main()
