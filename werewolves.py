import time
import random
import threading
from threading import Thread
def simple_worker():
    time.sleep(random.random() * 5)
    value = random.randint(0, 99)
    print('My value:'+str(value))

threads = [Thread(target=simple_worker) for _ in range(5)]
[t.start() for t in threads]
[t.join() for t in threads]
print([t for t in threads])
