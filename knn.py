__author__ = 's1213677'

import scipy.io
import numpy

data = scipy.io.loadmat('gtzan.mat')



# Go through every fragment within this fold, testing it with every other fragment in every other fold
# Classifies data given the fold number to use as test data
def classify(testFoldNum, k):
    testFold = data['fold' + str(testFoldNum) + '_features']
    distanceClasses = []

    # Go through every single fold (that isn't the test fold) and compare it with the test fold
    for trainingFoldNum in range (1, 10):
        if trainingFoldNum != testFoldNum:

            trainingFold = data['fold' + str(trainingFoldNum) + '_features']
            trainingFoldClasses = data['fold' + str(trainingFoldNum) + '_classes']

            # Now we loop through all the fragments in that fold
            for counter in range(0, 93):
                category = trainingFoldClasses[counter][0]

                # distancesList contains a list of distances, all associated with the above category
                distancesList = loopFold(testFold, trainingFold)

                # Add to our distanceClasses list which contains [eucledian distance, class]
                for distance in distancesList:
                    newList = [distance, category]
                    distanceClasses.append(newList)

    return getCategory(distanceClasses, k)

# Given a list of distances, with their classes, returns the most common class. Only taking into account the k nearest
def getCategory(distanceClasses, k):
    sortedList =  sorted(distanceClasses, key=lambda x: x[0], reverse=True)

    # categories is a dictionary containing  class: classCounter pairs
    categories = {}

    # Go to the first k points and get their category
    for i in range (0, k-1):
        categories[sortedList[i][1]] = categories.get(sortedList[i][1], 0) + 1

    # sort the dictionary by the values. The one with the highest value is the most common, so return that class
    for category in sorted(categories.iterkeys()):
        return category


# Go through all the fragments in the test folds and compare it with all the fragments in the training fold
def loopFold(testFold, trainingFold):
    for fragment in testFold:
        for trainingFragment in trainingFold:
            return loopFragment(fragment, trainingFragment)

# Loop through all the points within fragments, getting the eucledian distance
# Return array of eucledian distances and their points
def loopFragment(testFragment, trainingFragment):

    points = []
    testPointCounter = 0
    trainingPointCounter = 0

    # Loop through all the testPoints until we've hit the last one
    while testPointCounter <= len(testFragment)-1:
        testPoint = [testFragment[testPointCounter], testFragment[testPointCounter+1], testFragment[testPointCounter+2], testFragment[testPointCounter+3]]

        # Loop through all the training points until we reach the last one
        while trainingPointCounter <= len(trainingFragment)-1:
            trainingPoint = [trainingFragment[trainingPointCounter], trainingFragment[trainingPointCounter+1], trainingFragment[trainingPointCounter+2], trainingFragment[trainingPointCounter+3]]

            # get the eucledian distance between the two points and add it to our points list
            points.append(eucledian(testPoint, trainingPoint))
            trainingPointCounter +=4

        testPointCounter += 4

    return points

# Given two points, returns the eucledian distance
def eucledian(pointA, pointB):
    a = numpy.array((pointA[0],pointA[1],pointA[2], pointA[3]))
    b = numpy.array((pointB[0],pointB[1],pointB[2], pointB[3]))
    return numpy.sqrt(numpy.sum((a-b)**2))

# Print the category determined by KNN
print classify(1, 3)