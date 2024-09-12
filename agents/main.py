from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from langchain.schema import SystemMessage

from dotenv import load_dotenv

from tools.sql import list_tables, describe_table_tool, run_sqlite_tool
from tools.report import write_report_tool

load_dotenv()

chat = ChatOpenAI()

tables = list_tables()

prompt = ChatPromptTemplate(
  messages=[
    # only declare table names here in the SystemMessage to reduce message length
    # detailed table schema will be provided via a new tool for ChatGPT to use when it needs
    # SystemMessage(content='You are an AI that has access to a SQLite database which has the following tables: {tables}'),

    # better SystemMessage content
    SystemMessage(content=(
      'You are an AI that has access to a SQLite database.\n'
      f'The database has tables of {tables}.\n'
      'Do not make any assumptions about what tables or columns exist.\n'
      'Let make use of the provided "describe_tables" function instead.'
    )),
    HumanMessagePromptTemplate.from_template('{input}'),
    MessagesPlaceholder(variable_name='agent_scratchpad')  # agent_scratchpad acts like a simplified memory to keep track of the chat history
  ]
)

tools = [
  describe_table_tool, 
  run_sqlite_tool, 
  write_report_tool
]

agent = OpenAIFunctionsAgent(
  llm=chat,
  prompt=prompt,
  tools=tools
)

agent_executor = AgentExecutor(
  agent=agent,
  verbose=True,
  tools=tools
)

# worked since it's simple enough
# agent_executor('How many users are in the database?')

# did not work, needs more work here, eventually it worked with describe_table_tool in place
# agent_executor('How many users have provided a shipping address?')

# testing for generate report
# ChatGPT output: The top 5 most popular products have been summarized and written to a report file. You can download the report from [this link](sandbox:/top_5_popular_products_report.html)
agent_executor('Summarize the top 5 most popular products. Write the results to a report file')