
import logging
import subprocess
import tempfile
from os import environ, path, remove

logger = logging.getLogger('make_bundle')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%%(name)s]%%(levelname)s:%%(message)s')
stderr_handler = logging.StreamHandler()
stderr_handler.setFormatter(formatter)
logger.addHandler(stderr_handler)

REQ_FILES = [
    'requirements.txt',
]
    
def pip_create_bundle(workspace, pip, retries=3):
    """
    Create a pybundle for all of the requirements files and return the path.
    """
    bundle_path = workspace + '%(project_name)s.pybundle'

    pip_cmd = [pip, 'bundle', bundle_path]
    for req_f in REQ_FILES:
        req_f = path.abspath(path.join(workspace, req_f))
        pip_cmd += ['-r', req_f]
    returncode = subprocess.call(pip_cmd)
    if returncode != 0:
        remove(bundle_path)
        if retries < 1:
            # We're out of retries
            logger.error("Error creating the bundle")
            exit(returncode)
        # Let's try again
        logger.info(
            "There was an error creating the bundle. Retrying %%s more time(s)",
            retries)
        return pip_create_bundle(workspace, pip, retries=retries-1)

    return bundle_path

print pip_create_bundle('/home/%(user)s/', '/usr/local/bin/pip')