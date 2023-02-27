# this file contains the actual openFoodFacts api call and delivers a result to the scanPage

import openfoodfacts as off 


class ProductGetter:
        def __init__(self) -> None:
                pass
        
        def getProduct(self, barcode):
                product = off.products.get_product(barcode.strip()) # search openFoodFact database for a product using the barcode
                if product["status"]:   # if successful
                        result = {}
                        try:
                                result["name"] = product["product"]["product_name"]
                        except:
                                pass

                        try:
                                result["brand"] = product["product"]["brands"]
                        except:
                                pass

                        if not len(list(result.keys())):
                                result = 0

                        return result
