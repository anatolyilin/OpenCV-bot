import pickle

def writeMeuk():
    list = [0.0843, 2, 12.5, 7.5]
    with open('test.file', 'wb') as fp:
        pickle.dump(list, fp)

def readMeuk():
    with open('servo.conf', 'rb') as fp:
        listRead = pickle.load(fp)
    for i in listRead:
        print i

readMeuk()