import os
from tinydb import TinyDB
from cement.utils import fs


def extend_tinydb(app):
    app.log.debug('extending jhta application with tinydb')
    db_file = app.config.get('jhta', 'db_file')
    
    # ensure that we expand the full path
    db_file = fs.abspath(db_file)
    app.log.debug('tinydb database file is: %s' % db_file)
    
    # ensure our parent directory exists
    db_dir = os.path.dirname(db_file)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    app.extend('db', TinyDB(db_file))

