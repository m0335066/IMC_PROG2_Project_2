import uuid
# Represents the insurance agent
class Agent:
    def __init__(self, name, address):
        self.ID= str(uuid.uuid1())
        self.name = name
        self.address = address
        self.customers=[]
        self.score=0 # agent score starts with 0 and gets added by 1 for each customer

    # convert object o JSON
    def serialize(self):
        return {
            'id': self.ID,
            'name': self.name, 
            'address': self.address,
            'customers': self.customers
        }

    def addCustomer (self, customer):
        self.customers.append(customer.serialize())
        self.score =self.score + 1
        return self.customers

class Payments:
    def __init__(self,date,id,amount):
        self.date = date
        self.id=id
        self.amount=amount

class PayIn(Payments):

    def serialize(self):
        return {
            'date': self.date,
            'customer_id': self.id,
            'amount received': self.amount
        }

class PayOut(Payments):

    def serialize(self):
        return {
            'date': self.date,
            'agent_id': self.id,
            'amount sent': self.amount
        }

