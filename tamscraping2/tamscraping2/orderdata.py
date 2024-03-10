import json
import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.tamscraping2 import Newscraping  # Adjust the import path based on your project structure

json_strings = []

def extract_json_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Pattern to search for
    pattern_start = '{"__typename":"StaySearchResult","listing'
    pattern_end = '},{"__typename":"StaySearchResult","listing'

    # List to hold all JSON strings
    #json_strings = []
    start = 0

    while True:
        # Locate the JSON string in the HTML content
        start = html_content.find(pattern_start, start)
        if start == -1:  # No more patterns found
            break
        end = html_content.find(pattern_end, start) + 1
        if end == 0:  # No end pattern found, break the loop
            break

        # Extract the JSON string
        json_string = html_content[start:end]
        json_strings.append(json_string)

        # Update the start position for the next search
        start = end

    return json_strings


def parse_data_(json_string_):

    # Remove the leading and trailing single quotes
    # Trim or clean your JSON string if necessary
    # For example, if your string has leading and trailing single quotes, you can remove them:
    if json_string_.startswith("'") and json_string_.endswith("'"):
        json_string_ = json_string_[1:-1]

    # Replace any problematic encoding in your string
    # Example: Replace escaped unicode characters
    json_string_ = json_string_.encode().decode('unicode_escape')

    # Now, try to load it as a JSON object
    try:
        data = json.loads(json_string_)
        print("JSON loaded successfully")

        return json_string_ , data
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)


    

def parse_listing_data(json_string_):

    # Convert the JSON string to a Python dictionary
    uuu , data = parse_data_(json_string_)
    #data = json.loads(data_)

    # Extract the required fields
    listing = data['listing']
    listing_id = listing ["id"]
    listing_name = listing ["name"]
   
    latitude = listing['coordinate']['latitude']
    longitude = listing['coordinate']['longitude']
    pdpUrlType = listing ["pdpUrlType"]
    roomTypeCategory = listing ["roomTypeCategory"]
    room_rating = listing['avgRatingLocalized']
    pictures = listing['contextualPictures']
    #listofpicture = [pictures[0]['picture'], pictures[1]['picture'], pictures[2]['picture'], pictures[3]['picture'], pictures[4]['picture'], pictures[5]['picture']]
 

    pricequote = data['pricingQuote']

    pricenight = pricequote['structuredStayDisplayPrice']['primaryLine']#['price']
    totalprice = pricequote['structuredStayDisplayPrice']['secondaryLine']#['price']
    return {
        "ID": listing_id,
        "Name": listing_name,
       
        "latitude": latitude,
        "longitude": longitude,
        "PDP_URL_Type": pdpUrlType,
        "Room_Type-Category": roomTypeCategory,    
        "Room_Rating": room_rating,
        "Price_per_night" : pricenight,
        "total_price": totalprice,
        "listofpicture": pictures

    }

def order_html(html_name):
    # "1.html"
    # Path to the HTML file saved by Scrapy
    current_directory = os.getcwd()
    print(html_name)
    file_path =  os.path.join(current_directory, 'data', html_name)


    # Extract and parse the JSON data
    json_string = extract_json_from_html(file_path)
    #listing_data = parse_listing_data(json_string)
    all_listing_data = []

    #print(listing_data)

    for i in range(  0, 9 ): #
        try:
            # Parse each JSON string
            listing_data = parse_listing_data(json_string[i])
            all_listing_data.append(listing_data)
            #print(json_string[i])
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in one of the instances: {e}")

    # Print or process all_listing_data
    print(all_listing_data)

    return all_listing_data

#
def save_json_to_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main():
    #1 run the scraper scrapy crawl fullpage
    process = CrawlerProcess(settings={
        'BOT_NAME' : 'Newscraping',
        'SPIDER_MODULES' : ['spiders'],
        'NEWSPIDER_MODULE' : 'spiders',
        'ROBOTSTXT_OBEY' : False
    })

    process.crawl(Newscraping)
    process.start()
    #2 orderdata
    #3 loaddata
    current_directory = os.getcwd()
    output_directory = os.path.join(current_directory, 'output')
    print(output_directory)

    # Create output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for i in range(1,4 ):
        file_name = f"{i}.html"
        json_data = order_html(file_name)
        print(i)

        # Save each listing data to a separate JSON file
        for index, data in enumerate(json_data):
            output_file = os.path.join(output_directory, f'listing_{i}_{index}.json')
            print(output_file)
            save_json_to_file(data, output_file)
            print(i)
            print(index)
            print(data)
            print(output_directory)

if __name__ == "__main__":
    main()