#!/usr/bin/env python
"""
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
"""
import sys, os, time
from docopt import docopt
from globusonline.transfer.api_client import Transfer, TransferAPIClient, APIError
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import logging 

def get_submission_id():
    code, message, data = api.submission_id()
    api.close()
    return data['value']

def do_transfer(local_ep, local_dir, remote_ep, remote_dir):
    logging.debug('Initiating transfer with:')
    logging.debug('local endpoint: {0}, local dir: {1}, remote endpoint: {2}, remote dir: {3}'.format(local_ep, local_dir, 
                                              remote_ep, remote_dir))
    submission_id = get_submission_id()
    transfer = Transfer(submission_id, 
                        local_ep, remote_ep, 
                        sync_level=3, encrypt_data=True)
    logging.debug('Adding transfer item: {}, {}'.format(local_dir, remote_dir))
    transfer.add_item(local_dir, remote_dir, recursive=True)
    logging.debug('Transfer object as JSON:')
    logging.debug(transfer.as_json())
    logging.debug('API Client instance: {}'.format(api))
    api.transfer(transfer)
    api.close()

class MyEventHandler(LoggingEventHandler):
    
    def __init__(self, local_ep, local_dir, remote_ep, remote_dir):
        self.local_ep = local_ep
        self.local_dir = local_dir
        self.remote_ep = remote_ep
        self.remote_dir = remote_dir
        super(MyEventHandler, self).__init__()

    def on_any_event(self, event):
        logging.debug('Filesystem changed!')
        logging.debug('Starting transfer.')
        do_transfer(self.local_ep, self.local_dir, self.remote_ep, self.remote_dir)
        logging.debug('Transfering.')


if __name__ == '__main__':
    options = docopt(__doc__)
    logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)
    
    username = options['USERNAME']
    local_ep = options['LOCALENDPOINT']
    local_dir = options['LOCALPATH']
    remote_ep = options['REMOTEENDPOINT']
    remote_dir = options['REMOTEPATH']
    oauthtoken = options['OAUTHTOKEN']
    
    logging.debug('Running gosync.py with the following options:')
    logging.debug(options)

    api = TransferAPIClient(username, goauth=oauthtoken, httplib_debuglevel=1, max_attempts=5)
    logging.debug('Client created:')
    logging.debug(api)
    
    logging.debug('Starting initial transfer.')
    
    do_transfer(local_ep, local_dir, remote_ep, remote_dir)
    
    logging.debug('Watching for file system changes.')
    event_handler = MyEventHandler(local_ep, local_dir, remote_ep, remote_dir) 
    observer = Observer()
    logging.debug('Created observer to watch {}.'.format(local_dir))
    observer.schedule(event_handler, local_dir, recursive=True)
    observer.start()
    logging.debug('Observer started.')

    try:
        while True:
            time.sleep(1)
    except:
        observer.stop()
    
    observer.join()
