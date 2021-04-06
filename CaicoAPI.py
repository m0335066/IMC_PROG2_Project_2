from flask import Flask, request, jsonify
from InsuranceCompany import *
from Customer import *
from Agent import *

app = Flask(__name__)

# Root object for the insurance company
company = InsuranceCompany ("Be-Safe Insurance Company")

#Add a new customer (parameters: name, address).
@app.route("/customer", methods=["POST"])
def addCustomer():
    # parameters are passed in the body of the request
    cid = company.addCustomer(request.args.get('name'), request.args.get('address'))
    return jsonify(f"Added a new customer with ID {cid}")

#Add a new agent (parameters: name, address)
@app.route("/agent", methods=["POST"])
def addAgent():
    # parameters are passed in the body of the request
    cid = company.addAgent(request.args.get('name'), request.args.get('address'))
    return jsonify(f"Added a new agent with ID {cid}")

#Return the details of a customer of the given customer_id.
@app.route("/customer/<customer_id>", methods=["GET"])
def customerInfo(customer_id):
    c = company.getCustomerById(customer_id)
    if(c!=None):
        return jsonify(c.serialize())
    return jsonify(
            success = False,
            message = "Customer not found")

#Return the details of a agent of the given agent_id.
@app.route("/agent/<agent_id>", methods=["GET"])
def agentInfo(agent_id):
    c = company.getAgentById(agent_id)
    if(c!=None):
        return jsonify(c.serialize())
    return jsonify(
            success = False,
            message = "Agent not found")

#Assign a customer to an agent
@app.route("/agent/<agent_id>/<customer_id>", methods=["POST"])
def assignCustomer(customer_id,agent_id):
    ag = company.getAgentById(agent_id)
    cust = company.getCustomerById(customer_id)
    if(ag!=None and cust!=None):
        ag.addCustomer(cust)
        return jsonify("Customer successfully added")
    return jsonify(
            success = False,
            message = "Customer or agent not found")

#Add a new car (parameters: model, numberplate).
@app.route("/customer/<customer_id>/car", methods=["POST"])
def addCar(customer_id):
    c = company.getCustomerById(customer_id)
    if(c!=None):
        car = Car(request.args.get('model'), request.args.get('number_plate'), request.args.get('motor_power'))
        c.addCar (car)
    return jsonify(
            success = c!=None,
            message = "Customer not found")

#Delete customer
@app.route("/customer/<customer_id>", methods=["DELETE"])
def deleteCustomer(customer_id):
    result = company.deleteCustomer(customer_id)
    if(result):
        message = f"Customer with id{customer_id} was deleted"
    else:
        message = "Customer not found"
    return jsonify(
            success = result,
            message = message)

#delete agent
@app.route("/agent/<agent_id>", methods=["DELETE"])
def deleteAgent(agent_id):
    result = company.deleteAgent(agent_id)
    if(result!=None):
        message = f"Agent with id{agent_id} was deleted"
    else:
        message = "Agent not found"
    return jsonify(
            success = result,
            message = message)

#Return list of customers
@app.route("/customers", methods=["GET"])
def allCustomers():
    return jsonify(customers=[h.serialize() for h in company.getCustomers()])

#Return list of agents
@app.route("/agents", methods=["GET"])
def allAgents():
    return jsonify(agents=[k.serialize() for k in company.getAgents()])

#Return list of claims
@app.route("/claims", methods=["GET"])
def allClaims():
    #return [k.serialize() for k in company.getClaims()]
    return jsonify(claims=[k.serialize() for k in company.getClaims()])

#change claim status by changing approved amount
@app.route("/claims/<claim_id>/status", methods=["PUT"])
def changeStat(claim_id):
    c = company.getClaimById(claim_id)
    if (c != None): #checks if claim exists
        ap_am = request.args.get('appr_amount')
        var = c.changeStat(ap_am)
        if (var != None): #check if userinput is correct
            return jsonify(c.serialize())
        else:
            return 'sorry deepak... invalid entry for approved amount, try again'
    return 'sorry deepak... claim id not found'

#get a list of all payments
@app.route("/payments", methods=["GET"])
def allPayments():
    return jsonify(Caico_payments=[k.serialize() for k in company.getPayments()])

#get all payments received
@app.route("/payments/in", methods=["POST"])
def addPayIn():
    # parameters are passed in the body of the request
    p = company.addPayin(request.args.get('date'), request.args.get('id'), request.args.get('amount'))
    if p!= None:
        return jsonify(p)
    return 'sorry customer not found'

#get all payments sent
@app.route("/payments/out", methods=["POST"])
def addPayOut():
    # parameters are passed in the body of the request
    p = company.addPayout(request.args.get('date'), request.args.get('id'), request.args.get('amount'))
    if p!= None:
        return jsonify(p)
    return 'sorry agent not found'

#Return the details of a claim of the given claim_id.
@app.route("/claims/<claim_id>", methods=["GET"])
def claimInfo(claim_id):
    c = company.getClaimById(claim_id)
    if(c!=None):
        #return 'this works'
        return c.serialize()
    return jsonify(
            success = False,
            message = "Claim not found")

#File a claim for a customer based on customer id
@app.route("/claims/<customer_id>/file", methods=["POST"])
def addClaim(customer_id):
    c = company.getCustomerById(customer_id)
    if(c!=None):
        cid = c.addClaim (request.args.get('date'), request.args.get('claim amount'), request.args.get('inc_descript'))
        #return jsonify(f"Added a new claim with ID {cid}")
        return jsonify([c.serialize() for c in c.claims])
    return jsonify(
            success =  False,
            message = "Customer not found")

#return claim statistics
@app.route("/stats/claims", methods=["GET"])
def claimStats():
    return jsonify(Claims_by_agent=[k for k in company.getStatsforClaims()])

#return revenue statistics
@app.route("/stats/revenues", methods=["GET"])
def RevStats():
    return jsonify(Revenues_by_agent=[k.serialize() for k in company.getStatsforRevenue()])

#return agent scores
@app.route("/stats/agents", methods=["GET"])
def AgentScores():
    #return jsonify(agent_scores=[k for k in company.getAgentscores()])
    return jsonify(agent_scores=company.getAgentscores())

#ID1_=company.addCustomer("Dude","Vienna")
#ID2_=company.addCustomer("Johnny","Munich")
#ID3_=company.addAgent("Sue","Monacco")
#ID4_=company.addAgent("Alex","Paris")
#cust1=company.getCustomerById(ID1_)
#cust1.addCar("audi A5","W-12345","245HP","2018")
#cust1.addCar("VW polo","W-98765","180HP","2019")
#cust1.addClaim("DD-MM-YYYY", "1000" , "car accident on 123 fake street")
#cust1.addClaim("DD-MM-YYYY", "900" , "hit a deer on the road")
#cust2=company.getCustomerById(ID2_)
#cust2.addClaim("DD-MM-YYYY", "500" , "hit a dog on the road")
#ag1=company.getAgentById(ID3_)
#ag2=company.getAgentById(ID4_)
#ag1.addCustomer(cust1)
#ag1.addCustomer(cust2)
#company.addPayout ('DD-MM-YYYY', ID4_, '123')
#company.addPayout ('DD-MM-YYYY', ID4_, '997')
#company.addPayout ('DD-MM-YYYY', ID3_, '101')
#print(ag2.customers)
#company.deleteAgent(ID4_)


###DO NOT CHANGE CODE BELOW THIS LINE ##############################
@app.route("/")
def index():
    return jsonify(
            success = True,
            message = "Your server is running! Welcome to the Insurance Company API.")

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE"
    return response

if __name__ == "__main__":
    app.run(debug=True, port=8888)
