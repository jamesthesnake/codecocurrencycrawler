
import argparse

from threading import Thread

import queue
import json
import time


def gather_data(data_name="data_1.json"):
    """sets the global variables for the program to be shared
           inputs:
		data_name(str): name of json_file to run through
    """
    global DATA_DAG
    global first_edges
    global comp_active_thread
    with open(data_name) as f:
        DATA_DAG = json.load(f)
    start = 0
    first_edges = queue.Queue()

    comp_active_thread = []

    for edges in DATA_DAG:
        try:
            start = DATA_DAG[edges]['start']
            for edge in list(DATA_DAG[edges]['edges'].items()):
                first_edges.put(edge)
        except Exception as e:
            if start:
                break
            else:
                print('not found yet')


def get_edges(edge, start_time_first):
    """Gets the edges
           inputs:
             edge(tuple of str and int): a tuple of the edge and how long to sleep
             start_time_first(time_Stamp): tracks how long the program has been running overall
	   Returns:
             edge (float):  a tuple of the edge and how long to sleep
    """
    start_time = time.time()
    time.sleep(edge[1])
    here_time = time.time()
    print(edge[0], here_time - start_time, here_time - start_time_first)
    return edge


class DownloadWorker(Thread):
    def __init__(self, edge, time):
        Thread.__init__(self)
        self.queue_worker = queue.Queue()
        self.queue_worker.put(edge)
        self.time = time

    def run(self):
        while not self.queue_worker.empty():
            if self.queue_worker.empty():
                break
            edge = self.queue_worker.get()
            get_edges(edge, self.time)
            new_items = list(DATA_DAG[edge[0]]['edges'].items())
            try:
                self.queue_worker.put(new_items[0])
                del new_items[0]
                list(map(first_edges.put, new_items))
            except Exception as e:
                e
        return edge


def start_thread(edge, start_time):
    """start a thread to read a edge
           inputs:
		start_time(timestamp): time of program start
                edge (tuple(str,int)): a tuple of edge and time to sleep
           return
             worker(Thread): thread to put into the active threads array
    """
    worker = DownloadWorker(edge, start_time)
    worker.start()
    return worker


def check_comp():
    """Checks active threads 
    """
    for thread_worker in comp_active_thread:
        if not thread_worker.is_alive():
            comp_active_thread.remove(thread_worker)


def main():

    parser = argparse.ArgumentParser(description='give data name.')
    parser.add_argument('data_name',
                        metavar='N',
                        nargs='?',
                        type=str,
                        default='data_1.json',
                        help='name of data')

    args = parser.parse_args()
    gather_data(args.data_name)
    start_time = time.time()

    while first_edges.qsize() > 0 or len(comp_active_thread) > 1:
        if not first_edges.empty():
            edge = first_edges.get()
            worker = start_thread(edge, start_time)
            comp_active_thread.append(worker)
        else:
            check_comp()


if __name__ == '__main__':
    main()
