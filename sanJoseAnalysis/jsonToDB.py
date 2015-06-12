#Reads data from a json file and writes it to a mongodb database.
__author__ = 'Aishwarya'

import json

def insert_data(data, db):
    for a in data:
        db.city.insert(a)

def printVal(a):
    for b in a:
        print b

#Starts the program and does two things mainly: writes json data to database
# and prints data about the dataset.
if __name__ == "__main__":
    from pymongo import MongoClient
    client = MongoClient("mongodb://localhost:27017")
    db = client.examples

    #Writes the JSON file to the database
    with open('test.json') as f:
       data = json.loads(f.read())
       insert_data(data, db)

    #All the following code prints information about the database
    print db.city.find().count()
    print db.city.find_one()
    print db.city.find({ "type": { "$in":['way']} }).count()

    print len(db.final.distinct("created.user"))
    #Unique users
    print "User with highest number of posts:"
    pipeline = [{"$group":{"_id":"$created.user", "count":{"$sum":1}}},
                {"$sort": {"count":-1}},
                {"$limit":5}]
    a= db.final.aggregate(pipeline)
    printVal(a)
    #Users who made exactly one post
    print "Number of users who made only one post:"
    pipeline = [{"$group":{"_id":"$created.user", "count":{"$sum":1}}},
                {"$group":{"_id":"$count", "num_users":{"$sum":1}}},
                {"$sort":{"_id":1}},
                {"$limit":1}]
    a= db.final.aggregate(pipeline)
    printVal(a)

    #Number of cafes
    print "Total number of cafes of the area are:"
    pipeline = [{"$match":{"amenity":{'$exists':1},"amenity":"cafe"}},
           {"$group":{"_id":"cafe","count":{"$sum":1}}},
           {"$limit" : 1}]
    a= db.final.aggregate(pipeline)
    printVal(a)

    #Number of restaurants
    print "Total number of restaurants of the area are:"
    pipeline = [{"$match":{"amenity":{'$exists':1},"amenity":"restaurant"}},
           {"$group":{"_id":"restaurant","count":{"$sum":1}}},
           {"$limit" : 1}]
    a= db.final.aggregate(pipeline)
    printVal(a)

    #Top 5 religions of this area
    print "6 most common religions of the area are:"
    pipeline = [
                {"$match":{"amenity":{ "$ne":None},
                           "amenity":"place_of_worship",
                           "religion":{ "$ne":None}}},
                {"$group":{"_id":"$religion","count":{"$sum":1}}},
                {"$sort" : {"count":-1}},
                {"$limit" : 6}]
    a= db.final.aggregate(pipeline)
    printVal(a)

    #Most popular cuisines of this area
    print "Top 6 cuisines of the area are:"
    pipeline = [
                {"$match":{"amenity":{"$exists":1},
                           "amenity":"restaurant" ,
                           "cuisine":{ "$ne":None}}},
                {"$group":{"_id":"$cuisine","count":{"$sum":1}}},
                {"$sort" : {"count":-1}},
                {"$limit" : 6}
                ]
    a= db.final.aggregate(pipeline)
    printVal(a)
    #Total number of bus stations in this area
    print "Total number of bus stations of the area are:"
    pipeline = [{"$match":{"amenity":{'$exists':1},"amenity":"bus_station"}},
           {"$group":{"_id":"bus_station","count":{"$sum":1}}},
           {"$limit" : 1}]
    a= db.final.aggregate(pipeline)
    printVal(a)

    #Bank with the highest number of ATMs
    print "Bank having the highest number of ATMs in the area is:"
    pipeline = [
                {"$match":{"amenity":{'$exists':1},
                           "amenity":"atm",
                           "operator":{ "$ne":None}}},
                {"$group":{"_id":"$operator","count":{"$sum":1}}},
                {"$sort" : {"count":-1}},
                {"$limit" : 1}
                ]
    a= db.final.aggregate(pipeline)
    printVal(a)
    #Pharmacy with the highest number of outlets
    print "Pharmacy with the highest number of outlets in the area is:"
    pipeline = [
                {"$match":{"amenity":{'$exists':1},
                           "amenity":"pharmacy",
                           "operator":{ "$ne":None}}},
                {"$group":{"_id":"$operator","count":{"$sum":1}}},
                {"$sort" : {"count":-1}},
                {"$limit" : 1}
                ]
    a= db.final.aggregate(pipeline)
    printVal(a)
