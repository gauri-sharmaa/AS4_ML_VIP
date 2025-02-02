import requests
from bs4 import BeautifulSoup
import csv
import re

def save_article_to_csv(url, filename="output.csv"):
    try:
        # Headers to mimic a browser request
        HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
        }
        
        if not content:
            print("Error: Specified content not found on the page.")
            return

        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Content is in the article element not body__content
        content = soup.find("article")
        
        if not content:
            print("Error: Article content not found on the page.")
            return
        
        # Extract title
        title = soup.find("h1")
        title_text = title.get_text(strip=True) if title else "No title found"
        
        # Extract paragraphs
        paragraphs = [p.get_text(strip=True) for p in content.find_all("p")]

        
        # Extract sentences
        sentences = []
        for paragraph in paragraphs:
            split_sentences = re.split(r'(?<=[.!?])(?=\s|$)', paragraph)
            sentences.extend([s.strip() for s in split_sentences if s.strip()])
        
        # Write to CSV
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            
            # Write title
            writer.writerow(["*******************Title*******************"])
            writer.writerow([title_text])
            
            # Write sentences
            writer.writerow(["*******************Sentences*******************"])
            writer.writerows([[sentence] for sentence in sentences if sentence])
            
            # Write paragraphs
            writer.writerow(["*******************Paragraphs*******************"])
            writer.writerows([[paragraph] for paragraph in paragraphs if paragraph])
        
        print(f"Article content saved to {filename}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


url = "https://finance.yahoo.com/news/why-did-facebook-shares-fall-225006922.html"
save_article_to_csv(url, "yahoo_finance_article.csv")