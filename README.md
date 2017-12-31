<<<<<<< HEAD
# Rackspace Dev Test
## Overview
The purpose of this script is to allow a user to provide a file, directory, or multiple of these as a command line argument, the script would then find unique domains in each file provided and write out the results to a file. The output file include a list of every unique domain as well as the number of times the domain occurs in the document.
The script assumes that the correct format of a domain that the files provided include emails from which the domains can be extracted. The script also assumes that each domain name consist fo alphanumeric characters, cannot start or end with a hyphen (-), though it may include or or multiple in the middle. The script also assumes the Top Level Domain (TLD) consists of either a generic TLD, a country-specific TLD, or a ocmbination of both.
## Design
The program makes use of threads to allow for multiple files to be processed simultaneously, ensuring optimum time and memory usage. The script is currently limited to only sixteen (16) threads as trial and error has shown no benefit to adding more threads. 
The files provided are enqueued into file_queue after determining that they are, indeed, files, as well as that they are readable. Each thread will then apply a lock to the queue and dequeue the files. The lock allows each thread to access the resource without risk of a race-condition to occur. By having the threads continuously running, the risk of deadlock is mitigated as each thread will eventually gain access the to the resource. 
Once each thread has finished processing a file, a message is printed onto the screen to alert the user of success or failure. 
## Usage
In order to run the script, please use the following syntax:
    python2.7 DomainCounter.py FILE|DIRECTORY [FILE|DIRECTORY...]
## Future Steps
The next step in the program would be to use the argparse module to allow for more options to the script such as changing the number of threads. Previous implementation of the module caused the program to crash in a not-so-graceful way.
A recursive search of directory is also in the work, though a limit must be applied (providing '/' as an argument shouldn't cause the system to crash... As I've learned the hard way).
=======
# Rackspace Dev Test
### Description
This script allows the user to provide a file, multiple files, a directory, or multiple directories (or a combination of both) to determine the unique domains within. The script assumes that the list provided contain email addresses from which a domain can be extracted.  
The script creates 16 threads to split the work required to analyze each document. The threads coninuously work until the work queue is emptied; a user can provide as many files as needed.
>>>>>>> 5b4b01e23fcf273a1b6157eb803dc02513db2335
