import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Scrape book data
url = "http://books.toscrape.com"
response = requests.get(url)
response.encoding = 'utf-8'  # Fix encoding issue
soup = BeautifulSoup(response.text, "html.parser")

books = soup.select('.product_pod')

titles = []
prices = []
ratings = []

rating_dict = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}

for book in books:
    title = book.h3.a['title'] if book.h3 and book.h3.a.has_attr('title') else "Unknown Title"
    
    price_elem = book.select_one('.price_color')
    price = float(price_elem.text.strip().replace('£', '')) if price_elem else 0.0
    
    rating_elem = book.select_one('p.star-rating')
    rating_class = rating_elem['class'][1] if rating_elem and len(rating_elem['class']) > 1 else 'Zero'
    rating = rating_dict.get(rating_class, 0)
    
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

print("Data saved to books.csv")

# Plot: Average Price by Rating
avg_price_per_rating = df.groupby("Rating")["Price"].mean()

plt.figure(figsize=(8, 5))
avg_price_per_rating.plot(kind='bar')
plt.title("Average Book Price by Rating")
plt.xlabel("Rating")
plt.ylabel("Average Price (£)")
plt.grid(axis='y')
plt.tight_layout()
plt.show()
