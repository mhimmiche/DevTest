#!usr/bin/python
"""
Author: Mehdi Himmiche
TODO: Implement argparser to allow user to change thread count through flags and more user-friendly UI
TODO: Allow recursive file lookup without bloating system (would have to apply a path depth limit)
(learned that lesson by passing '/' as an argument and watching my computer explode)
"""
import re
import sys
from os.path import isfile, isdir, realpath
from os import access, R_OK, listdir
import threading
import Queue


class FunctionThread(threading.Thread):
    def __init__(self, thread_id, queue, pattern):
        self.thread_id = thread_id
        self.queue = queue
        self.pattern = pattern
        threading.Thread.__init__(self)

    def run(self):
        """
        Runs the threads created to count unique domains in files.
        """
        domain_counter(self.queue, self.pattern)


def domain_counter(queue, pattern):
    """
    The method counts unique domain names in a file provided, it ensures that each thread handles one file at a time.
    Using threads allows for parallel work when multiple files are provided, making the script run smoothly and faster
    :param queue: a queue containing all input files provided to the script
    :param pattern: the pattern to test against (in this case it's the pattern for domain names in emails)
    """
    while not end_of_work:
        thread_lock.acquire()
        if not queue.empty():
            in_file = queue.get()
            thread_lock.release()
            out_file = in_file + "_output.txt"
            domain_list = read_file(in_file, pattern)
            write_file(in_file, out_file, domain_list)
            print "Script has finished running for {0}. Results can be found in {1}".format(in_file, out_file)
        else:
            thread_lock.release()


def read_file(file_name, pattern):
    """
    Method created to read the files provided. This ensures better readability and easier follow of code.
    Reading files as binary mitigates the risk that files provided are not readable text files
    i.e. user provides image, application, or even image within a text file (sneaky sneaky)
    :param file_name: name of the file to read
    :param pattern: patter to test the contents of the file against
    :return: a dict containing the unique domains and count of each one, or an empty dict if no domain is found.
    """
    hash_list = {}
    with open(file_name, "rb") as bin_file:
        for line in bin_file:
            if pattern.search(line):
                domain = pattern.search(line).group()[1:]
                if domain in hash_list:
                    hash_list[domain] += 1
                else:
                    hash_list.update({domain: 1})
    return hash_list


def write_file(file_name_in, file_name_out, hash_list):
    """
    Method to write contents of the dict into an output file.
    :param file_name_in: name of the file provided, this allows to write more information int he output file.
    :param file_name_out: name of the output file to write domain info in.
    :param hash_list: dict containing the domain information from the input file.
    """
    with open(file_name_out, "w") as bin_out:
        if len(hash_list) > 0:
            bin_out.write("Here are the result for {0}\n".format(file_name_in))
            for key, value in sorted(hash_list.items(), key=lambda x: x[1], reverse=True):
                bin_out.write("\t{0} --> {1}\n".format(key, value))
        else:
            bin_out.write("The file provided, {0}, contained no unique domains.".format(file_name_in))


def start_threads(t_list, t_count, queue, pattern):
    """
    This method starts all the threads required for this script.
    :param t_list: list containing all running threads.
    :param t_count: maximum count of threads to create
    :param queue: queue of files to test, this allows the threads to pull file names from the provided arguments
    :param pattern: pattern to test the files against
    """
    current_thread = 0  # Keeps track of thread ID created (counting starts at 0 or /r/programmerhumor will have a fit)
    while current_thread < t_count:
        curr_thread = FunctionThread(current_thread, queue, pattern)
        curr_thread.start() # Starting the theads helps mitigate deadlock as threads will eventually get access to resource as it becomes available.
        t_list.append(curr_thread)
        current_thread += 1


if __name__ == '__main__':
    # Flag created to allow for thread termination.
    # Ensures that every thread can be joined when all work is done.
    # https://www.tutorialspoint.com/python/python_multithreading.htm
    end_of_work = False
    max_threads = 16  # Max number of threads to be created, value can be changed depending on needs
    thread_list = []
    domain_pattern = re.compile('@[^\W](\w|-)*[^\W](\.\w*){1,2}')
    thread_lock = threading.Lock()  # Creates a lock to ensure that no race condition occurs between threads
    file_queue = Queue.Queue()
    start_threads(thread_list, max_threads, file_queue, domain_pattern)
    thread_lock.acquire()
    if len(sys.argv) == 1:
        print "Description:\n\tThis script allows a user to provide a file or directory to find unique domains"
        print "\tUser may pass more than one file or directory to the script"
        print "Usage:"
        print "\tpython {0} FILE|DIRECTORY [FILES|DIRECTORY..]".format(sys.argv[0])
    else:
        for arg in sys.argv[1:]:
            if isfile(arg) and access(arg, R_OK):
                file_queue.put(realpath(arg))
            elif isdir(arg):
                for file_in_dir in listdir(arg):
                    if isfile(file_in_dir) and access(file_in_dir, R_OK):
                        file_queue.put(realpath(file_in_dir))
            else:
                print "Could not fine file {0} provided. Skipping over it.".format(arg)
    thread_lock.release()
    while not file_queue.empty():
        pass
    end_of_work = True
    for thread in thread_list:
        thread.join()
    print "{0} has finished running. Thank you for using it.".format(sys.argv[0])
