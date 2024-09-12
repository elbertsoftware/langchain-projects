import sqlite3

from langchain.tools import Tool

conn = sqlite3.connect('db.sqlite')

def list_tables():
  c = conn.cursor()
  c.execute('SELECT name FROM sqlite_master WHERE type="table";')
  rows = c.fetchall()
  # print(tables)

  return '\n'.join(row[0] for row in rows if row[0] is not None)

def describe_tables(table_names):
  c = conn.cursor()

  tables = ', '.join('"' + table + '"' for table in table_names)
  c.execute(f'SELECT sql FROM sqlite_master WHERE type="table" AND name IN ({tables});')
  rows = c.fetchall()
  # print(rows)

  return '\n'.join(row[0] for row in rows if row[0] is not None) 

def run_sqlite_query(query):
  c = conn.cursor()

  try:
    c.execute(query)
    return c.fetchall()
  except sqlite3.OperationalError as err:
    return f'The following error occured: {str(err)}'

describe_table_tool = Tool.from_function(
  name='describe_tables',  
  description='Given a list of table names, returns the schema of those tables',  # a must for ChatGPT to know what to do
  func=describe_tables  # the method exact name above
)

run_sqlite_tool = Tool.from_function(
  name='run_sqlite_query',
  description='Run a sqlite query',  # must be precise in order to tell ChatGPT what needs to be done
  func=run_sqlite_query  # the method exact name above
)