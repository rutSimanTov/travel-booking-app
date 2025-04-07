from passenger import Passengers
from travel import Travel
import json

travelList = []  # List to hold travel objects
passengersList = []  # List to hold passenger objects
TravelsDict = {}  # Dictionary to store travel destinations

# Define the JSON filename
filename = 'dataFile.json'

# Attempt to read data from the JSON file
try:
    with open(filename, 'r') as file:
        data = json.load(file)
        travelList = [Travel(travel['target'], travel['Date'], travel['price']) for travel in data['travelList']]
        passengersList = [Passengers(passenger['name'], passenger['id'], passenger['debt']) for passenger in
                          data['passengersList']]
        TravelsDict = data['TravelsDict']
except (IOError, json.JSONDecodeError) as e:
    print(f"Error reading the file: {e}")

userCurrent = None  # Variable to store the current user
manager = False  # Flag to check if the user is a manager
choice = None  # User's choice for the action they want to perform
choiceUserTrip = None  # The trip value for a user wanting to register for a specific destination
target = Travel(None, None, 0)  # Helper object of type Travel

name = input("Hi! Please enter your name: ")  # User's name input
id = input("Please enter your identity ID: ")  # User's ID input

# Check if the client already exists
for p in passengersList:
    if p.Check_if_it_exists(id, name):
        userCurrent = p
        break

# If the client does not exist, add them to the system
if userCurrent is None:
    userCurrent = Passengers(name, id, 0)
    passengersList.append(userCurrent)

# Check if the user is in manager mode
if userCurrent.isManager():
    manager = True
    print("Welcome to the manager panel!")

    # Accept the action number the manager wants to perform
    while choice not in (1, 2):
        choice = int(input("Press 1 to add a destination\nPress 2 to view trip data\n"))

    # If the choice is to add a trip
    if choice == 1:
        target.addtravel()
        flag = False

        # Check if a trip to the same destination already exists
        for i in travelList:
            if i.target == target.target:
                flag = True
                break

        # If a trip to that destination exists, prompt for a new destination
        while flag:
            print("Destination exists, please enter another destination.")
            target.addtravel()
            flag = any(i.target == target.target for i in travelList)

        # Add the destination to the travel array
        travelList.append(target)
        #TravelsDict[target.target] = target
        TravelsDict[target.target] = []

        print("The trip was successfully recorded.")
    else:
        # Print the trips that are available in the system
        for item in TravelsDict:
            for travel in travelList:
                if item == travel.target:
                    print("Trip: ")
                    travel.print_details()
                    print("\nPassenger IDs: ")
                    for i in TravelsDict[item]:
                        print(i + ",")
                    break

# In passenger mode
else:
    print(f"Hello, {userCurrent.name}!")

    # Choosing the action the passenger wants to perform
    while choice not in (1, 2, 3):
        choice = int(input(
            "Press 1 to register for a new trip\nPress 2 to pay for previous trips\nPress 3 to view your upcoming trips\n"))

    # If the user wants to join a trip
    if choice == 1:
        # Validate the user's selected trip and avoid duplicates
        while (choiceUserTrip is None or (choiceUserTrip not in TravelsDict) or userCurrent.id in TravelsDict[
            choiceUserTrip]):
            if choiceUserTrip is not None:
                if userCurrent.id in TravelsDict[choiceUserTrip]:
                    print("You are already registered for this trip. Please select a different trip.")
                elif choiceUserTrip not in TravelsDict:
                    print("Invalid input. Please enter a valid travel destination.")
            else:  # Prompt user to choose a trip
                print("Choose a trip.")

            # Displaying available trips
            for key in TravelsDict:
                print(f"To register for {key}, press {key}")
            choiceUserTrip = input("")

        # Check if the user is already in the trip and save the date and price for payment
        for item in travelList:
            if item.target == choiceUserTrip:
                DateTrip = item.Date
                priceTrip = item.price

        for item in travelList:
            if DateTrip == item.Date:
                if userCurrent.id in TravelsDict[item.target]:
                    print("You are already registered for the trip on the selected date.")
                    exit()

        # Add the passenger to the travel list
        TravelsDict[choiceUserTrip].append(userCurrent.id)

        # Ask if the user wants to pay now
        pay = input("Do you want to pay now? (y/n) ")
        if pay.lower() == "y":
            print("This trip is paid for. You have successfully registered for the trip.")
        else:
            print("Payment for this trip is added to your debt.")
            userCurrent.debt += priceTrip

    # If the user wants to pay off their debts, if any
    elif choice == 2:
        if userCurrent.debt == 0:
            print("You have no debts.")
        else:
            num = int(
                input(f"You have a debt of {userCurrent.debt} shekels. How much of the debt do you want to cover? "))
            while num > userCurrent.debt:
                print("You requested too much. Please enter an amount again.")
                num = int(input(
                    f"You have a debt of {userCurrent.debt} shekels. How much of the debt do you want to cover? "))

            # Call the function that updates the debt and print a suitable message
            userCurrent.Payment(num)
            print(f"The remaining debt is {userCurrent.debt}. Thank you!")

    else:
        # If the passenger wants to see their list of trips
        for key, value in TravelsDict.items():
            if userCurrent.id in value:
                print(key)
        print("\nHave a great day!")

# Writing to the JSON file
try:
    with open(filename, 'w') as file:
        json.dump({
            "travelList": [travel.to_dict() for travel in travelList],
            "passengersList": [passenger.to_dict() for passenger in passengersList],
            "TravelsDict": TravelsDict
        }, file, indent=4)
except Exception as e:
    print(f"Error writing to the file: {e}")