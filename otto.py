### Authors: Neil Walton and Stephen Strozyk ###
###              March 2015                  ###



def loadData(filename):
    "Load data from the CSV training and test files"
    data = []
    fin = open(filename, 'r')
    line = fin.readline()
    while (line != ''):
        data.append(line.strip('\n'))
        line = fin.readline()
    fin.close()
    return data[1:]


def getFeatureNames(filename):
    "Return a list of feature names"
    fin = open(filename, 'r')
    line = fin.readline()
    line.strip('\n')
    featureNames = line.split(',')
    return featureNames[1:-1]


def getLabels(data):
    "Returns a list of actual training/test data labels"
    labels = []
    i = 0
    for datum in data:
        datumRow = datum.split(',')
        if len(datumRow) == 95:
            labels.append(datumRow[94])
    return labels


def extractFeatures(featureNames, datum):
    "Returns a dictionary of feature, value pairs from a training datum"
    features = {}
    idx = 1
    datum = datum.split(',')
    for feat in featureNames:
        features[feat] = datum[idx]
        idx += 1
    return features


def getDataSet(data, featureNames, labels):
    "Returns a list of (feature vector, label) tuples"
    dataSet = []
    idx = 0
    for datum in data:
        if idx < len(labels):
            dataSet.append((extractFeatures(featureNames, datum), labels[idx])) 
        idx += 1
    return dataSet 


def main():
    "Select classifier to use and classify the data"
    classifier = raw_input("Which classifier would you like to use?  ")
    rawTrainingData = loadData("train.csv")
    rawTestData = loadData("test.csv")
    validLabels = ['Class 1', 'Class 2', 'Class 3', 'Class 4', 'Class 5', 'Class 6', 'Class 7', 'Class 8', 'Class 9']
    actualTrainingLabels = getLabels(rawTrainingData)
    actualTestLabels = getLabels(rawTestData)
    featureNames = getFeatureNames("train.csv")
    trainingDataSet = getDataSet(rawTrainingData, featureNames, actualTrainingLabels)
    testDataSet = getDataSet(rawTestData, featureNames, actualTestLabels)
    
    
    
    


            

main()
