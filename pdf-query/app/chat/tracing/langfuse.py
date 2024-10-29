import os

from langfuse.client import Langfuse


langfuse = Langfuse(
  os.environ['LANGFUSE_PUBLIC_KEY'],
  os.environ['LANGFUSE_SECRET_KEY'],
  # host='https://prod-langfuse.fly.dev'  # self-hosted langfuse
  host='https://us.cloud.langfuse.com'  # default one pointed to langfuse official hosting service
)
