# hitRatio
userHits = dict()
for i in range(len(allData['game-clicks']['userId'])):
    uid = allData['game-clicks']['userId'][i]
    if uid not in userHits.keys():
        userHits[uid] = {'clicks' : 1, 'hits' : 0}
    else:
        userHits[uid]['clicks'] += 1
    userHits[uid]['hits'] = userHits[uid]['hits'] + int(allData['game-clicks']['isHit'][i])

for k in userHits.keys():
    hitRate = userHits[k].get('hits')/userHits[k].get('clicks')
    userHits[k].update({'hitRatio' : hitRate})

# ad clicks
adClicks = dict()
for i in range(len(allData['ad-clicks']['userId'])):
    uid = allData['ad-clicks']['userId'][i]
    sessionId = allData['ad-clicks']['userSessionId'][i]
    adCategory = allData['ad-clicks']['adCategory'][i]
    if uid not in adClicks.keys():
        adClicks[uid] = {'totalClicks' : 1
        , 'sessions' : { sessionId : 1 }
        , 'adCategories' : { adCategory : 1}
        }
    else:
        adClicks[uid]['totalClicks'] += 1
        if sessionId not in adClicks[uid]['sessions'].keys():
            adClicks[uid]['sessions'][sessionId] = 1
        else: adClicks[uid]['sessions'][sessionId] += 1
        if adCategory not in adClicks[uid]['adCategories'].keys():
            adClicks[uid]['adCategories'][adCategory] = 1
        else: adClicks[uid]['adCategories'][adCategory] += 1

for k in adClicks.keys():
    aveClicks = adClicks[k]['totalClicks']/len(adClicks[k]['sessions'].values())
    adClicks[k].update({'aveClicks' : aveClicks})

# buy clicks
buyClicks = dict()
for i in range(len(allData['buy-clicks']['userId'])):
    uid = allData['buy-clicks']['userId'][i]
    price = allData['buy-clicks']['price'][i]
    if uid not in buyClicks.keys():
        buyClicks[uid] = {'clicks' : 1, 'price' : float(price)}
    else:
        buyClicks[uid]['clicks'] += 1
        buyClicks[uid]['price'] += float(price)

for k in buyClicks.keys():
    avePrice = buyClicks[k]['price']/buyClicks[k]['clicks']
    buyClicks[k].update({'avePrice' : avePrice})

 
