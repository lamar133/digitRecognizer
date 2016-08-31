import csv
import random
import operator
def main():
    def loadDataSet(filename, split, trainingSet=[], testSet=[]):
        with open(filename, 'r') as csvfile:
            lines = csv.reader(csvfile)
            dataset = list(lines)
            dataset = dataset[1:]
            for x in range(len(dataset)-1):
                for y in range(785):
                    dataset[x][y] = float(dataset[x][y])
                if random.random() < split:
                    trainingSet.append(dataset[x])
                else:
                    testSet.append(dataset[x])

    def condenseData(trainingSet, testSet, condensedTraining=[], condensedTest=[]):
        trainingSet = trainingSet
        pixelCountInRows = 0
        totalOnesInTrainingRow = []
        numberOfOnes = 0
        crop = 0

        for row in range(len(trainingSet)):
            for pixel in trainingSet[row]:

                crop += 1

                if crop <= 28 or crop > 756:
                    continue

                if pixel != 0:
                    pixel = 1
                    numberOfOnes += 1

                if pixelCountInRows == 28:
                    pixelCountInRows = 0
                    totalOnesInTrainingRow.append(numberOfOnes)
                    numberOfOnes = 0

                pixelCountInRows += 1

            condensedTraining.append(totalOnesInTrainingRow)
            totalOnesInTrainingRow = []
            crop = 0

        testSet = testSet
        pixelCountInRows = 0

        totalOnesInTestRow=[]
        numberOfOnes = 0
        crop = 0

        for row in range(len(testSet)):
            for pixel in testSet[row]:

                crop += 1

                if crop <= 28 or crop > 756:
                    continue

                if pixel != 0:
                    pixel = 1
                    numberOfOnes += 1

                if pixelCountInRows == 28:
                    pixelCountInRows = 0
                    totalOnesInTestRow.append(numberOfOnes)
                    numberOfOnes = 0

                pixelCountInRows += 1

            condensedTest.append(totalOnesInTestRow)
            totalOnesInTestRow = []
            crop = 0

    def euclideanDistance(instance1, instance2, length):
        distance = 0
        for x in range(length):
            distance += pow((instance1[x] - instance2[x]), 2)
        return distance**0.5

    def getNeighbours(condensedTraining, testInstance, k):
        distances = []
        length = len(testInstance) - 1
        for x in range(len(condensedTraining)):
            dist = euclideanDistance(condensedTraining[x], testInstance, length)
            distances.append((int(trainingSet[x][0]), dist))
        distances.sort(key=operator.itemgetter(1))

        neighbours = []
        for x in range(k):
            neighbours.append(distances[x][0])
        return neighbours

    def getResponse(neighbours):
        classVotes = {}
        for x in range(len(neighbours)):
            response = neighbours[x]
            if response in classVotes:
                classVotes[response] += 1
            else:
                classVotes[response] = 1
        sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
        return sortedVotes[0][0]


    trainingSet=[]
    testSet=[]
    split = 0.67
    loadDataSet('train.csv', split, trainingSet, testSet)
    condensedTraining=[]
    condensedTest=[]
    condenseData(trainingSet, testSet, condensedTraining, condensedTest)
    correct = 0
    k = 13
    for x in range(len(condensedTest)):
        neighbours = getNeighbours(condensedTraining, condensedTest[x], k)
        result = getResponse(neighbours)
        if result == int(testSet[x][0]):
            correct += 1
    accuracy = correct/float(len(testSet)) * 100
    print("Accuracy: " + repr(accuracy) + "%")
