0. Launch Anaconda PowerShell
   
1. cd "C:\Users\Kenneth\Documents\Courses\Udemy - ChatGPT and Langchain - The Complete Developer Masterclass\langchain-projects\agents"
2. conda activate langchain
3. pipenv install (run once)
4. pip install pyboxen (run once)
5. pipenv shell
   
6. python main.py

7.  exit
8.  conda deactivate

Use the online tool to generate JSON schema:
https://transform.tools/json-to-json-schema

input:
{
  "query": "SELECT..."
}

output:
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Generated schema for Root",
  "type": "object",
  "properties": {
    "query": {
      "type": "string"
    }
  },
  "required": [
    "query"
  ]
}

use only this section for the "parameters" of the ChatGPT function definitions:

"parameters": {
  {
    "type": "object",
    "properties": {
      "query": {
        "type": "string"
      }
    },
    "required": [
      "query"
    ]
  }
}