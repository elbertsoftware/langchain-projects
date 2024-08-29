from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

from argparse import ArgumentParser
from dotenv import load_dotenv

# moved to .env file which should not be checked in
# api_key = 'sk...'

parser = ArgumentParser()
parser.add_argument('--language', default='python')
parser.add_argument('--task', default='returns a list of numbers')

# python main.py --language java --task 'prints Hello World to the console'
args = parser.parse_args()

load_dotenv()  # OpenAI class below will look for API key from the environment variable OPENAI_API_KEY
llm = OpenAI(
  #openai_api_key=api_key
)

code_prompt = PromptTemplate(
  input_variables=['language', 'task'],
  template='Write a short {language} function which {task}'
)

test_prompt = PromptTemplate(
  input_variables=['language', 'code'],
  template='Write actual unit tests in the {language} for the following code:\n{code}'
)

code_chain = LLMChain(
  llm=llm,
  prompt=code_prompt,
  output_key='code'
)

test_chain = LLMChain(
  llm=llm,
  prompt=test_prompt,
  output_key='test'
)

chain = SequentialChain(
  chains=[code_chain, test_chain],
  input_variables=['language', 'task'],
  output_variables=['code', 'test']
)

result = chain({
  'language': args.language,
  'task': args.task
})

#print(result)
print(f'\nGenerated code:\n{result["code"]}')
print(f'\nGenerated test:\n{result["test"]}')

