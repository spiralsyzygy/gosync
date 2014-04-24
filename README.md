A simple client for syncing directories between two Globus Online end points. 

Usage: gosync.py USERNAME LOCALENDPOINT LOCALPATH REMOTEENDPOINT REMOTEPATH OAUTHTOKEN

Arguments:
    USERNAME         Globus Online username.
    LOCALENDPOINT    Local end point.
    REMOTEENDPOINT   Remote end point.
    LOCALPATH        The local path to sync from.
    REMOTEPATH       The remote path to sync to.
    OAUTHTOKEN       Globus Online OAuth token string.

Options:
    -h --help           show this help.
    --version           print version
