import random
import pandas as pd
from datetime import datetime

def get_product_price(product="iPhone"):
    # Mock API (replace with real API or BeautifulSoup scraping)
    price = random.randint(500, 1000)
    return pd.DataFrame([{"timestamp": datetime.now(), "product": product, "price": price}])
