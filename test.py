import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "9hETYJpxw5MdFEc4xYy9Q", "isbns": "9781632168146"})
print(res.json())
