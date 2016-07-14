htmDF = pd.read_csv('./HitsTimeMoney.csv')
htmDF.head(n = 5)

htm = htmDF[['totalMoneySpent','totalTimeSpent','hitRatio']]
htm.shape
sqlContext = SQLContext(sc)
cxDF = sqlContext.createDataFrame(htm)
parseData = cxDF.rdd.map(lambda line: array([line[0], line[1], line[2]])) #totalMoneySpent totalTimeSpent hitRatio

htm_km = KMeans.train(parseData, 3, maxIterations=20, runs=20, initializationMode="random")

print(htm_km.centers)
