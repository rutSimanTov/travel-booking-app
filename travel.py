class Travel:
    def __init__(self, target, date, price):
        self.target = str(target)  # Store the travel destination
        self.Date = date  # Store the date of travel
        self.price = float(price)  # Store the price of the travel

    def addtravel(self):
        self.target = str(input("Enter the target: "))  # Get the travel destination from user input
        self.Date = input("Enter date of travel: ")  # Get the travel date from user input
        self.price = float(input("Enter price of travel: "))  # Get the travel price from user input

    # Print the details of the travel
    def print_details(self):
        print(f"Destination: {self.target}, Date: {self.Date}, Price: {self.price}")

    # Convert the travel object to a dictionary for JSON serialization
    def to_dict(self):
        return {
            "target": self.target,
            "Date": self.Date,
            "price": self.price
        }