from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from langchain.schema import SystemMessage

from dotenv import load_dotenv

from tools.sql import list_tables, describe_table_tool, run_sqlite_tool

load_dotenv()

chat = ChatOpenAI()

tables = list_tables()

prompt = ChatPromptTemplate(
  messages=[
    # only declare table names here in the SystemMessage to reduce message length
    # detailed table schema will be provided via a new tool for ChatGPT to use when it needs
    SystemMessage(content=f'You are an AI that has access to a SQLite database which has the following tables:\n{tables}'),
    HumanMessagePromptTemplate.from_template('{input}'),
    MessagesPlaceholder(variable_name='agent_scratchpad')  # agent_scratchpad acts like a simplified memory to keep track of the chat history
  ]
)

tools = [describe_table_tool, run_sqlite_tool]

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

# did not work, needs more work here
agent_executor('How many users have provided a shipping address?')