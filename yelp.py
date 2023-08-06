# This is needed to perform REST API calls - requests
# Original - https://www.8bitavenue.com/yelp-fusion-api-python-example/
# 1. Modify to take command line arguments
#   -term -t <search term>
#   -loc -l <location>
#   -n <max number to return>
# 2. Modify to pull API_KEY from .env
# 3. Cosmetics - Add header, line up output, truncate name & address
# 4. Add reviews and business ID
# 5. Add the ability to print more information if given a business ID
# 6. Add business hours

import argparse
import requests
import json
from decouple import config

# Developer API key
API_KEY = config('API_KEY_YELP')

# Default values
DEFAULT_TERM = 'Smog Check'       # What you are searching for
DEFAULT_LOCATION = 'San Jose, CA' # Business location
SEARCH_LIMIT = 5                  # Maximum number of results to return

search_term = DEFAULT_TERM
search_location = DEFAULT_LOCATION
search_limit = SEARCH_LIMIT

argParser = argparse.ArgumentParser()
argParser.add_argument("--term", help="Search term")
argParser.add_argument("--loc", help="Location")
argParser.add_argument("--num", help="Number to return")
argParser.add_argument("--id", help="Business ID")
args = argParser.parse_args()

if args.term:
	search_term = args.term

if args.loc:
	search_location = args.loc

if args.num:
	search_limit = args.num

# Header should contain the API key
headers = {'Authorization': 'Bearer {}'.format(API_KEY)}

if args.id:
	# Give more info about the specific business
	yelp_id = args.id

	# Specific business end point
	url = 'https://api.yelp.com/v3/businesses/' + str(yelp_id)

	# Call the API
	response = requests.request('GET', url, headers=headers)

	# Interesting additional information
	# name, rating, review_count, display_address, display_phone, url, cross_streets, hours - array["hours"]["open"]["day"][0-6]["start"]["end"]

	# See what data we can get
	business_data = response.json()

	print(business_data["name"], "** Rating -", business_data["rating"], "  Reviews -", business_data["review_count"],"**")

	print(business_data["location"]["display_address"][0], 
		business_data["location"]["display_address"][1])

	if len(business_data["location"]["display_address"]) > 2:        # If record has second address line, print it out
		print(business_data["location"]["display_address"][2])

	print("Cross streets -",business_data["location"]["cross_streets"])
	
	print(business_data["display_phone"], "\n")

	# print(business_data["hours"][0]["open"][0]["start"])

	# hours of operations
	# create an matrix of days and hour.  Preset day of the week and "Closed" as default

	bhours = ["Monday", " Closed"], ["Tuesday", " Closed"], ["Wednesday", " Closed"], ["Thursday", " Closed"], ["Friday", " Closed"], ["Saturday", " Closed"], ["Sunday"," Closed"]

	# Business hours array - "day" indicates day of the week.  Does not have empty elements.
	# Want to set hours in the array element.  If array element doesn't exist, you want it to say "Closed"

	# For every element, we need to stuff it into the right spot in the matrix
	for hours in business_data["hours"][0]["open"]:
		i = hours["day"]   # Day of the week
		bhours[i][1] = " " + hours["start"] + "-" + hours["end"]
		#print(bhours[i][1])
 
	#print(bhours)

	print("Hours of operation:")
	
	#print(bhours[6][0], bhours[6][1])

	for x in range(len(bhours)):
		day = bhours[x][0]
		hours = bhours[x][1]
		#print(day, hours)
		print("{:10} {:10}".format(day, hours))

	#print(business_data["url"])

	#print(json.dumps(business_data, indent = 3))

else:
	# Busines search end point
	url = 'https://api.yelp.com/v3/businesses/search'

	# Search parameters
	url_params = {
		'term': search_term, 
		'location': search_location,
		'limit': search_limit
		}

	# Call the API
	response = requests.request('GET', url, headers=headers, params=url_params)

	# Print header
	print("{:30}  {:6}   {:6}  {:20}  {:10}  {:20}".format("Name","Rating","Reviews","Address","Phone         ","Business ID")) 


	# To get a better understanding of the structure of 
	# the returned JSON object refer to the documentation
	# For each business, print name, rating, location and phone

	for business in response.json()["businesses"]:
	    print("{:30}  {:6}   {:6}   {:20}  {:10}  {:20}".format(
		business["name"][:30], 
		business["rating"], 
		business["review_count"], 
		business["location"]["display_address"][0][:20], 
		business["display_phone"],
		business["id"]))

# Convert the JSON String
#business_data = response.json()

#print(json.dumps(business_data, indent = 3))
