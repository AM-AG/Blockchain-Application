from blockchain import *
import csv

#        |    templates:
#        |               - Registre Page
#        |               - Mining page
#        |               - Transaction page

app = Flask(__name__)

# Generate a unique adress for the node
node_identifier = str(uuid4()).replace('-', '')

# Let's create a blockchain object
blockchain = Blockchain()
def write_to_csv(data):
    file_exists = os.path.isfile('transactions.csv')
    with open('transactions.csv', mode='a', newline='') as file:
        fieldnames = ['ID','sender','stocksymbol','Destinataire', 'Quantity', 'action']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)
def read_from_csv():
    transactions = []
    with open('transactions.csv', mode='r',newline='') as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            transactions.append(line)
    return transactions

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/mine', methods=['GET'])
def mine():
    # Let's mine the last Block
    dernier_block = blockchain.last_block
    proof = blockchain.proof_of_work(dernier_block)

    # Reading the file and adding the new transaction in the new Block
    transact = read_from_csv()
    blockchain.new_transaction(transact[-1][1],
                               transact[-1][2],
                               transact[-1][3],
                               transact[-1][4])

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(dernier_block)
    block = blockchain.new_block(proof, previous_hash)
    response = {
        'message': "----New Block mined ----",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    if request.method=='POST':
        sender = request.form['tx_id'] 
        amount = request.form['amount'] 
        s = request.form['action'] 
        if s!=None: action="Buy"
        else: action ="Sell"
        recipient= "Amine"
        ticker = request.form['ticker']
        values = {"sender":sender,
                 "stocksymbol":ticker,
                 "Destinataire":recipient,
                 "Quantity":amount,
                 "action":action
                }

    # Create a new Transaction
        index = blockchain.new_transaction(values['sender'], values['stocksymbol'], values['Destinataire'], values['Quantity'])

        response = {"ID":index,
                    "sender":sender,
                    "stocksymbol":ticker,
                    "Destinataire":recipient,
                    "Quantity":amount,
                    "action":action}
        write_to_csv(response)

        return redirect(url_for('transaction'))
    else:
        return 'Method not allowed'

@app.route('/transactions')
def transaction():
    transactions = read_from_csv()
    return render_template('transaction.html', transactions=transactions)


@app.route("/block")
def affiche_block():
    return Blockchain.chain[-1]

#public_url =ngrok.connect()
#print(public_url)

if __name__ == '__main__':
     app.run(port=8080)                
    
    # ngrok config add-authtoken 2Qkh6y5n0vE133xirAZK2CBo3tJ_3ypFmpyz6UVz3AyoFsdmL
    # ngrok http http://localhost:8080 