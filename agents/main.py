from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor

from dotenv import load_dotenv

from tools.sql import run_sqlite_tool

load_dotenv()

chat = ChatOpenAI()

prompt = ChatPromptTemplate(
  messages=[
    HumanMessagePromptTemplate.from_template('{input}'),
    MessagesPlaceholder(variable_name='agent_scratchpad')  # agent_scratchpad acts like a simplified memory to keep track of the chat history
  ]
)

tools = [run_sqlite_tool]

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