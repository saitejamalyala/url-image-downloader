import asyncio
import os
import sys
import urllib
import urllib.request
from typing import Optional
from urllib.parse import ParseResult

import aiofiles
import aiohttp
import bs4
import click
from tqdm import tqdm

__author__ = "Saiteja Malyala"
__version__ = "0.1"

SUPPORTED_IMAGE_EXTS = ('tif', 'tiff', 'jpg', 'png', 'svg')
""" List of the Image Extensions that shall be downloaded """


@click.command()
@click.option('--web_url', prompt='Enter the Url', help='Enter the website address where images are located')
@click.option('--download_directory', prompt='Path to Directory', help='Enter the website address where images are located')
def get_all_images_from_url(
    web_url: str,
    download_directory: str
) -> None:
    '''
    Purpose: To download all Images from a provided Url to a local directory
    Inputs :  1. url (from where the images are supposed to be downloaded)
              2. download_directory (directory to save the downloaded images)

    NOTE: asyncio will help a lot speeding up the process
    '''
    asyncio.run(async_get_all_images_from_url(web_url, download_directory))


async def async_get_all_images_from_url(
    web_url: str,
    download_dir: str
) -> None:
    """ Asyncionous version of get_all_images_from_url()

    Args:
        web_url (str): Base URL of the page on which we are looking for images.
        download_dir (str): Local path where we want to store the downloaded
            images.
    """

    # get the html page and stop execution if the page could not be fetched
    website_html = await _load_page(web_url)
    if website_html is None:
        _handle_invalid_parent_url()

    # parse the html page using a parser
    website_parse_page = bs4.BeautifulSoup(website_html, 'html.parser')

    # build an iterator to go through all links on the page.
    # We want to have them as strings for subsequent processing
    attachment_iter = (
        str(a.get('href')) for a in website_parse_page.find_all('a'))

    # get details of the web url like scheme, hostname, netloc etc.
    base = urllib.request.urlparse(web_url)

    # filter those links that are actually images.
    # NOTE: we could use the filter() function, but we want to print
    # the number of found files, so a list is the better data tyoe.
    links = [
        _make_link_absolute(base, str(link_in_page))
        for link_in_page in attachment_iter
        if link_in_page.endswith(SUPPORTED_IMAGE_EXTS)
    ]

    # make sure the user knows what she is waiting for
    links_tally = len(links)
    print(f"\nFound {links_tally} Images in the provided url.")

    # Download all links found for images
    print(f"\nNow downloading {links_tally} Images.......... \n")
    tasks = [_download_binary_file(cur_link, download_dir)
             for cur_link in links]
    [await f for f in tqdm(asyncio.as_completed(tasks), total=len(tasks))]

    print(
        f"\nDownload completed. check {download_dir} folder for downloaded images. \n")


async def _download_binary_file(
    url: str,
    download_dir: str
) -> None:
    """ Download the file located at url to the local
    directory download_dir

    Args:
        url (str): Loation of the File to download
        download_directory (str): local directory in which
            to store the file
    """

    # ensure that the output directory exists
    try:
        os.makedirs(download_dir)
    # CAUSE: download_dir exists
    # SPEED: faster to catch than to check
    # ACTION: ignore, directory exists
    except FileExistsError:
        pass

    # CAUSE: not able to write on the local fs
    # SPEED: faster to chatch than to check
    # ACTION: stop here, tell the user
    except OSError:
        raise

    # asyncronously stream result into local file
    filename = os.path.basename(url)
    dst = os.path.join(download_dir, filename)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if 200 <= resp.status < 300:
                async with aiofiles.open(dst, 'wb') as fid:
                    await fid.write(await resp.read())
            else:
                print(f"\nUnable to download file{filename}. \n")


def _make_link_absolute(
    base: ParseResult,
    link_in_page: str
) -> str:
    """ Create an absolute url from a link on the
    page. The link can either be relative
    (e.g., start with '.'), relative to the
    tld (e.g., start with '/'), or be
    absolute (e.g., start with 'http://')

    Args:
        base (ParseResult): Base Url
        link_in_page (str): link on the page

    Returns:
        str: Absolute page
    """

    if link_in_page.startswith(("http://", "https://", ".")):
        raise NotImplementedError()
    # !!! still open to malicious injection!
    return base.scheme+'://'+base.hostname + str(link_in_page)


async def _load_page(web_url: str) -> Optional[str]:
    """ Load a page located as web_url and
    if the page could be found, return its body.
    Otherwise return None

    Args:
        web_url (str): Url that is requested

    Returns:
        Optional[str]: Content of the webseite if
            status code was in the 200s. Otherwise
            None.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(web_url) as response:
            if 200 <= response.status < 300:
                return await response.text()
            return None


def _handle_invalid_parent_url() -> None:
    print("Invalid URL")
    # NOTE JM: sys.exit() indicates successful termination.
    #   If you added the code to a CICD pipeline, the pipeline
    #   would continue to run
    sys.exit(1)


if __name__ == '__main__':
    get_all_images_from_url()
