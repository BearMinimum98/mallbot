# Kingdom of Loathing MallBot by KevZho (#2434890)
import kol.database.ItemDatabase
from kol.Session import Session
from kol.request.MallItemSearchRequest import MallItemSearchRequest
from kol.request.MallItemPurchaseRequest import MallItemPurchaseRequest
from kol.request.StoreInventoryRequest import StoreInventoryRequest
from kol.request.AddItemsToStoreRequest import PutItemInStoreRequest
import threading

s = Session()
searchTerm = "Mr. Accessory"
# how long between each check (seconds)
checkTime = 5
# most you are willing to stock
buyLimit = 10
# how low until buy?
thresholdPrice = 300000
# how much you want to undercut the lowest price on the market
underCut = 10000
# login with your username as password here
s.login("username", "password")

# end options
def pad(word):
	return '"{0}"'.format(word)
def buyItem(storeID, itemID, quantity, price):
	print "Buying {2} of {1} from {0}".format(storeID, itemID, quantity)
	try:
		m = MallItemPurchaseRequest(s, storeID, itemID, price, quantity)
		m.doRequest()
		print "Brought {2} of {1} from {0}".format(storeID, itemID, quantity)
	except:
		print "Buy error, probably someone beat you or you were baleeted."
def sellItem(itemId, price, quantity, limit=""):
	print "Attempting to sell {2} of {0} at {1} each".format(itemId, price, quantity)
	p = PutItemInStoreRequest(s, [{'id': itemId, 'quantity': quantity, 'price': price, 'limit': limit}])
	p.doRequest()
	print "Sold {2} of {0} at {1} each".format(itemId, price, quantity)
def search():
	print "searching"
	m = MallItemSearchRequest(s, pad(searchTerm), noLimits=True)
	res = m.doRequest()["results"]
	inv = StoreInventoryRequest(s)
	inventory = inv.doRequest()
	for item in inventory["items"]:
		if item["id"] == getItemFromName(searchTerm) and item["quantity"] < buyLimit:
			if res[0]["price"] + thresholdPrice < res[1]["price"]:
				buyItem(res[0]["storeId"], getItemFromName(searchTerm), min(buyLimit - item["quantity"], res[0]["quantity"]), res[0]["price"])
				sellItem(getItemFromName(searchTerm), res[1]["price"] - underCut, min(buyLimit - item["quantity"], res[0]["quantity"]))
			else:
				print "Not low enough prices."
		else:
			print "Already have 10 of them. Not buying"
def start():
	t = threading.Timer(checkTime, start)
	search()
	t.start()
start()
