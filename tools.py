import os
import sys
import subprocess
from isis2json import isis2json

def is_valid_extension(filename):
    extension = filename.split('.')[-1]

    if extension in ['iso', 'part']:
        return True

    return False

def is_valid_file(filemeta):
    """
    This method validates an uploaded file checking the extension and mimetipe.
    The allowed extensions are: ['.iso', '.part']
    """
    content_type = filemeta['content_type']
    filename = filemeta['filename']

    if content_type == u'application/octet-stream' and is_valid_extension(filename):
        return True

    return False


def list_uploaded_files():
    """
    This method list the uploaded files available at the uploads directory.
    """

    return os.listdir('uploads')


def get_json(iso_file_name):
    """
    This method converts an iso file extracted from a ISIS database to JSON, using
    the isi2json api.
    """
    return subprocess.check_output(['isis2json/isis2json.py',
                                    iso_file_name, '-c', '-p', 'v', '-t', '3'])
