import threading
import random
from queue import Queue
import time

def generate_numbers(queue):
    while True:
        number = random.randint(1, 100)
        print(f"Generated: {number}")
        queue.put(number)
        time.sleep(0.1)

def print_even_numbers(queue):
    while True:
        number = queue.get()
        if number % 2 == 0:
            print(f"Even number detected: {number}")

queue = Queue()

thread1 = threading.Thread(target=generate_numbers, args=(queue,))
thread2 = threading.Thread(target=print_even_numbers, args=(queue,))

thread1.start()
thread2.start()

# Keep the main thread alive to prevent immediate exit
while True:
    time.sleep(1)
