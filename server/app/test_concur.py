import os
from multiprocessing import Process
import random 

# Number of concurrent requests to send
num_requests = 1000

# Define the curl command
curl_command = 'curl -X POST http://localhost:5000/user/new_transaction -H "Content-Type: application/json" -d \'{"buyer_id": {}, "seller_id": {}, "prod_id": {}, "selling_price": 100, "quantity": 1}\' '

# Function to send curl commands
def send_request(l):

    i = random.randint(1, 6)
    j = random.randint(1, 6)
    k = random.randint(1, 6)
    os.system(f'curl -X POST http://localhost:5000/user/new_transaction -H "Content-Type: application/json" -d \'{{"buyer_id": {i}, "seller_id": {j}, "prod_id": {k}, "selling_price": {10*i}, "quantity": 1}}\'')
    
processes = []
for l in range(1, num_requests+1):
    process = Process(target=send_request(l))
    processes.append(process)
    process.start()

# Wait for all processes to finish
for process in processes:
    process.join()
