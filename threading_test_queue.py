import threading
from queue import Queue
import time

print_lock = threading.Lock()

def example_job(task):
    time.sleep(0.5)

    with print_lock:
        print(threading.current_thread().name, task)

def worker():
    while True:
        task = q.get()
        example_job(task)
        q.task_done()

# driver code
if __name__ == '__main__':
    q = Queue()

    for task in range(10):
        q.put(task)

    for _ in range(10):
        t = threading.Thread(target = worker, daemon = True)
        t.start()

    start = time.time()

    # wait until sub threads are done before ending the main thread
    q.join()

    print("entire job took: ", time.time() - start)
