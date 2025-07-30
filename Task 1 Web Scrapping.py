import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

# Step 1: Scrape book data
url = "http://books.toscrape.com"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

books = soup.select('.product_pod')

titles = []
prices = []
ratings = []

for book in books:
    title = book.h3.a['title']
    price = book.select_one('.price_color').text.strip().replace('£', '')
    rating_class = book.select_one('p.star-rating')['class'][1]
    
    titles.append(title)
    prices.append(float(price))
    
    # Convert rating text to number
    rating_dict = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    ratings.append(rating_dict.get(rating_class, 0))

# Step 2: Create DataFrame
df = pd.DataFrame({
    "Title": titles,
    "Price": prices,
    "Rating": ratings
})

df.to_csv("books.csv", index=False)
