import os
from zipfile import ZipFile

"""
 This following class is saving all the files on /tmp/gradana_backup/ as a archieve to the 
specified path.
"""

class ArchieveGenerator(object):
    def __init__(self, *args):

    @property
    def filename(self, *args):
        return str(*args)