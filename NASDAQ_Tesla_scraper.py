
def save_article_to_csv(url, filename="output.csv"):
    try:
        HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
        }
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        content = soup.find("div", class_="body__content")
        
        if not content:
            print("Error: Specified content not found on the page.")
            return
        
        # Extract paragraphs
        paragraphs = [p.get_text(strip=True) for p in content.find_all("p")]
        
        # Extract sentences
        sentences = []
        for paragraph in paragraphs:
            sentences.extend(re.split(r'(?<=[.!?]) +', paragraph))
        
        # Extract headers
        headers = [header.get_text(strip=True) for header in content.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])]
        
        # Write to CSV and remove empty rows
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["*******************Sentences*******************"])
            writer.writerows([[sentence] for sentence in sentences if sentence.strip()])
            
            writer.writerow(["*******************Paragraphs*******************"])
            writer.writerows([[paragraph] for paragraph in paragraphs if paragraph.strip()])
            
            writer.writerow(["*******************Headers*******************"])
            writer.writerows([[header] for header in headers if header.strip()])
        
        print(f"Cleaned data saved to {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

# Put in URL
url = "https://www.nasdaq.com/articles/tesla-stock-surged-695-in-2020.-is-it-a-buy-for-2021-2020-12-31"
save_article_to_csv(url, "content.csv")
