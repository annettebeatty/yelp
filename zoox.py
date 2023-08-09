# 
# Delta = (miles * mileage) 
# United = (miles * mileage) + premium (miles * .10)
# Southwest = (miles * mileage)
# LuigiAir = whichever is higher = $100 or 2 * mileage
# 
# 
#  Brute force.  Next iteration will use classes to calculate per airline
# 
# 
#

test_input = [
   "United 150.0 Premium",
   "Delta 60.0 Business",
   "Southwest 1000.0 Economy",
   "LuigiAir 50.0 Business"
]

premium_seat = 25
business_seat = 50


def main():
	air = []

	# change the input to array of stuff
	for x in range(len(test_input)):
		airline, mileage, seating = test_input[x].split(' ')
		new_air = airline, float(mileage), seating
		air.append(new_air)

#	print("new array", air)

	# do the calculations

#	print(len(air))
#	print(air[0])

	for x in range(len(air)):
		cost = 0
		airline = air[x][0]
		mileage = air[x][1]
		seating = air[x][2]

		# Figure out operating costs
		if airline == "United":
			cost = float(mileage) * .75
			if seating == "Premium":
				cost = cost + (float(mileage) * .10)
		elif airline == "Delta":
			cost = float(mileage) * .5
		elif airline == "Southwest":
			cost = float(mileage)
			
		# Figure out upgrade cost
		if seating == "Premium":
			cost += 25
		elif seating == "Business":
			cost += 50 + (.25 * mileage)

		# Weird Luigi Air
		if airline == "LuigiAir":
			higher = 2 * cost
			if cost < higher:
				cost = higher

		#print(airline, "cost", cost)
		print(cost)
		
if __name__ == "__main__":
    main()

