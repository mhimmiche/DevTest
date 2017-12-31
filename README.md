# Rackspace Dev Test
## Overview
The purpose of this script is to find unique domains from files provided by the user. All results are written to an output file. The output file includes a list of every unique domain as well as the number of times each domain occurs in the input file.  
The script assumes that the provided file includes emails from which the domains can be extracted. The script also assumes that each domain name consist of alphanumeric characters, does not start or end with a hyphen (-), and does not include any other special character. The Top Level Domain (TLD) consists of either a generic TLD (.com), a country-specific TLD (.uk), or a combination of both (.co.uk).  
## Design
To find unique domains, the program utilizes a regular expression pattern to find every match within the document.  
The program makes use of threads to allow for multiple files to be processed simultaneously, ensuring optimum time and memory usage. The script is currently limited to only sixteen (16) threads, as testing has shown no benefit to adding more threads.  :
The files provided are enqueued into a queue after determining that they are, indeed, files, as well as that they are readable. Each thread will then apply a lock to the queue and dequeue a file yo operate on. The lock allows each thread to access the resource without risk of a race-condition to occur. By having the threads continuously running, the risk of deadlock is mitigated as each thread will eventually gain access the to the resource.   
Once each thread has finished processing a file, a message is printed onto the screen to alert the user of which file was processed.   
## Usage
In order to run the script, please use the following syntax:  
* python2.7 DomainCounter.py FILE|DIRECTORY [FILE|DIRECTORY...]
## Future Steps
Next iterations of the program will focus on:
* Using the argparse module to allow for more options for the script, such as changing the number of threads. Previous implementation of the module caused the program to crash in a not-so-graceful way. Further research and reading is required for optimum implementation.
* A recursive search of a provided directory is also in the works, though a limit must be applied to limit the depth of the search (providing '/' as an argument shouldn't cause the system to crash... As I've learned the hard way).
