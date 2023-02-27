# This File is used to dump and load data to and from the database 

import json
import time, os.path
import pages

class Manager:
    def __init__(self):
        self.dest = os.path.dirname(__file__)+"/../ide/products.json"


    def addProductToInventory(self, name, days, code):
        with open(self.dest, 'r') as fp:
            data = json.load(fp)

        # check if product already has an entry, if not: create one

        if not name in list(data["inventory"].keys()):
            data["inventory"][name] = {}
        

        # search a free index to save prduct in
        freeIndicies = list(range(len(list(data["inventory"][name].keys()))+3)) # at least one has to be free
        if name in data["inventory"]:
            for index in freeIndicies:
                if str(index) not in list(data["inventory"][name].keys()):
                    x = str(index)
                    break
        else: 
            data["inventory"][name] = {}
            x = "0"
        
        # save product
        data["inventory"][name][str(x)] = { 
            "code":code,
            "storedDate":time.time(),
            "days":days,
        }

        # add to / update  known products
        if code != "-1":
            data["knownProducts"][code] = { 
                "code":code,
                "days":days,
                "name":name
            }

        # write changes
        with open(self.dest, 'w') as fp:
            json.dump(data, fp, sort_keys=True, indent=4)
    

    def removeProductFromInventoryByCode(self, code, pVs):
        # remove oldest entry

        with open(self.dest, 'r') as fp:
            data = json.load(fp)
        
        # search for product
        found = False
        
        for product in list(data["inventory"].keys()):
            index = list(data["inventory"][product].keys())[0]
            if code == data["inventory"][product][index]["code"]:
                found = True
                break

        # warn and return if no product is found
        if not found:
            pVs.currentPage = pages.MessagePage(pVs, "no product found in inventory", 2, pages.HomePage)
            return
        
        # if product is in inventory: search for oldest enrty 
        oldest = list(data["inventory"][product].keys())[0]
        for item in list(data["inventory"][product].keys()):
            if data["inventory"][product][item]["storedDate"] < data["inventory"][product][oldest]["storedDate"]:
                oldest = item 

        # remove entry
        data["inventory"][product].pop(oldest, None)
        if len(list(data["inventory"][product].keys())) == 0:
            data["inventory"].pop(product, None)

        with open(self.dest, 'w') as fp:
            json.dump(data, fp, sort_keys=True, indent=4)

        pVs.currentPage = pages.MessagePage(pVs, "successfully removed \" "+product+" \"", 1, pages.HomePage)

    def removeProductFromInventoryByName(self, pVs, name):
        # remove oldest entry

        with open(self.dest, 'r') as fp:
            data = json.load(fp)
        
        # search for product
        found = False
        
        if name in list(data["inventory"].keys()):
            found = True

        # warn and return if no product is found
        if not found:
            pVs.currentPage = pages.MessagePage(pVs, "no product found in inventory", 2, pages.HomePage)
            return
        
        # if product is in inventory: search for oldest enrty 
        oldest = list(data["inventory"][name].keys())[0]
        for item in list(data["inventory"][name].keys()):
            if data["inventory"][name][item]["storedDate"] < data["inventory"][name][oldest]["storedDate"]:
                oldest = item 

        # remove entry
        data["inventory"][name].pop(oldest, None)
        if len(list(data["inventory"][name].keys())) == 0:
            data["inventory"].pop(name, None)

        with open(self.dest, 'w') as fp:
            json.dump(data, fp, sort_keys=True, indent=4)

        pVs.currentPage = pages.MessagePage(pVs, "successfully removed \" "+name+" \"", 1, pages.removeProductPage)
        
    def getInventory(self) -> dict:
        with open(self.dest, "r") as fp:
            data = json.load(fp)
        
        result = {}
        for prodType in list(data["inventory"].keys()):
            result[str(prodType)] = len(list(data["inventory"][prodType].keys()))
        
        return result

    def searchProductByCode(self, code):
        found = False
        name, days = None, None

        with open(self.dest, 'r') as fp:
            data = json.load(fp)
            if str(code) in list(data["knownProducts"].keys()):
                # found entry
                found = True
                name, days = data["knownProducts"][str(code)]["name"], data["knownProducts"][str(code)]["days"]
        return found, name, days

    def checkFiles(self):
        if not os.path.isfile(self.dest):
            f = open(self.dest, "x")
            f.close()

            template = {"inventory":{},"knownProducts":{}}
            with open(self.dest, "w") as fp:
                json.dump(template, fp, sort_keys=True, indent=4)