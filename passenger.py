
import travel

class Passengers:
    def __init__(self, name, id, debt):
        # Initialize passenger attributes with appropriate data types
        self.name = str(name)
        self.id = str(id)
        self.debt = float(debt)

    # Check if the given ID and name match the passenger's attributes
    # This is used to verify if a customer already exists
    def Check_if_it_exists(self, id, name):
        return self.id.__eq__(id) and self.name.__eq__(name)

    # Process a payment to reduce the passenger's debt by the specified amount
    def Payment(self, sum):
        self.debt -= sum

    # Check if the current passenger is a manager based on predefined ID and name
    def isManager(self):
        return self.id.__eq__("1") and self.name.__eq__("manager")

    # Return the passenger's information as a dictionary
    def to_dict(self):
        return {
            "name": self.name,
            "id": self.id,
            "debt": self.debt
        }
