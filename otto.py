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


def length_of_table(table):
    """Returns the count of instances in a table"""
    return len(table)

def count_dups(table):
    """Counts duplicates in a given table"""
    count = 0
    for row in table:
        if table.count(row) > 1:
            count+=1
    return count
    
def print_count_csv_dups(table):
    """Prints a csv with a count at the beginning of duplicate rows"""
    for row in table:
        c = table.count(row)
        if c > 1:
            print "count:" + str(c) + "*******************************"
        for i in range(len(row) - 1):
            sys.stdout.write(str(row[i]) + ',')
        print row[-1]

def print_csv_summary(filename):
    """Prints the length and count of duplicates in a csv file"""
    line = "--------------------------------------------------"
    table = read_csv(filename)
    
    print line
    print filename + ":"
    print line

    print "No. of instances:" + str(length_of_table(table))
    print "Duplicates: " + str(count_dups(table))

    
def twod_list(w, h):
    """ Creates a two dimentional list with specified width and height"""
    default = "NA"
    twod_list = []
    new = []
    
    for i in range (0, w):
        for j in range (0, h):
            new.append(default)
        twod_list.append(new)
        new = []
    return twod_list

def wait():
    "Waits for user input"
    print "\n"
    raw_input("Press Enter to continue...")

def holdout_partition(table):
    "Creates Holdout Partitions"
    randomized = table[:]
    n = len(table)    
    for i in range(n):
        j = random.randint(0, n-1)
        randomized[i], randomized[j] = randomized[j], randomized[i]
    n0 = (n*2)/3
    return randomized[0:n0],randomized[n0:]

def kfold_partition(table,k):
    "Creates k roughly equal parts"
    randomized = table[:]
    n = len(table)
    folds = []
    extra = n % k
    foldsize = n / k
    i = 0
    x = 0
    while i < k:
        temp = []
        x = 0;
        while x < foldsize:
            #print("extra+" + str(extra))
            #print("foldsize+" + str(foldsize))
            #print(i + (x*k))
            #print(n)
            temp.append(randomized[i + (x*k)])
            #print("reg fold okay!")
            x = x+1
        if extra > 0:
            temp.append(randomized[i + (x*k)])
            extra = extra-1
        folds.append(temp)
        i = i+1
    return folds
    
def getknn(k, table, columns, columnToPredict,weighted,filename):
    instances = randomDraw(k, str(filename))
    avgs = []
    results = []
    DataTable = table[:]
    #print "Read Data"
    predictedClass = []
    for i in range(k):
        #print "Starting First Loop"
        NNs = getNearestNeighbors(k, instances[i], columns, DataTable,weighted)
        #print "Appending First Val"        
        avgs.append(NNs)
        for NNs in avgs:
            for NN in NNs:
                tempclass = []
                tempclass.append(NN[columnToPredict])
                if tempclass.count("false") >= tempclass.count("true"):
                    predictedClass.append("false")
                else:
                    predictedClass.append("true")
    j = 0
    TP = 0
    FP = 0
    TN = 0
    FN = 0
    for instance in instances:
        #print "Instance: "
        #print instance
        actual_Class =  instance[columnToPredict]
        predicted_Class = predictedClass[j]
        #print "Class, " + str(predicted_Class)
        #print "Actual, " + str(actual_Class)    
        j += 1
        results.append(actual_Class)
        results.append(predicted_Class)
        if predicted_Class == actual_Class:
            if predicted_Class == "True":
                TP = TP + 1
            else:
                TN = TN + 1
        else:
            if predicted_Class == "True":
                FP = FP +1
            else:
                FN = FN +1 
    count = len(results)/2
    accuracy =(TP+TN)/(count * 1.0)
   # print accuracy
    return accuracy

def majorityVote(predictions,attr):
    votes = []
    for a in attr:
            votes.append(0)
    for prediction in predictions:
        if prediction != -1:
            index=0
            for a in attr:
                if a == prediction:
                    votes[index] =  votes[index] +1
                index = index + 1                
    index = predictions.index(max(predictions))
    return(attr.pop(index))
    
def getNearestNeighbors(k, instance, columns, dataTable,weighted):
    nearest = []
    #print "creating Ordered List"
    orderedList = orderByNearestNeighbor(instance, columns, dataTable,weighted)
    i = 1           #first value is the item itself
    while i <= k:
        nearest.append(orderedList[i])
        i += 1
    return nearest
    

def orderByNearestNeighbor(instance, columns, dataTable,weighted):
    distances = []
    #print "Reading row 1"
    for row in dataTable:
        if weighted != True:
            distances.append(getDistance(instance, row, columns,dataTable))
        else:
            distances.append(getWeightedDistance(instance, row, columns,dataTable))
    return [x for (y,x) in sorted(zip(distances,dataTable))]
    
def getDistance(x1, x2, columns,table):
    if x1 == x2:
        return 0.0
    else:
        sumSqr = 0.0
        for i in columns:
            if isinstance(x1[i], basestring):
                if x1[i] != x2[i]:
                    sumSqr += 1.0
            else:
                totalVals = []
                for row in table:
                   totalVals.append(row[i])
                sumSqr += ((float(x1[i]) - float(x2[i])) ** 2)/(float(max.totalVals-min.totalVals))
            
    return sumSqr
    
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
    
    
    
    


            

if __name__ == '__main__':
    main()
