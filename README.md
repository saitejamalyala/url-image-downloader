## url-image-downloader
Python script to download images from a provided url


- Instantly download all necessary image files from the url

## Step 1: 
 [Download](https://github.com/saitejamalyala/url-image-downloader/archive/main.zip) or [clone](https://github.com/saitejamalyala/url-image-downloader.git) the repository, and cd to the script directory

## Step 2: 
 Install the [Requirements](https://github.com/saitejamalyala/url-image-downloader/blob/main/requirements.txt) to run the python script get_images.py

  -To install the requirements using pip run the below command in your terminal
    ```
    pip install -r requirements.txt
    ```

## Step 3: 
**How to Use:** 

- Download the Python script and run it on your terminal

  ```
  python3 get_images.py --web_url 'https://www.heisig.com/aktuelle-auftraege/drehen' --download_directory 'downloaded_images'
  ```
  
- Or to give inputs through a prompt 
  ```
  python3 get_images.py 
  ```
  - Enter the url
  ```
  Enter the Url: https://www.heisig.com/aktuelle-auftraege/drehen (example url)
  ```
  - Enter Directory name to store images
  ```
  Path to Directory: .\dir_images 
  ```
- Watch the progress of the download  
  Valid URL  
  Found 60 Images in the provided url.  
  Now downloading 60 Images..........  
 100% ███████████████████████████████████████████████████| 60/60 [00:14<00:00,  4.20it/s]  
 
 Download completed. check .\dir_images folder for downloaded images.
