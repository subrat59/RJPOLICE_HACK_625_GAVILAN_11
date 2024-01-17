from DScrap.models import TitleLink,Title
from django.core.management.base import BaseCommand
from argparse import ArgumentParser
from tbselenium.tbdriver import TorBrowserDriver
from tbselenium.utils import start_xvfb, stop_xvfb
from os.path import join, dirname, realpath
# Connect to the SQLite database
all_objects = Title.objects.all()
tbb_dir="/home/anonymous/Downloads/tor-browser"
class Command(BaseCommand):
    help = 'Prints the titles of all Posts'
    
    def take_screenshot(self,links_set):
      
    # start a virtual display
        xvfb_display = start_xvfb()
        i = 4
        with TorBrowserDriver(tbb_dir) as driver:
            for url in links_set:
                print(url)
                driver.load_url(url)
                out_img = join(dirname(realpath(__file__)), f"h{i}.png")
        # driver.get_screenshot_as_file(out_img)
                driver.get_full_page_screenshot_as_file(out_img)
                
                print("Screenshot is saved as %s" % out_img)
                i+=1



    def handle(self, *args, **options):
        links_set = []
        for i in Title.objects.all():
            links_set.append(i.link)
        links_set=set(links_set)
            
        self.take_screenshot(links_set)

