import queue
import threading
import time
import random

class Road_streetQueue:
    def __init__(self, capacity):
        self.queue = queue.Queue(capacity)

    def protecter_01(self, item,n):
        self.queue.put(item)  # Blocks if queue is full
        print("Protecter_01" + str(n) + " allow: " + str(item) + " - queue: " + str(self.queue.queue))
    def protecter_02(self,item,n):
        self.queue.put(item) 
        print("Protecter_02" + str(n) + " allow: " + str(item) + " - queue: " + str(self.queue.queue))

    def Driver(self,n):
        item = self.queue.get()  # Blocks if queue is empty
        print("Driver " + str(n) + " run: " + str(item) + " - queue: " + str(self.queue.queue))
        return item

# Usage example:
def producer(pcq, n):
    while True:
        time.sleep(1)
        i = random.randint(1, 1000)
        pcq.produce(i, n)

def consumer(pcq, m):
    while True:
        time.sleep(1)
        pcq.consume(m)


# nhập vào số liệu n 
num_queue = int(input("Enter the number of queues: "))
pcq = ProducerConsumerQueue(num_queue)

t1 = threading.Thread(target=producer, args=(pcq,1))
t2 = threading.Thread(target=producer, args=(pcq,2))
t3 = threading.Thread(target=producer, args=(pcq,3))
t4 = threading.Thread(target=producer, args=(pcq,4))

t10 = threading.Thread(target=consumer, args=(pcq,1))
t11 = threading.Thread(target=consumer, args=(pcq,2))


t1.start()
t2.start()
t3.start()
t4.start()
t10.start()
t11.start()



t1.join()
t2.join()
t3.join()
t4.join()
t10.join()
t11.join()
