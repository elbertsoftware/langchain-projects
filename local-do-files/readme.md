Use this to run a local file-upload server.

# Setup

- Run `pipenv install` to install dependencies then run `pipenv shell` to enter the Pipenv environment
- Start the server with `python app.py`
- In the `pdf-query` project, find the `.env` file and change the `UPLOAD_URL` line to the following: `UPLOAD_URL=http://localhost:8050`
- Exit the Pipenv virtual enviorment and recreate using `pipenv shell`
- Run `inv dev` to restart the pdf-query application
- Run `inv devworker` to start  pdf-query's worker
