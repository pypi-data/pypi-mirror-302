from urllib.parse import unquote, urlparse
import pymysql

def _parse_connection_string(url: str) -> dict:
  conn = urlparse(url)
  if conn.scheme != 'mysql':
    raise ValueError("Invalid connection string")
  
  result = {}
  result['hostname'] = conn.hostname
  result['port'] = conn.port if conn.port else None
  result['username'] = unquote(conn.username) if conn.username != '' else None
  result['password'] = unquote(conn.password) if conn.password != '' else None
  database = conn.path.split('/')[-1]
  result['database'] = database if database != '' else None
  return result


def get_db_connection(url: str) -> pymysql.Connection:
  """Get a connection to a MySQL database from a url style connection string.
  Param url: MySQL connection string, e.g.: mysql://user:password@hostname:port/database"""
  conn = _parse_connection_string(url)
  try:
    return pymysql.connect(
        host=conn['hostname'],
        port=conn['port'],
        user=conn['username'],
        passwd=conn['password'],
        db=conn['database'],
        connect_timeout=5,
        cursorclass=pymysql.cursors.DictCursor,
    )
  except pymysql.MySQLError as e:
      print(f"Database connection failed: {e}")
      raise