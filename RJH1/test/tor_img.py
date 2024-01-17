import requests

def get_tor_session():

        session = requests.session()

        session.proxies = {'http':  'socks5h://127.0.0.1:9050',
                       'https': 'socks5h://127.0.0.1:9050'}
        return session
def download_image(url, save_path):
    try:
        # Send a GET request to the URL
        request = get_tor_session()
        response = request.get(url, stream=True)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Open a local file with write-binary mode
        with open(save_path, 'wb') as file:
            # Iterate over the content of the response in chunks and write to the file
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Image downloaded successfully and saved at: {save_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")