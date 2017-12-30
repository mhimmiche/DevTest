# Rackspace Dev Test
### Description
This script allows the user to provide a file, multiple files, a directory, or multiple directories (or a combination of both) to determine the unique domains within. The script assumes that the list provided contain email addresses from which a domain can be extracted.  
The script creates 16 threads to split the work required to analyze each document. The threads coninuously work until the work queue is emptied; a user can provide as many files as needed.
