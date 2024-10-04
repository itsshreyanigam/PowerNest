from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
import mysql.connector
import hashlib
import json
from time import time

app = Flask(__name__)

# Enable CORS for all routes and all origins
CORS(app)

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Shreya@2003",
    database="project"
)
@app.route('/')
def root():
    return redirect(url_for('homepage'))


# Route to render index.html
@app.route('/homepage', methods=['GET'])
def homepage():
    return render_template('index.html')

@app.route('/seller')
def seller():
    return render_template('seller.html')

@app.route('/buyer')
def buyer():
    return render_template('buyer.html')


# Error handler for invalid URLs
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "URL not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
# Blockchain structure
class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_data = []
        self.new_block(previous_hash='1', proof=100)  # Create genesis block

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'data': self.current_data,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_data = []
        self.chain.append(block)
        return block

    def new_data(self, data):
        self.current_data.append(data)
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

blockchain = Blockchain()

# Route to accept form data and create a block for contributions
@app.route('/contribute', methods=['POST'])
def contribute():
    data = request.json

    # Insert data into MySQL
    cursor = db.cursor()
    cursor.execute("INSERT INTO contributions (firstName, lastName, email, phone, address, energyType, energyUnits, frequency) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                   (data['firstName'], data['lastName'], data['email'], data['phone'], data['address'], data['energyType'], data['energyUnits'], data['frequency']))
    db.commit()

    # Create a new block with this data
    blockchain.new_data(data)
    block = blockchain.new_block(proof=123)

    response = {
        'message': 'New block has been added to the blockchain!',
        'block': block
    }
    return jsonify(response), 200

# Route to accept form data and create a block for energy purchases
@app.route('/buy', methods=['POST'])
def buy_energy():
    try:
        # Parse the JSON data from the request
        data = request.get_json()

        # Extract relevant fields from the JSON data
        name = data.get('name')
        email = data.get('email')
        address = data.get('address')
        city = data.get('city')
        state = data.get('state')
        zipcode = data.get('zipcode')
        energy_type = data.get('type')
        amount = data.get('amount')
        total = data.get('total')

        # Logic to handle purchase (e.g., saving to a database, processing order)
        # For now, we simply print the order to the console for debugging purposes
        print(f"Received order from {name}:")
        print(f"{amount} kWh of {energy_type} energy for a total of ₹{total}")
        print(f"Shipping to: {address}, {city}, {state}, {zipcode}")
        print(f"Contact Email: {email}")

        # Simulate order processing and respond with a success message
        return jsonify({"message": f"Order for {amount} kWh of {energy_type} placed successfully!"})

    except Exception as e:
        # Handle any errors that may occur
        return jsonify({"error": str(e)}), 400
if __name__ == '__main__':
    app.run(port=5000, debug=True)
@app.route('/homepage')
def homepage():
    return render_template('index.html')
    