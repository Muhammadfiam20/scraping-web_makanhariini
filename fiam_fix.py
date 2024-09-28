import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Base URL for the dessert recipe pages
base_url = "https://www.masakapahariini.com/resep/resep-dessert/"

# Function to scrape the data from a single page
def scrape_page(page_url):
    # Set headers to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
    }

    # Send an HTTP request to the page
    response = requests.get(page_url, headers=headers)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the page: {page_url}")
        return []

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # List to store the scraped data
    recipes = []

    # Find all the recipe cards
    recipe_cards = soup.find_all("h3", class_="card-title")

    # Loop through each recipe card and extract the desired information
    for card in recipe_cards:
        # Extract the data-tracking-value from the h3 -> a tag (the recipe title)
        title_tag = card.find("a")
        recipe_title = title_tag['data-tracking-value'] if title_tag else "N/A"

        # Extract the time (span within a link tag with the specified class)
        time_tag = soup.find("a", class_="btn item d-flex align-items-center me-1 me-md-2 mt-3")
        time_text = time_tag.find("span").text if time_tag else "N/A"

        # Extract the difficulty level (text inside the link with the specified class)
        difficulty_tag = soup.find("a", class_="btn item d-flex align-items-center me-1 me-md-2 mt-3 icon_difficulty")
        difficulty_text = difficulty_tag.text.strip() if difficulty_tag else "N/A"

        # Append the collected data to the recipes list
        recipes.append({
            "Title": recipe_title,
            "Time": time_text,
            "Difficulty": difficulty_text
        })

    # Remove the last 3 items if there are more than 3 items
    if len(recipes) > 3:
        recipes = recipes[:-3]

    return recipes

# Function to scrape data from multiple pages
def scrape_all_pages(num_pages=5):
    # Create the output directory if it doesn't exist
    output_directory = r'C:\Users\Zahra Delafiana Zaki\Downloads\sc_masak'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Loop through the specified number of pages
    for page_num in range(1, num_pages + 1):
        # Construct the URL for each page
        if page_num == 1:
            page_url = base_url  # First page does not have "/page/1"
        else:
            page_url = base_url + f"page/{page_num}/"
        print(f"Scraping page {page_num}: {page_url}")
        
        # Scrape the data from the current page
        recipes = scrape_page(page_url)
        
        # Convert the scraped data into a pandas DataFrame
        df = pd.DataFrame(recipes)
        
        # Define the output file path for each page
        output_file = os.path.join(output_directory, f'scraped_recipes_page_{page_num}.xlsx')
        
        # Save the DataFrame to an Excel file for the current page
        df.to_excel(output_file, index=False)
        
        print(f"Data from page {page_num} saved to {output_file}")

# Scrape data from the first 5 pages
scrape_all_pages(5)
