from math import ceil, log
import mmh3
import sys
import csv
import random as rm
from bitarray import bitarray

class HashFunction:
    def __init__(self, seed: int, size: int):
        self.seed: int = seed
        self.array_size: int = size

    def __call__(self,key: str):
        return mmh3.hash128(key,self.seed) % self.array_size

class BloomFilter: #construct a bloomfilter based on a dataset
    def constructBloomFilter(n: int,targetProbability = 0.1):
        #returns the empty bloomFilter bitarray and the hash functions 
        #n: expected number of items initially in the bloom filter
        #targetProbability: is the expected number of false positives
        m = ceil((n * log(targetProbability)) / log(1 / pow(2, log(2))))
        k = ceil(m/n * log(2,2))
        hash_functions = []
        fib3 = 1 #use fibonnacci sequence to generate seeds
        fib2 = 1
        fib1 = 0
        for _ in range(k):
            fib3 = fib2 + fib1
            fib1 = fib2
            fib2 = fib3  
            hash_functions.append(HashFunction(fib3,m)) #
        
        bloomFilter = bitarray(m)
        return (bloomFilter, hash_functions)

    def __init__(self, size: int, p = 0.1):
        self.array, self.hash_functions = BloomFilter.constructBloomFilter(size,p)
    
    def lookup(self,element: str):
        for hash in self.hash_functions:
            hashedIndex: int = hash(element)
            if self.array[hashedIndex] == False:
                return False
        return True
    
    def insert(self,element):
        for hash in self.hash_functions:
            hashedIndex = hash(element)
            self.array[hashedIndex] = True
    
    def insertList(self,dataset):
        for element in dataset:
            for hash in self.hash_functions:
                hashedIndex = hash(element)
                self.array[hashedIndex] = True



arguments = sys.argv
if len(arguments) >= 3:
    emailListCSV = arguments[1]
    emailTestCSV = arguments[2]
    print(emailListCSV,emailTestCSV)
    emailList = []
    with open(emailListCSV, 'r') as csvfile:
        emailreader = csv.reader(csvfile)
        next(emailreader)  #skip the headers
        for email in emailreader:
            if email:
                emailList.append(email[0])

    emailBloomFilter = BloomFilter(len(emailList),0.0000001)
    #insert all of our emails into the bloom filter
    for email in emailList:
        emailBloomFilter.insert(email)

    #generate OutputCSV
    with open('results.csv', 'w', newline="") as outputfile:
        csvwriter = csv.writer(outputfile)
        header = ['Email','Result']
        csvwriter.writerow(header)
        with open(emailTestCSV, 'r') as testfile:
            emailreader = csv.reader(testfile)
            next(emailreader) #skip the header
            for email in emailreader:
                if email:
                    elementFound = emailBloomFilter.lookup(email[0])
                    if elementFound:
                        csvwriter.writerow((email,"Probably in the DB"))
                    else:
                        csvwriter.writerow((email,"Not in the DB"))
    

    



    




