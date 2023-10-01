import hashlib
import json
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

def calculate_hash(index, previous_hash, timestamp, data):
    value = str(index) + str(previous_hash) + str(timestamp) + json.dumps(data)
    return hashlib.sha256(value.encode('utf-8')).hexdigest()

def create_genesis_block():
    return Block(0, "0", int(time.time()), [], "0000000000000000000000000000000000000000000000000000000000000000")

def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = int(time.time())
    hash = calculate_hash(index, previous_block.hash, timestamp, data)
    return Block(index, previous_block.hash, timestamp, data, hash)

# Initialize blockchain with a genesis block
blockchain = [create_genesis_block()]
current_block = blockchain[-1]

# Example data for lost and found system
lost_item_data = {
    "item_name": "Phone",
    "description": "iPhone X",
    "owner_name": "Alice",
    "contact_info": "123-456-7890"
}

# Add a lost item to the blockchain
current_block = create_new_block(current_block, lost_item_data)
blockchain.append(current_block)

# Print the blockchain
for block in blockchain:
    print(f"Index: {block.index}")
    print(f"Previous Hash: {block.previous_hash}")
    print(f"Timestamp: {block.timestamp}")
    print(f"Data: {json.dumps(block.data)}")
    print(f"Hash: {block.hash}\n")
