# server_setup.py (Optional)
import typing
import writer.serve

if typing.TYPE_CHECKING:
    from fastapi import FastAPI

# Returns the FastAPI application associated with the writer server.
asgi_app: FastAPI = writer.serve.app

# Define a healthcheck endpoint
@asgi_app.get("/probes/healthcheck")
def healthcheck():
    return "1"
