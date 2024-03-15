import logging
import subprocess

def blacklist(app):
    logging.info(f"Blacklisting {app}.")
    subprocess.call(f"sudo ./scripts/blacklist.sh {app}", shell=True)

def whitelist(app):
    logging.info(f"Whitelisting {app}.")
    subprocess.call(f"sudo ./scripts/whitelist.sh {app}", shell=True)
