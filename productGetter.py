import openfoodfacts as off 


class ProductGetter:
        def __init__(self) -> None:
                pass
        
        def getProduct(self, barcode):
                product = off.products.get_product(barcode.strip()) # search openFoodFact database for a product using the barcode
                if product["status"]:   # if successful
                        try:    
                                productName = product["product"]["product_name"]
                                try:    return  { 
                                                "name":product["product"]["product_name"],
                                                "brand":product["product"]["brands"]
                                        }
                                except: print("Brand or name not given") 
                        except: return 0
                else:
                        return 0
