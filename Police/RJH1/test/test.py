import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_onion_image_urls(onion_url, visited_pages=None):
    if visited_pages is None:
        visited_pages = set()

    try:
        # Set up Tor proxy (Make sure Tor is running on port 9050)
        session = requests.session()
        session.proxies = {'http': 'socks5h://localhost:9050', 'https': 'socks5h://localhost:9050'}

        # Send a GET request to the Onion URL
        response = session.get(onion_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all image tags (img) and extract the 'src' attribute
            image_urls = [img['src'] for img in soup.find_all('img', src=True)]

            # Convert relative URLs to absolute URLs
            image_urls = [urljoin(onion_url, img_url) for img_url in image_urls]

            # Add the current page to the visited pages set
            visited_pages.add(onion_url)

            # Find all links (a tags) and recursively fetch image URLs from linked pages
            for link in soup.find_all('a', href=True):
                next_url = urljoin(onion_url, link['href'])
                if next_url not in visited_pages and next_url.endswith('.onion'):
                    # Recursively fetch image URLs from linked pages
                    image_urls += get_onion_image_urls(next_url, visited_pages)

            return image_urls
        else:
            print(f"Failed to retrieve content from {onion_url}. Status code: {response.status_code}")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # Replace 'http://example.onion' with the Onion URL you want to analyze
    target_onion_url = 'http://ly75dbzixy7hlp663j32xo4dtoiikm6bxb53jvivqkpo6jwppptx3sad.onion/'

    # Get image URLs from the Onion site
    image_urls_onion = get_onion_image_urls(target_onion_url)

    if image_urls_onion:
        print("Image URLs on Onion site:")
        for idx, img_url in enumerate(image_urls_onion, start=1):
            if 10 <= idx <= 15:
                print(f"{idx}. {img_url}")
    else:
        print("No image URLs found on Onion site.")
