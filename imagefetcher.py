"""
    Fetches images from a URL and saves them in /out.
"""
import sys
import os
import requests
import re

url = str(sys.argv[1]) # get the website
output_dir = str(sys.argv[2]) if len(sys.argv) > 2 else "out"

if ("http" not in url):
    url = "http://" + url
r = requests.get(url) # get the html
page = r.content

# Check to see if there's an output directory
os.makedirs(output_dir, exist_ok=True)

from html.parser import HTMLParser

class ImageParser(HTMLParser):
    def __init__(self):
        super(ImageParser, self).__init__() # call super init
        self.image_count = 0

    def handle_starttag(self, tag, attrs):
        if (tag != 'img'): return # don't do anything for non-image tags
        img_url = ""
        for (key, val) in attrs:
            if (key == 'src'):
                print(val)
                img_url = val # get the image url

        if img_url != "": # if the image isn't blank, write the file
            if ('http://' not in img_url and "https://" not in img_url): # no http protocol?
                match = re.search("\/\/[\w+\.\w+]+\/", img_url)
                domain = match.group(0) if match else None
                if (domain): # has domain
                    img_url = "http:" + img_url
                else:
                    img_url = url + img_url

            print("img: " + str(img_url))
            if img_url != "": # if image still not null after some parsing
                spl = img_url.split(".")
                fext = str(spl[-1])
                if (len(fext) != 3): fext = "jpg" # default to jpg

                f = open(output_dir + "/image_" + str(self.image_count) + "." + fext, "wb") # save the image
                img = requests.get(img_url).content # get raw data
                f.write(img) # write the image data
                f.close() # close the file

            self.image_count += 1 # increment the image count

IP = ImageParser()
IP.feed(str(page))
