# Kingdom of Loathing MallBot by KevZho (#2434890)
# make sure to edit the options first on lines 15 to 27
# TODO: fix hitting the limits

from kol.database import ItemDatabase
from kol.Session import Session
from kol.request.MallItemSearchRequest import MallItemSearchRequest
from kol.request.MallItemPurchaseRequest import MallItemPurchaseRequest
from kol.request.CocktailcraftingRequest import CocktailcraftingRequest
from kol.request.AddItemsToStoreRequest import PutItemInStoreRequest
#from kol.Error import Error as Error
#import logging

s = Session()
# add booze terms here, make sure to use the same capitalization as in the recipe dictionary
# searchTerms = ['parisian cathouse', 'prussian cathouse', 'vodka martini', 'rockin\' wagon', 'soft green echo eyedrop antidote martini', 'sangria de menthe']
searchTerms = ['soft green echo eyedrop antidote martini']
# add the ingredients as an array to the dictionary term
recipe = {'parisian cathouse': ['raspberry', 'boxed champagne'], 'prussian cathouse': ['parisian cathouse', 'magical ice cubes'], 'vodka martini': ['olive', 'bottle of vodka'], 'rockin\' wagon': ['vodka martini', 'magical ice cubes'], 'soft green echo eyedrop antidote martini': ['rockin\' wagon', 'soft green echo eyedrop antidote'], 'sangria de menthe': ['peppermint twist', 'boxed wine']}
# meat you are willing to spend in on each type booze
meatLimit = 100000
# how much you want to undercut the lowest price on the market
underCut = 1
# login with your username as password here
s.login("username", "password")

# end options
myStoreId = s.userId
result = {}
def pad(word):
    return '"{0}"'.format(word)
def makeItRain():
    for term in searchTerms:
        m = MallItemSearchRequest(s, pad(term))
        res = m.doRequest()["results"][0]
        curResult = [res["price"], res["quantity"], res["id"]]
        result[term] = curResult
        print "Booze: {0}, price: {1}, quantity: {2}".format(res["name"], res["price"], res["quantity"])
        curRecipe = recipe[term]
        total = 0
        recipeData = []
        for ingredient in curRecipe:
            m = MallItemSearchRequest(s, pad(ingredient))
            searchData = m.doRequest()
            recipeData.append(searchData["results"][0])
            price = searchData["results"][0]["price"]
            total += price
        if res["price"] > total:
            print "{0} should be crafted for profit. {0} has a total ingredient cost of {1}, but is selling for {2}".format(term, total, res["price"])
            if "limit" in recipeData[0] or "limit" in recipeData[1]:
                if "limit" in recipeData[0] and "limit" not in recipeData[1]:
                    if min(recipeData[0]["quantity"], recipeData[1]["quantity"]) > recipeData[0]["limit"]:
                        print "minimum is greater than limit, must limit how much we buy for {0}".format(term)
                        quantityOfEach = min(int(meatLimit / total), recipeData[0]["limit"])
                        buyItem(recipeData[0]["storeId"], ItemDatabase.getItemFromName(recipeData[0]["name"])["id"], quantityOfEach, recipeData[0]["price"])
                        buyItem(recipeData[1]["storeId"], ItemDatabase.getItemFromName(recipeData[1]["name"])["id"], quantityOfEach, recipeData[1]["price"])
                        if res["storeId"] == myStoreId:
                            sellItem(craftItem(ItemDatabase.getItemFromName(recipeData[0]["name"])["id"], ItemDatabase.getItemFromName(recipeData[1]["name"])["id"], quantityOfEach), res["price"], quantityOfEach)
                        else:
                            sellItem(craftItem(ItemDatabase.getItemFromName(recipeData[0]["name"])["id"], ItemDatabase.getItemFromName(recipeData[1]["name"])["id"], quantityOfEach), (res["price"] - underCut), quantityOfEach)
                    else:
                        print "Minimum less than limit for {0}".format(term)
                        quantityOfEach = min(int(meatLimit / total), min(recipeData[0]["quantity"], recipeData[1]["quantity"]))
                        buyItem(recipeData[0]["storeId"], ItemDatabase.getItemFromName(recipeData[0]["name"])["id"], quantityOfEach, recipeData[0]["price"])
                        buyItem(recipeData[1]["storeId"], ItemDatabase.getItemFromName(recipeData[1]["name"])["id"], quantityOfEach, recipeData[1]["price"])
                        if res["storeId"] == myStoreId:
                            sellItem(craftItem(ItemDatabase.getItemFromName(recipeData[0]["name"])["id"], ItemDatabase.getItemFromName(recipeData[1]["name"])["id"], quantityOfEach), res["price"], quantityOfEach)
                        else:
                            sellItem(craftItem(ItemDatabase.getItemFromName(recipeData[0]["name"])["id"], ItemDatabase.getItemFromName(recipeData[1]["name"])["id"], quantityOfEach), (res["price"] - underCut), quantityOfEach)
                elif "limit" in recipeData[1] and "limit" not in recipeData[0]:
                    if min(recipeData[0]["quantity"], recipeData[1]["quantity"]) > recipeData[1]["limit"]:
                        print "minimum is greater than limit, must limit how much we buy for {0}".format(term)
                        quantityOfEach = min(int(meatLimit / total), recipeData[1]["limit"])
                        buyItem(recipeData[0]["storeId"], ItemDatabase.getItemFromName(recipeData[0]["name"])["id"], quantityOfEach, recipeData[0]["price"])
                        buyItem(recipeData[1]["storeId"], ItemDatabase.getItemFromName(recipeData[1]["name"])["id"], quantityOfEach, recipeData[1]["price"])
                        if res["storeId"] == myStoreId:
                            sellItem(craftItem(ItemDatabase.getItemFromName(recipeData[0]["name"])["id"], ItemDatabase.getItemFromName(recipeData[1]["name"])["id"], quantityOfEach), res["price"], quantityOfEach)
                        else:
                            sellItem(craftItem(ItemDatabase.getItemFromName(recipeData[0]["name"])["id"], ItemDatabase.getItemFromName(recipeData[1]["name"])["id"], quantityOfEach), (res["price"] - underCut), quantityOfEach)
                    else:
                        print "Minimum less than limit for {0}".format(term)
                        quantityOfEach = min(int(meatLimit / total), min(recipeData[0]["quantity"], recipeData[1]["quantity"]))
                        buyItem(recipeData[0]["storeId"], ItemDatabase.getItemFromName(recipeData[0]["name"])["id"], quantityOfEach, recipeData[0]["price"])
                        buyItem(recipeData[1]["storeId"], ItemDatabase.getItemFromName(recipeData[1]["name"])["id"], quantityOfEach, recipeData[1]["price"])
                        if res["storeId"] == myStoreId:
                            sellItem(craftItem(ItemDatabase.getItemFromName(recipeData[0]["name"])["id"], ItemDatabase.getItemFromName(recipeData[1]["name"])["id"], quantityOfEach), res["price"], quantityOfEach)
                        else:
                            sellItem(craftItem(ItemDatabase.getItemFromName(recipeData[0]["name"])["id"], ItemDatabase.getItemFromName(recipeData[1]["name"])["id"], quantityOfEach), (res["price"] - underCut), quantityOfEach)
                elif "limit" in recipeData[1] and "limit" in recipeData[0]:
                    if min(recipeData[0]["quantity"], recipeData[1]["quantity"]) > min(recipeData[1]["limit"], recipeData[0]["limit"]):
                        print "minimum is greater than limit, must limit how much we buy for {0}".format(term)
                        quantityOfEach = min(int(meatLimit / total), min(recipeData[1]["limit"], recipeData[0]["limit"]))
                        buyItem(recipeData[0]["storeId"], ItemDatabase.getItemFromName(recipeData[0]["name"])["id"], quantityOfEach, recipeData[0]["price"])
                        buyItem(recipeData[1]["storeId"], ItemDatabase.getItemFromName(recipeData[1]["name"])["id"], quantityOfEach, recipeData[1]["price"])
                        if res["storeId"] == myStoreId:
                            sellItem(craftItem(ItemDatabase.getItemFromName(recipeData[0]["name"])["id"], ItemDatabase.getItemFromName(recipeData[1]["name"])["id"], quantityOfEach), res["price"], quantityOfEach)
                        else:
                            sellItem(craftItem(ItemDatabase.getItemFromName(recipeData[0]["name"])["id"], ItemDatabase.getItemFromName(recipeData[1]["name"])["id"], quantityOfEach), (res["price"] - underCut), quantityOfEach)
                    else:
                        print "Minimum less than limit for {0}".format(term)
                        quantityOfEach = min(int(meatLimit / total), min(recipeData[0]["quantity"], recipeData[1]["quantity"]))
                        buyItem(recipeData[0]["storeId"], ItemDatabase.getItemFromName(recipeData[0]["name"])["id"], quantityOfEach, recipeData[0]["price"])
                        buyItem(recipeData[1]["storeId"], ItemDatabase.getItemFromName(recipeData[1]["name"])["id"], quantityOfEach, recipeData[1]["price"])
                        if res["storeId"] == myStoreId:
                            sellItem(craftItem(ItemDatabase.getItemFromName(recipeData[0]["name"])["id"], ItemDatabase.getItemFromName(recipeData[1]["name"])["id"], quantityOfEach), res["price"], quantityOfEach)
                        else:
                            sellItem(craftItem(ItemDatabase.getItemFromName(recipeData[0]["name"])["id"], ItemDatabase.getItemFromName(recipeData[1]["name"])["id"], quantityOfEach), (res["price"] - underCut), quantityOfEach)
            else:
                print "Ingredients not limited for {0}".format(term)
                quantityOfEach = min(int(meatLimit / total), min(recipeData[0]["quantity"], recipeData[1]["quantity"]))
                buyItem(recipeData[0]["storeId"], ItemDatabase.getItemFromName(recipeData[0]["name"])["id"], quantityOfEach, recipeData[0]["price"])
                buyItem(recipeData[1]["storeId"], ItemDatabase.getItemFromName(recipeData[1]["name"])["id"], quantityOfEach, recipeData[1]["price"])
                if res["storeId"] == myStoreId:
                    sellItem(craftItem(ItemDatabase.getItemFromName(recipeData[0]["name"])["id"], ItemDatabase.getItemFromName(recipeData[1]["name"])["id"], quantityOfEach), res["price"], quantityOfEach)
                else:
                    sellItem(craftItem(ItemDatabase.getItemFromName(recipeData[0]["name"])["id"], ItemDatabase.getItemFromName(recipeData[1]["name"])["id"], quantityOfEach), (res["price"] - underCut), quantityOfEach)
        else:
            print "{0} should NOT be crafted for profit. {0} has a total ingredient cost of {1}, but is selling for {2}".format(term, total, res["price"])
def buyItem(storeID, itemID, quantity, price):
    print "Buying {2} of {1} from {0}".format(storeID, itemID, quantity)
    try:
        m = MallItemPurchaseRequest(s, storeID, itemID, price, quantity)
        m.doRequest()
        print "Brought {2} of {1} from {0}".format(storeID, itemID, quantity)
    except:
        print "Oh no!"

def craftItem(item1, item2, quantity):
    print "Crafting {2} of {0} and {1} together".format(item1, item2, quantity)
    c = CocktailcraftingRequest(s, item1, item2, quantity)
    response = c.doRequest()
    print "Crafted {2} of {0} and {1} together to make {3}".format(item1, item2, quantity, response["booze"]["name"])
    return response["booze"]["id"]
def sellItem(itemId, price, quantity, limit=""):
    print "Attempting to sell {2} of {0} at {1} each".format(itemId, price, quantity)
    p = PutItemInStoreRequest(s, [{'id': itemId, 'quantity': quantity, 'price': price, 'limit': limit}])
    p.doRequest()
    print "Sold {2} of {0} at {1} each".format(itemId, price, quantity)
makeItRain()
