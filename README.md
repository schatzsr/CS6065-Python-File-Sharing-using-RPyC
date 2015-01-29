PyFileShare
===========

Python File Share.

Python File Share is a command line file sharing application. You may work from a server via ip or use a localhost.

To run the server move server.py

To run the client move client.py to a directory. Now add two folders to this directory, one will contain the files you wish to share, the other will be the location for the server to write files to.

Navigate to the directory containing your python file. 
If you are running an instance of the server on your local host execute as follows.
    >client.py <share_folder_name> <receive_folder_name>
If you have an ip for another machine running a server instance execute as follows.
    >client.py <share_folder_name> <receive_folder_name> <ip>

After successfully connecting to a server you may use the following commands.
    >ls
        This will list the available files nested under what user has uploaded them to the server. The id for both user and document will precede the listing.
    >#<user_id>:<doc_id>
        This will obtain the associated document from the user who's id you pass.
    >q
        This will remove you from the server.

Known Issues:
    *If a user disconnects the server needs to be reset.
        (ReferenceError: weakly-referenced object no longer exists)