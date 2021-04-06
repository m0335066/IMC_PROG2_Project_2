from Customer import *
from Agent import *
import uuid

class InsuranceCompany:
    def __init__(self, name):
        self.name = name # Name of the Insurance company
        self.customers = [] # list of customers
        self.agents = []  # list of dealers
        self.allclaims=[]
        self.payments = [] #list of all payments sent and received
        self.cl_list = [] #list for claim stats
        self.rev_list=[] #list for all revenues

    def getCustomers (self):
        return list(self.customers)

    def getAgents(self):
        return list(self.agents)

    def getPayments(self):
        return list(self.payments)

    def getClaims(self):
        for c in self.customers:
            for cl in c.claims:
                self.allclaims.append(cl)
        return list(self.allclaims)

    def getStatsforClaims(self):
        for agent in self.agents:
            self.cl_list.append(agent.name)
            for cust in agent.customers:
                self.cl_list.append(cust['claims'])
        return self.cl_list

    def getStatsforRevenue(self):
        for entry in self.payments:
            if isinstance(entry,PayOut):
                self.rev_list.append(entry)
        return self.rev_list

    def getAgentscores(self):
        return sorted([(a.score,a.name) for a in self.agents],key=lambda c:c[0],reverse=True)

    def addPayout (self, date, id, amount):
        c = PayOut (date, id, amount)
        #check if ID exists in agents
        ag_id = self.getAgentById(id)
        if ag_id != None:
            self.payments.append(c)
            if int(c.amount) >= 100: #adds 3 points to an agent score if payment is higher 100
                ag_id.score = ag_id.score + 3
            return c.serialize()
        return None

    def addPayin (self, date, id, amount):
        c = PayIn (date, id, amount)
        #check if ID exists in customers
        if self.getCustomerById(id) != None:
            self.payments.append(c)
            return c.serialize()
        return None

    def addCustomer (self, name, address):
        c = Customer (name, address)
        self.customers.append(c)
        return c.ID

    def addAgent (self, name, address):
        c = Agent (name, address)
        self.agents.append(c)
        return c.ID

    def getCustomerById(self, id_):
        for d in self.customers:
            if(d.ID==id_):
                return d
        return None

    def getAgentById(self, id_):
        for d in self.agents:
            if(d.ID==id_):
                return d
        return None

    def getClaimById(self, id_):
        for claim in self.allclaims:
            if claim.clID==id_:
                return claim
        return None

    def deleteCustomer (self, customer_id):
        c = self.getCustomerById(customer_id)
        self.customers.remove(c)

    def deleteAgent (self, a_id):
        c = self.getAgentById(a_id) #searches if agent is in the list
        if (c!=None):
            if len(c.customers)!=0: #checks if customers are assigned to this agent
                temp = c.customers
                c.customers=[]
                self.agents.remove(c)
                for item in temp:
                    self.agents[0].customers.append(item)
                return 'ok'
            else:
                c.customers=[]
                self.agents.remove(c)
                return 'ok'
        return None

