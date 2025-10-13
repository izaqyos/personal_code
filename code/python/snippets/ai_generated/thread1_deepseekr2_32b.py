import threading
from queue import Queue
import random
import time

def producer(queue):
    for _ in range(100):  # Generate 100 numbers
        number = random.randint(1, 100)
        queue.put(number)
        time.sleep(0.1)  # Optional: to simulate slower production
    queue.put(None)  # Signal the consumer to stop

def consumer(queue):
    while True:
        number = queue.get()
        if number is None:
            break  # Exit loop when sentinel is received
        if number % 2 == 0:
            print(f"Even number: {number}")

# Create the queue
q = Queue()

# Start producer and consumer threads
producer_thread = threading.Thread(target=producer, args=(q,))
consumer_thread = threading.Thread(target=consumer, args=(q,))

producer_thread.daemon = True
consumer_thread.daemon = True

producer_thread.start()
consumer_thread.start()

# Wait for both threads to finish
producer_thread.join()
consumer_thread.join()
