import sqlite3 as db
import settings, datetime
       
_db_connection = None

def get_connection():
    global _db_connection
    """Return the database connection. """
    if not _db_connection: 
        _db_connection = db.connect(settings.DB_DATABASE)
        _db_connection.row_factory = db.Row
        # create schema if db is empty
        cur = _db_connection.cursor()
        cur.execute('select count(*) from sqlite_master WHERE type=\'table\'')
        if cur.fetchone()[0] == 0:
            cur.executescript(settings.DDE_SCRIPT)
    return _db_connection

def query(sql_statement, parameters = ()):
    """Executes a SELECT statement on the database and returns the resultset as an associative dictionary. """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql_statement, parameters)    
    return cur.fetchall()

def query_row(sql_statement, parameters = ()):
    """Executes a SELECT statement on the database and returns the first row as a list. """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql_statement, parameters)    
    rows = cur.fetchone()    
    return rows

def execute(sql_statement, parameters = ()):
    """Executes an insert, update or delete statement and returns the affected row and last inserted id. """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql_statement, parameters)
    return (cur.rowcount, cur.lastrowid)

def get_global_param(param_name):
    """Returns the value of a global parameter from the DB. """
    param_objtype = '__GLOBAL__'
    row = query_row('SELECT ParamValue FROM Param WHERE ParamName=? AND ParamObjType=?', (param_name, param_objtype))
    return row[0]

def set_global_param(param_name, param_value, param_desc = None):
    """Sets the value of a global parameter in the DB. """
    param_objtype = '__GLOBAL__'
    res = query_row('SELECT COUNT(*) FROM Param WHERE ParamName=? AND ParamObjType=?', (param_name, param_objtype))
    if (res[0] == 0):
        retval = execute('INSERT INTO Param (ParamName, ParamValue, ParamDesc) VALUES (?, ?, ?)', (param_name, param_value, param_desc))
    else:
        retval = execute('UPDATE Param SET ParamValue = ?, ParamDesc = ? WHERE ParamObjType = ? AND ParamName = ?', (param_value, param_desc, param_objtype, param_name))
    return retval

def commit():
    """Commits the current transaction and opens a new one."""
    global _db_connection
    _db_connection.commit()

def rollback():
    """Rollbacks the current transaction and opens a new one."""
    global _db_connection
    _db_connection.rollback()

def close():
    """Close the current database connection. """
    global _db_connection
    if _db_connection: _db_connection.close()
