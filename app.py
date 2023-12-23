import json
from flask import Flask,request,jsonify

#Creating a Flask web Application Instance
app = Flask(__name__)

#employees 
employees = [  
                {"id":1,"name":"Sachin Dubey"},
                {"id":2,"name":"Rohan Preet Sigh"},
                {"id":3,"name":"Neha Kakkar"}
            ]
#For the next id to start with 4
nextEmployeeId = 4

#Get method to get all the list of the employees
@app.route('/employees',methods=['GET'])
def get_employees():
    return jsonify(employees)


#Get the employee by id
@app.route('/employees/<int:id>',methods=['GET'])
def get_employees_id(id:int):
    employee_details = get_emp_id(id)
    if employee_details is None:
        return jsonify({"error":"Invalid Employee Properties"}),404
    return jsonify(employee_details),200

#helper function to get the data by id
def get_emp_id(id):
    return next((record for record in employees if record["id"] == id),None)

#POST method for inserting or adding the new data
@app.route('/employees', methods=['POST'])
def create_employee():
    global nextEmployeeId
    employee = json.loads(request.data)
    if not employee_is_valid(employee):
        return jsonify({ 'error': 'Invalid employee properties.' }), 400

    employee['id'] = nextEmployeeId
    nextEmployeeId += 1
    employees.append(employee)

    return jsonify({ 'location': f'/employees/{employee["id"]}' }),201

#helper function to check
def employee_is_valid(employee):
    for key in employee.keys():
        if key != 'name':
            return False
    else:
        return True


#PUT method to update the employees data
@app.route('/employees/<int:id>',methods=['PUT'])
def update_employees(id:int):
    employee = get_emp_id(id)
    if employee is None:
        return jsonify({"error":"Employee Does Not Exist."}),400
    update_employee = json.loads(request.data)
    if not employee_is_valid(update_employee):
        return jsonify({"error":"Invalid Employee properities"}),400
    employee.update(update_employee)
    return jsonify({"updated data":employee}),200


#DELETE method to delete the employee data by id
@app.route('/employees/<int:id>',methods=['DELETE'])
def delete_employee(id:int):
    global employees
    employee = get_emp_id(id)
    if employee is None:
        return jsonify({"error":"Employee Details Does not exists"}),400
    
    employees = [e for e in employees if e['id']!=employee['id']]
    return jsonify({"After Deleting the employee data":employees}),200


if __name__ == "__main__":
    app.run(port=8080)