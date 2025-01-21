import requests
from bs4 import BeautifulSoup

def scrape_and_save(url, filename):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP errors

        # Parse the webpage content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all text from the webpage
        page_text = soup.get_text()

        # Save the text to a .txt file
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(page_text)

        print(f"Content successfully saved to {filename}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Input URL from the user
    url = input("Enter the URL to scrape: ")
    filename = "scraped_content.txt"

    scrape_and_save(url, filename)
