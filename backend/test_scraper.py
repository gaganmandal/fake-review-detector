from scraper import get_flipkart_reviews

url = "https://www.flipkart.com/bumchums-printed-men-multicolor-bermuda-shorts/product-reviews/itm9c11ad9dca3b4?pid=SRTGVGJGUXXYGHNZ&lid&marketplace=FLIPKART"

reviews = get_flipkart_reviews(url)

for r in reviews:
    print(r)