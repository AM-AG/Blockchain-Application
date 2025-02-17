import json
import hashlib
from time import *
from  flask import *
import requests
from urllib.parse import urlparse
from uuid import uuid4
from argparse import ArgumentParser
from flask_ngrok import *
from pyngrok import ngrok

class Blockchain:
  #--------------------------------------- Constructor
  def __init__(self):                 
    self.transactions_courrentes= []
    self.chain = []
    self.nodes=set()
    self.acknowledgments = []
    self.verified= []
    self.new_block(previous_hash='1',proof=100)     # Create the first bloc in the blockchain

  #--------------------------------------- Chain Validation
  def valid_chain(self,chain):
    last_block = chain[0]
    index = 1
    while index <len(chain):
      block = chain[index]
      print(last_block,"-----",block)
      last_block_hash = self.hash(last_block)
      if block["previous_hash"] != last_block_hash:
        return False
      if not self.valid_proof(last_block["proof"],block["proof"],last_block_hash):
        return False
      last_block = block
      index +=1

    return True
  #--------------------------------------- Register a node
  def registre_node(self,address):
    """
         Create a new node that will be added to the other existant nodes
    """
    parsed_url = urlparse(address)
    if parsed_url.netloc:
        self.nodes.add(parsed_url.netloc)
    elif parsed_url.path:
        self.nodes.add(parsed_url.path)
    else:
        raise ValueError('Invalid URL')
    
#----------------------------------------- Create a new Block
  def new_block(self,proof,previous_hash):
    """ Create a new Block in the blockchain                       
        proof in parameter is gived by the proof of work algorithm
        The function will allow us to create a new Block 
    """               
    time_now = time.time()
    block = {
        "index":len(self.chain)+1,
        "timestamp":time_now,
        "transactions":self.transactions_courrentes,
        "proof":proof,
        "previous_hash":previous_hash or self.hash(self.chain[-1]),
    }
    self.transactions_courrentes = []
    self.acknowledgments = []
    self.chain.append(block)
    return block
  
  #--------------------------------------- Create a new transaction
  def new_transaction(self,sender,stocksymbol,recipient,amount):
    """
           Register a new transaction which have in parameters all informations that should be registered

    """
    self.transactions_courrentes.append({"sender":sender,
                                         "stocksymbol":stocksymbol,
                                         "recipient":recipient,
                                         "amount":amount,})
    return self.last_block["index"]-1

  #--------------------------------------- Return the last Block
  @property
  def last_block(self):
    return self.chain[-1]

  #--------------------------------------- The hash function
  @staticmethod
  def hash(block):
    """
           The hash function of the Block using the SHA256 (256 bits)
    """
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()
  
  #--------------------------------------- The proof of work algorithm
  def proof_of_work(self,last_block):

    last_proof = last_block["proof"]
    last_hash  = self.hash(last_block)
    proof =0
    while self.valid_proof(last_proof,proof,last_hash) is False:
      proof +=1
    return proof
  
  #--------------------------------------- The proof validation function 
  @staticmethod
  def valid_proof(last_proof,proof,last_hash):
    guess = f'{last_proof}{proof}{last_hash}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:5] == "00000"



