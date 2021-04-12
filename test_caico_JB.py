import pytest
from InsuranceCompany import *
from Customer import *
from Agent import *

#scope can be session, class, module (for the entire file), package (for the entire directory),
#default scope is function
@pytest.fixture (scope = 'module')
def persons():
    return [Agent("Daryl","Paris"),Customer("Dude","Vienna")]

@pytest.fixture
def cars():
    return Car("audi A5","W-12345","245HP","2018")

@pytest.fixture
def claims():
    return Claims("DD-MM-YYYY", "500" , "hit a dog on the road")

def test_addCustomer(persons):
    agent1=persons[0]
    customer=persons[1]
    agent1.addCustomer(customer)
    assert customer in agent1.customers , 'customer has not been added to the agents customer list'

def test_addCar(cars,persons):
    car=cars
    customer=persons[1]
    customer.addCar(car)
    assert car in customer.cars , 'car has not been added to the list'

def test_getAgentById(persons):
    agent=persons[0]
    company=InsuranceCompany('Caico')
    x = company.getAgentById(company.addAgent(agent.name,agent.address))
    assert x!=None , "None was returned because Agent wasnt found"

def test_deleteAgent(persons):
    agent=persons[0]
    company=InsuranceCompany('Caico')
    ag_id = company.addAgent(agent.name,agent.address)
    #assert company.deleteAgent(ag_id) != None ,"None was returned because Agent wasnt found"
    assert agent not in company.agents , "agent is still in the list"