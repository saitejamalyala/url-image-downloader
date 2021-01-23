import urllib.request,urllib, bs4, wget, click
from tqdm import tqdm
import os, sys



__author__  = "Saiteja Malyala"
__version__ = "0.1"


#web_url = 'https://www.heisig.com/aktuelle-auftraege/drehen'
#download_directory = pathlib.Path('.\downloaded_images')

@click.command()
@click.option('--web_url', prompt = 'Enter the Url', help= 'Enter the website address where images are located')
@click.option('--download_directory', prompt = 'Path to Directory', help= 'Enter the website address where images are located')


def get_all_images_from_url(web_url,download_directory):

    '''
    Purpose: To download all Images from a provided Url to a local directory
    Inputs : url (from where the images are supposed to be downloaded)

    '''
    #check if entered url is valid
    check_validity(web_url)

    # get the html page
    website_html = urllib.request.urlopen(web_url).read()

    # parse the html page using a parser
    website_parse_page = bs4.BeautifulSoup(website_html, 'html.parser')

    # get details of the web url like scheme, hostname, netloc etc.
    base = urllib.request.urlparse(web_url)

    links = []

    #Parse Through the html page to find href's to get links to download images of all different formats 
    for attachment in tqdm(website_parse_page.find_all('a')):
        link_in_page = attachment.get('href')
        link_in_page = str(link_in_page)
        # check if any attachment is of image format (Supported formats: .tif,.tiff,.png,.jpg,.svg)
        if (link_in_page.endswith(('tif','tiff','jpg','png','svg'))):
            
            links.append(base.scheme+'://'+base.hostname + link_in_page)

    print("\nFound {} Images in the provided url.".format(len(links)))

    # Download all the links found for the images
    print('\nNow downloading {} Images.......... \n'.format(len(links)))
    for download_link in tqdm(links):  
        try: 
            # check if directory exists, if no create the directory
            if not os.path.exists(download_directory):
                #print('\n','Creating Directory to save downloaded Images.\n')
                os.makedirs(download_directory)
                #os.makedirs(download_directory.split('\\')[-1])
            wget.download(download_link,out=download_directory,bar=None)

        except:

            print('\nUnable to download a file. \n')
    print('\nDownload completed. check {} folder for downloaded images. \n'.format(str(download_directory)))

def check_validity(web_url):
    try:
        urllib.request.urlopen(web_url)
        print("Valid URL")
    except IOError:
        print ("Invalid URL")
        sys.exit()

if __name__ == '__main__':

    get_all_images_from_url()

