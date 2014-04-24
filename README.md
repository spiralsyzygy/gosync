A simple client for syncing directories between two Globus Online end points. 

Usage: gosync.py USERNAME LOCALENDPOINT LOCALPATH REMOTEENDPOINT REMOTEPATH OAUTHTOKEN

Installation:

You must have a Globus Online account and a Globus Online Personal end point set up on the local machine. 

Check out this repository
    git clone git@github.com:spiralsyzygy/gosync.git

Create a virtualenv
    cd gosync
    virtualenv env
    source env/bin/activate

Install required packages:
    pip install -r requirements.txt
