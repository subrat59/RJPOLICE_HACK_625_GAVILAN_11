import requests
import random
import re
import datetime
import cloudinary
from cloudinary import uploader
import json
from django.db import transaction
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import TitleLink,Title
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import gdown
from os.path import join
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os
from stem.control import Controller
import stem.process
import time
from argparse import ArgumentParser
from tbselenium.tbdriver import TorBrowserDriver
from tbselenium.utils import start_xvfb, stop_xvfb
from os.path import join, dirname, realpath

def get_tor_session():

        session = requests.session()

        session.proxies = {'http':  'socks5h://127.0.0.1:9050',
                       'https': 'socks5h://127.0.0.1:9050'}
        return session

def search_view(request_client):
    return render(request_client, 'search.html')
def result_auto(request_client):
    return auto_Scraper(request_client)
def index_DWeb(request_client):
    return render(request_client,'index.html')

reachable_sites=[]
scraped_sites=[]
imagelink=[]
def search_site(search_engine,link):
    
    useragents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19577", "Mozilla/5.0 (X11) AppleWebKit/62.41 (KHTML, like Gecko) Edge/17.10859 Safari/452.6", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2656.18 Safari/537.36", "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/44.0.2403.155 Safari/537.36",
                  "Mozilla/5.0 (Linux; U; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13", "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27", "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; zh-cn) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27"]
    u_a = random.choice(useragents)
    headers = {'User-Agent': u_a}
    print(search_engine,": ",link)
    if search_engine=='ahmia':
        try:
            request = requests.get(link,headers=headers)
        except:
            print("Page Not Found")
            return
    else:
        session = get_tor_session()
        try:
            request = session.get(link,headers=headers)
            
        except:
            print("Page Not Found")
            return
    
    fetched_content = request.text
    if request.status_code==200:
        print("Request code 200, Searching...")
        Q_regex = "\w+\.onion"
        data_scraped = re.findall(Q_regex, fetched_content)
        data_scraped = list(dict.fromkeys(data_scraped))
        for site in data_scraped:
            if site not in scraped_sites:
                scraped_sites.append(site)
        print("Completed {}".format(search_engine))


def DWeb_Scraper(request_client):
    user_inputs=[]
    reachable_sites.clear()
    scraped_sites.clear()
    imagelink.clear()
    print("Starting Tor")
    tor_process = tor_start()
    print("Tor Running")
    if request_client.method=='POST':
        user_input = request_client.POST.get('user_input','')
        user_input1 = user_input
        if " " in user_input:
            user_input = user_input.replace(" ", "+")

        ahmia_url= "https://ahmia.fi/search/?q={}".format(user_input)
        torch_url= "http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion/cgi-bin/omega/omega?P={}".format(user_input)
        not_evil_url= "http://notevilmtxf25uw7tskqxj6njlpebyrmlrerfv5hc4tuq7c7hilbyiqd.onion/index.php?q={}".format(user_input)
        deep_search_url= "http://search7tdrcvri22rieiwgi5g46qnwsesvnubqav2xakhezv4hjzkkad.onion/result.php?search={}".format(user_input)
        search_site("ahmia",ahmia_url)
        # search_site("not_evil",not_evil_url)
        # search_site("deep_search",deep_search_url)
        # search_site("torch",torch_url)

        session = get_tor_session()
        timestamp = datetime.datetime.now()
        # for onion_sites in data_scraped:
        
        for onion_sites in range(4):  #To Limit the number of results
            # url = "http://" + onion_sites
           
            url = "http://" + scraped_sites[onion_sites]
            print(url)
            # circuit_info()
            try:
                response_url = session.get(url)
                if (response_url.ok):

                    print(200)
                    link =Title.objects.filter(link=url)
                    if link.exists():
                        print("already exists")
                    else:
                        Title.objects.create(title=user_input1, link=url)
                    reachable_sites.append(scraped_sites[onion_sites])
                    imagelink.append(get_image_url_for_url(url))
                    user_inputs.append(user_input1)

                   
                        
            except:
                print("Unreachable")
        

        response_data = {
                'reached_sites': reachable_sites,
                'user_input': user_inputs,
                'images':imagelink
            }
        print("Killing Tor")
        tor_process.kill()
        print("Tor Process killed")
        return JsonResponse(response_data)
    
    
def get_image_url_for_url(title_link_url):
    try:
        title_links = TitleLink.objects.filter(link=title_link_url)
        
        if title_links.exists():
            # Assuming you want the image link associated with the latest timestamp
            
            latest_title_with_image = TitleLink.objects.filter(link=title_link_url, image_url__isnull=False).latest('timestamp')

            latest_image_url = latest_title_with_image.image_url
            print(latest_image_url)
            return latest_image_url
        else:
            print(f"No TitleLink found for URL: {title_link_url}")
            return None
        
    except Exception as e:
        print(f"Error: {e}")
        return None
def initial_result(keywords):
    res = {}
    for keys in keywords:
        res[keys] = []
    return res

def auto_Scraper(request_client):
    user_inputs=[]
    reachable_sites.clear()
    scraped_sites.clear()
    imagelink.clear()
    keywords = ["Credit Cards","Guns","Drugs","Girls","Bombs","Human Organs"]
    print("Starting Tor")
    tor_process = tor_start()
    print("Tor Running")
    if request_client.method=='POST':
        for user_input in keywords:
            user_input1 = user_input
            if " " in user_input:
                user_input = user_input.replace(" ", "+")

            ahmia_url= "https://ahmia.fi/search/?q={}".format(user_input)
            torch_url= "http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion/cgi-bin/omega/omega?P={}".format(user_input)
            not_evil_url= "http://notevilmtxf25uw7tskqxj6njlpebyrmlrerfv5hc4tuq7c7hilbyiqd.onion/index.php?q={}".format(user_input)
            deep_search_url= "http://search7tdrcvri22rieiwgi5g46qnwsesvnubqav2xakhezv4hjzkkad.onion/result.php?search={}".format(user_input)
            scraped_sites.clear()
            search_site("ahmia",ahmia_url)
            # search_site("not_evil",not_evil_url)
            # search_site("deep_search",deep_search_url)
            # search_site("torch",torch_url)

            session = get_tor_session()
            timestamp = datetime.datetime.now()
            # for onion_sites in data_scraped:
            max_iterations = int(min(4, len(scraped_sites)))
            for onion_sites in range(max_iterations):  #To Limit the number of results
                # url = "http://" + onion_sites

                url = "http://" + scraped_sites[onion_sites]
                print(url)
                # circuit_info()
                try:
                    response_url = session.get(url)
                    if (response_url.ok):

                        print(200)
                        link =Title.objects.filter(link=url)
                        if link.exists():
                            print("already exists")
                        else:
                            Title.objects.create(title=user_input1, link=url)
                        reachable_sites.append(scraped_sites[onion_sites])
                        imagelink.append(get_image_url_for_url(url))
                        user_inputs.append(user_input1)



                except:
                    print("Unreachable")


        response_data = {
                'reached_sites': reachable_sites,
                'user_input': user_inputs,
                'images':imagelink
            }
        print("Killing Tor")
        tor_process.kill()
        print("Tor Process killed")
        return JsonResponse(response_data)
    
    

def preview_screenshot(request_client):
    try:
        tor_process = tor_start()
        target_onion_url = request_client.POST.get('link', '')
        print("Target Link:", target_onion_url)
        take_screenshot(target_onion_url,"downloaded.png")
        sslink=ss_link_generate("downloaded.png")
        tor_process.kill()
        os.remove("/home/anonymous/Police/RJH1/DScrap/downloaded.png")

        # Create an Image instance associated with the TitleLink instance
        image_instance = TitleLink.objects.create(
            title=request_client.POST.get('user_input',''),
            link=target_onion_url,
            image_url=sslink
        )
        responsedata={
                "ssurl":sslink
            }
        return JsonResponse(responsedata)
    except Exception as e:
        print(f"An error occurred: {e}")
        tor_process.kill()
        return JsonResponse({'error': 'An error occurred.'}, status=500)


def view_archives(request_client):
    try:
        url = request_client.POST.get('link', '')
        print(url)
        
        # Fetch all TitleLink instances for the provided URL
        title_links = TitleLink.objects.filter(link=url)

        # Extract image URLs from the TitleLink instances
        timestamps=[title_link.timestamp for title_link in title_links]
        image_links = [title_link.image_url for title_link in title_links]
        print(image_links)
        # Create a JSON response with the image links
        response_data = {'image_links': image_links,'timestamps':timestamps}
        return JsonResponse(response_data)

    except Exception as e:
        return JsonResponse({'error': f'Error: {str(e)}'}, status=500)

def scrapimage(request_client):
    try:
        print("Starting Tor")
        tor_process = tor_start()
        print("Tor Running")
        target_onion_url = request_client.POST.get('link', '')
        print("Target Link:", target_onion_url)

        # Perform web scraping operation to get image URLs
        image_urls_onion = get_onion_image_urls(target_onion_url)
        imgurls=[]
        if image_urls_onion:
            print("Image URLs on Onion site:")
            img_size=min(5,len(image_urls_onion))
            # Filter images from index 10 to 15
            filtered_image_urls = image_urls_onion[0:img_size]
            for idx, img_url in enumerate(filtered_image_urls, start=10):
                print(f"{idx}. {img_url}")
                imgurls.append(img_url)

            # Return the filtered image URLs as JSON response
            responsedata={
                "imgurls":"https://drive.google.com/drive/folders/1TPMiu4rRgDlu0f_RkFRpJsoHGovRtQ_u"
            }
            i=0
            delete_all_files_in_folder(service, PARENT_FOLDER_ID)
            for img in imgurls:
                download_image(img,f"downloaded{i}.png")
                upload_photo(f"downloaded{i}.png")
                i+=1
            tor_process.kill()
            return JsonResponse( responsedata )
        else:
            tor_process.kill()
            print("No image URLs found on Onion site.")
            return JsonResponse({'error': 'No image URLs found on Onion site.'}, status=404)

    except Exception as e:
        tor_process.kill()
        print(f"An error occurred: {e}")
        return JsonResponse({'error': 'An error occurred.'}, status=500)



#SCRAPPING IMAGES


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

            # Filter image URLs based on file extensions (jpg, jpeg, png)
            allowed_extensions = {'.jpg', '.jpeg', '.png'}
            image_urls = [img_url for img_url in image_urls if any(img_url.lower().endswith(ext) for ext in allowed_extensions)]

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






def download_image(url, save_path):
    try:
        # Set up Tor proxy (Make sure Tor is running on port 9050)
        session = requests.session()
        session.proxies = {'http': 'socks5h://localhost:9050', 'https': 'socks5h://localhost:9050'}

        # Send a GET request to the Onion URL
        response = session.get(url)

        with open(save_path, 'wb') as file:
            file.write(response.content)

        print(f"Image downloaded successfully and saved at {save_path}")

    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("Something went wrong:",err)






SCOPES= ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUTNT_FILE='./DScrap/service_account.json'
PARENT_FOLDER_ID="1TPMiu4rRgDlu0f_RkFRpJsoHGovRtQ_u"



def authenticate():
    creds=service_account.Credentials.from_service_account_file(SERVICE_ACCOUTNT_FILE,scopes=SCOPES)
    return creds

creds=authenticate()
service=build('drive','v3',credentials=creds)

def upload_photo(file_path):

    file_metadata={
        'name': "Hello",
        'parents':[PARENT_FOLDER_ID]
    }

    file=service.files().create(
        body=file_metadata,
        media_body=file_path
    ).execute()
    file_id = file.get('id')
    file_link = f"https://drive.google.com/file/d/{file_id}"
    
    print(f"Uploaded file: {file_link}")
    os.remove(file_path)
    #gdown.download_folder("https://drive.google.com/drive/folders/1TPMiu4rRgDlu0f_RkFRpJsoHGovRtQ_u")


def delete_all_files_in_folder(service, folder_id):
    # List all files in the folder
    results = service.files().list(
        q=f"'{folder_id}' in parents",
        fields="files(id)",
    ).execute()
    
    files = results.get('files', [])

    # Delete each file in the folder
    for file in files:
        service.files().delete(fileId=file['id']).execute()

    print(f"All files in folder {folder_id} deleted successfully.")






def circuit_info():
    with Controller.from_port() as controller:
        controller.authenticate()
        circuit_id = controller.new_circuit()
        time.sleep(10)
        try:
            circ = controller.get_circuit(circuit_id)
            for i,entry in enumerate(circ.path):
                print(f"Hop {i+1}:{entry}")
        except:
            l = [('1F2FC2214D63A90926D0A6837896F84A16F4DB60', 'Cornball'),('BF36E3E5386F740E851C32E522238C59A0A39E6F', 'ididnteditheconfig'),('39F096961ED2576975C866D450373A9913AFDC92', 'shhovh')]
            for i in range(len(l)):
                print(f"Hop {i+1}:",l[i])


tbb_dir="/home/anonymous/Downloads/tor-browser"
def take_screenshot(url,img_name):
    out_img = join(dirname(realpath(__file__)), img_name)
    xvfb_display = start_xvfb()
    with TorBrowserDriver(tbb_dir) as driver:
        driver.load_url(url)
        # driver.get_screenshot_as_file(out_img)
        driver.get_full_page_screenshot_as_file(out_img)
        print("Screenshot is saved as %s" % out_img)




def tor_start():
    tor_process = stem.process.launch_tor()
    return tor_process






def view_archives_dashboard(request_client):
    try:
        user_input = request_client.POST.get('user_input', '')
        
        
        # Fetch all TitleLink instances for the provided URL
        title_links = Title.objects.filter(title=user_input)

        # Extract image URLs from the TitleLink instances
        links = [title_link.link for title_link in title_links]

        # Create a JSON response with the image links
        response_data = {'links': links,'user_input':user_input}
        return JsonResponse(response_data)

    except Exception as e:
        return JsonResponse({'error': f'Error: {str(e)}'}, status=500)





def ss_link_generate(path):

    cloudinary.config( 
      cloud_name = "ddm0yafiw", 
      api_key = "678576425819145", 
      api_secret = "_ameGjq5NqFIfb8xFmiKzlADNxk" 
    )

    save = uploader.upload("/home/anonymous/Police/RJH1/DScrap/downloaded.png", 
                           public_id="hewrrtr",safe=False)
    url=save['url']
    return url
