import sqlite3

from langchain.tools import Tool

conn = sqlite3.connect('../db.sqlite')

def run_sqlite_query(query):
  c = conn.cursor()
  c.execute(query)

  return c.fetchall()

run_sqlite_tool = Tool.from_function(
  name='run_sqlite_query',
  description='Run a sqlite query',  # must be precise in order to tell ChatGPT what needs to be done
  func=run_sqlite_query
)