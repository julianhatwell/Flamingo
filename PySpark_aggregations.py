import pandas as pd
from numpy import array
import sys

pySp = False

# local
fileloc = 'C:/Dev/Study/Hadoop/big_data_capstone_datasets_and_scripts/flamingo-data/'
# spark VM
if pySp: fileloc = ''

gc = 'game-clicks.csv'
ac = 'ad-clicks.csv'
bc = 'buy-clicks.csv'
us = 'user-session.csv'

#Read game-clicks.csv file
gameClicksDF = pd.read_csv(fileloc + gc)
gameClicksDF = gameClicksDF.rename(columns=lambda x: x.strip())
gameClicksDF['clickCount'] = 1

userGameClicks = gameClicksDF[['userId', 'clickCount', 'isHit']]
hitRatioPerUser = userGameClicks.groupby('userId').sum()
hitRatioPerUser['ratio'] = hitRatioPerUser['isHit']/hitRatioPerUser['clickCount']
hitRatioPerUser = hitRatioPerUser.reset_index()
hitRatio = hitRatioPerUser[['userId', 'ratio']]
# hitRatio = hitRatio.reset_index()

#Read ad-clicks.csv file
adclicksDF = pd.read_csv(fileloc + ac)
adclicksDF = adclicksDF.rename(columns=lambda x: x.strip())
adclicksDF['adCount'] = 1

useradClicks = adclicksDF[['userId','adCount']]
adsPerUser = useradClicks.groupby('userId').sum()
adsPerUser = adsPerUser.reset_index()

#Read buy-clicks.csv file
buyClicksDF = pd.read_csv(fileloc + bc)
buyClicksDF = buyClicksDF.rename(columns=lambda x: x.strip())
userPurchases = buyClicksDF[['userId','price']]

revenuePerUser = userPurchases.groupby('userId').sum()
revenuePerUser = revenuePerUser.reset_index()

#Read user-sessions.csv file
userSessionsDF = pd.read_csv(fileloc + us)
sessionStarts = userSessionsDF[userSessionsDF['sessionType'] == 'start']
sessionEnds = userSessionsDF[userSessionsDF['sessionType'] == 'end'][['timestamp', 'userSessionId', 'userId']]
userSessionsCondensed = sessionStarts.merge(sessionEnds, on = ['userSessionId', 'userId'])
userSessionsCondensed['duration'] = pd.to_datetime(userSessionsCondensed['timestamp_y']) - pd.to_datetime(userSessionsCondensed['timestamp_x'])
userSessionsCondensed = userSessionsCondensed.reset_index()
userDurations = userSessionsCondensed[['userId', 'duration']]
durationPerUser = userDurations.groupby('userId').sum()
durationPerUser = durationPerUser.reset_index()

#merge together to create trainingDF
trainingDF = adsPerUser.merge(revenuePerUser, on = 'userId', how = 'outer')
trainingDF = trainingDF.merge(hitRatio, on = 'userId', how = 'outer')
trainingDF = trainingDF.merge(durationPerUser, on = 'userId')
trainingDF = trainingDF.fillna(0)

if pySp:
    from pyspark.mllib.clustering import KMeans, KMeansModel
    from pyspark import SparkConf, SparkContext
    from pyspark.sql import SQLContext

    conf = (SparkConf().setMaster("local").setAppName("My app").set("spark.executor.memory", "1g"))
    sc 			= SparkContext(conf = conf)
    sqlContext 	= SQLContext(sc)
    pDF = sqlContext.createDataFrame(trainingDF)
    parsedData = pDF.rdd.map(lambda line: array([line[1], line[2], line[3], line[4]]))
    #Train KMeans model to create clusters
    clusters = KMeans.train(parsedData, 2, maxIterations=10, runs=10, initializationMode="random")

    #redirect stdout
    orig_stdout = sys.stdout
    f = open('clusterCenters.txt', 'w')
    sys.stdout = f

    #Display the clusterCenters
    print(clusters.centers)
    print('\n1: adCount\n2: price\n3: ratio\n4: duration')

    #Redirect back the stdout
    sys.stdout = orig_stdout
    f.close()
