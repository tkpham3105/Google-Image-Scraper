# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 11:02:06 2020

@author: OHyic

"""
#Import libraries
import os
from collections import deque
from multiprocessing import Process 
from GoogleImageScrapper import GoogleImageScraper
from patch import webdriver_executable

if __name__ == "__main__":
    #Define file path
    webdriver_path = os.path.normpath(os.path.join(os.getcwd(), 'webdriver', webdriver_executable()))
    image_path = os.path.normpath(os.path.join(os.getcwd(), 'photos'))

    #Add new search key into array ["cat","t-shirt","apple","orange","pear","fish"]
    search_keys= ['Breathing Apparatus firefighter']

    #Parameters
    number_of_images = 20
    headless = True
    min_resolution=(0,0)
    max_resolution=(9999,9999)

    #Threading
    queue = deque()
    def scrapping(scrapper):
        scrapper.find_image_urls(queue)
    def downloading(scrapper):
        scrapper.save_images(queue)
    #Main program
    processes = []
    for search_key in search_keys:
        image_scrapper = GoogleImageScraper(webdriver_path,image_path,search_key,number_of_images,headless,min_resolution,max_resolution)
        scrapper = Process(target=scrapping, args=(image_scrapper,))
        downloader = Process(target=downloading, args=(image_scrapper,))
        scrapper.start()
        downloader.start()
        processes.append(scrapper)
        processes.append(downloader)
        #image_urls = image_scrapper.find_image_urls()
        #image_scrapper.save_images(image_urls)
    for process in processes:
        process.join()

    #Release resources    
    del image_scrapper