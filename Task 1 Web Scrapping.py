import requests
from bs4 import BeautifulSoup
import pandas as pd

# Step 1: Scrape book data
url = "http://books.toscrape.com"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

books = soup.select('.product_pod')

titles = []
prices = []
ratings = []

rating_dict = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}

for book in books:
    # Extract title attribute
    title = None
    if book.h3 and book.h3.a and book.h3.a.has_attr('title'):
        title = book.h3.a['title']
    else:
        title = "Unknown Title"
    
    # Extract price and convert to float 
    price_elem = book.select_one('.price_color')
    if price_elem and price_elem.text:
        price_text = price_elem.text.strip()
        price = float(price_text.replace('£', ''))
    else:
        price = 0.0
    
    # Extract rating as number using class name
    rating_elem = book.select_one('p.star-rating')
    if rating_elem and 'class' in rating_elem.attrs and len(rating_elem['class']) > 1:
        rating_class = rating_elem['class'][1]
        rating = rating_dict.get(rating_class, 0)
    else:
        rating = 0
    
    titles.append(title)
    prices.append(price)
    ratings.append(rating)

# Step 2: Create DataFrame
df = pd.DataFrame({
    "Title": titles,
    "Price": prices,
    "Rating": ratings
})

# Save to CSV
df.to_csv("books.csv", index=False)

print(df.head())
