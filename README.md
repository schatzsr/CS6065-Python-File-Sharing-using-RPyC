Python File Sharing using RPyC
================

CS6065 Intro to Cloud Computing Project 1

*Cloned from University of Cincinnati's git site, github.uc.edu*

*Assignment Outline: https://docs.google.com/document/d/1rp1nNmEYoRUtE30CGOO6jAli4SXybevYwDQO-D_dR3k/*

*Sean Schatzman and Anthony Kleiser*

### Python File Share.

Python File Share is a command line file sharing application. You may work from a server via ip or use a localhost.

Move client.py and server.py to a directory and create a folder that will hold your files being shared and a folder that will contain your downloaded files.

To run the server navigate to the correct diretory and run.

`python server.py`

To run the client navigate to the correct directory and run.

`python client.py shareFolderDirectory downloadFolderDirectory optionIP`

If the ip is blank the client will default to using localhost.

After successfully connecting to a server you may use the following commands.

######ls - This will list the available files nested under what user has uploaded them to the server. The id for both user and document will precede the listing.

######userId:docId - This will obtain the associated document from the user who's id you pass.

######q - This will remove you from the server.

#### Known Issues:

If a user disconnects the server needs to be reset.