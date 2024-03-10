import scrapy
import os
import json
from datetime import datetime, timedelta
import numpy as np





def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    


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




 
class Newscraping(scrapy.Spider):
    name = 'Newscraping'
    counter = 0

    def init___():
        current_directory = os.getcwd()
        output_directory = os.path.join(current_directory,"airbnbscrapy")
        input_data_directory = os.path.join(output_directory, 'inputdata')

        
        # Path to the JSON file
        json_info_path = os.path.join(current_directory,'info.json')

        coordinate_json_path = os.path.join(current_directory,'coordinate.json')

        lko= read_json(json_info_path)



        ###### coordinates creation
        coord_data = read_json(coordinate_json_path)

        c_a1 = coord_data['latitude'][0]
        c_b1 = coord_data['latitude'][1]
        lat_diff = c_a1 - c_b1

        c_a2 = coord_data['longitude'][0]
        c_b2 = coord_data['longitude'][1]    
        long_diff = c_a2 - c_b2

 
        urls = []
        counter__ = 1

        #urls = 'https://www.airbnb.com/s/nex-mexico/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-03-01&monthly_length=3&monthly_end_date=2024-06-01&price_filter_input_type=0&channel=EXPLORE&date_picker_type=calendar&checkin=2024-03-13&checkout=2024-03-16&source=structured_search_input_header&search_type=user_map_move&query=Tirana%2C%20Albania&price_filter_num_nights=3&zoom_level=15.944565424945226&place_id=ChIJ28X6cAQxUBMRIDdlEK-SAAQ&ne_lat=41.319768724456715&ne_lng=19.81439458236403&sw_lat=41.31811903861763&sw_lng=19.81235800502456&zoom=15.944565424945226&search_by_map=true'
        
        start_date = '2024-03-15'
        end_date = '2024-06-01'
      

        for l in range (0,  np.int32(coord_data['latitude_movement'])):
            for p in range (0, np.int32(coord_data['longitude_movement'])):

                lat_a = coord_data['latitude'][0] + (lat_diff * l)
                lat_b = coord_data['latitude'][1] + (lat_diff * l)

                long_a = coord_data['longitude'][0] + (long_diff *p)
                long_b = coord_data['longitude'][1] + (long_diff *p)   


                print(lat_a, lat_b, long_a, long_b)

                url_sing = 'https://www.airbnb.com/s/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-03-15&monthly_length=3&monthly_end_date=2024-06-01&price_filter_input_type=0&channel=EXPLORE&date_picker_type=calendar&checkin=2024-03-13&checkout=2024-03-16&source=structured_search_input_header&search_type=user_map_move&query=Tirana%2C+Albania&price_filter_num_nights=3&zoom_level=15.944565424945226&place_id=ChIJ28X6cAQxUBMRIDdlEK-SAAQ&ne_lat='  + str(lat_a) + '&ne_lng='  + str(long_a) + '&sw_lat=' + str(lat_b) + '&sw_lng='  + str(long_b) + '&zoom=15.944565424945226&search_by_map=true'
                print(url_sing)
                urls.append(url_sing)

        
        return urls 
    





    #start_urls =  init___()
    #print(start_urls)


    
   
    #start_urls = "https://www.airbnb.com/s/nex-mexico/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-03-01&monthly_length=3&monthly_end_date=2024-06-01&price_filter_input_type=0&channel=EXPLORE&date_picker_type=calendar&checkin=2024-03-13&checkout=2024-03-16&source=structured_search_input_header&search_type=user_map_move&query=Tirana%2C%20Albania&price_filter_num_nights=3&zoom_level=15.944565424945226&place_id=ChIJ28X6cAQxUBMRIDdlEK-SAAQ&ne_lat=41.319768724456715&ne_lng=19.81439458236403&sw_lat=41.31811903861763&sw_lng=19.81235800502456&zoom=15.944565424945226&search_by_map=true"
    
    start_urls = init___()
    
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'

    def start_requests(self):
        for url in self.start_urls:
            print(url)
            yield scrapy.Request(url, headers={'User-Agent': self.user_agent})


  #  def start_requests(self):
      
  #          yield scrapy.Request(self.start_urls, headers={'User-Agent': self.user_agent})


    def parse(self, response):
        current_directory = os.getcwd()
        self.counter += 1

         # Extract query parameters from URL
        # parsed_url = urlparse(response.url)
        # query_params = parse_qs(parsed_url.query)

        # # Extract additional data from URL
        # checkin = query_params.get('checkin', [None])[0]
        # checkout = query_params.get('checkout', [None])[0]
        # adults = query_params.get('adults', [None])[0]
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Extract data using CSS selectors or any other method
        data = {
            'url': response.url,
            'content': response.text,
            'current_date': current_date,
            
        }

        data_html = response.body
        # Define a filename based on the URL or another unique identifier
        filename = f"{self.counter}.html"

        # Define the directory where you want to save the file
        directory = os.path.join(current_directory,  'data')
        #print(directory)
        
        # Create directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Combine the directory and filename
        file_path = os.path.join(directory, filename)

        # Write the extracted data to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(data_html))
            
            self.log(f'Saved file {filename}')




print("newscraping")