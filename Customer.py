import uuid
# Represents the customer of the car insurance company
class Customer:
    def __init__(self, name, address):
        self.ID= str(uuid.uuid1())
        self.name = name
        self.address = address
        self.cars = [] # List of cars
        self.claims=[] #list of claims

    def addCar(self,model,plate,power,year):
        c=Car(model,plate,power,year)
        self.cars.append(c.serialize()) #serialize it to show the content when appending
        return self.cars

    def addClaim (self, date, claim_amount,inc_descript):
        cl = Claims(date, claim_amount,inc_descript)
        self.claims.append(cl)
        return cl.clID

    # convert object o JSON
    def serialize(self):
        return {
            'id': self.ID, 
            'name': self.name, 
            'address': self.address,
            'cars': self.cars,
            'claims': [x.serialize() for x in self.claims]
        }

class Car :
    def __init__(self, model_name, number_plate, motor_power, year):
        self.name = model_name
        self.number_plate = number_plate
        self.motor_power = motor_power
        self.year = year

    def serialize(self):
        return {
            'model': self.name,
            'plate-nb': self.number_plate,
            'power': self.motor_power,
            'year': self.year
        }

class Claims:
    def __init__(self, date, claim_amount,inc_descript):
        self.clID = str(uuid.uuid1())
        self.date = date
        self.claim_amount=claim_amount
        self.inc_descript=inc_descript
        self.appr_amount = 0
        self.status='default'

    def changeStat(self,ap_am):
        try:
            self.appr_amount = int(ap_am)
            if self.appr_amount == 0:
                self.status = 'REJECTED'
                return 'ok'
            elif self.appr_amount < int(self.claim_amount) and self.appr_amount > 0:
                self.status = 'PARTIALLY COVERED'
                return 'ok'
            elif self.appr_amount >= int(self.claim_amount):
                self.status = 'FULLY COVERED'
                return 'ok'
        except ValueError: #try expect block incase user enters not a number
            return None

    # convert object o JSON
    def serialize(self):
        return {
            'id': self.clID,
            'date': self.date,
            'claim amount': self.claim_amount,
            'approved amount': self.appr_amount,
            'description': self.inc_descript,
            'status': self.status
        }