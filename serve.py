import uvicorn
import writer.serve
import logging

# Configure logging
app_path = "."  # . for current working directory
mode = "edit"  # run or edit

try:
    asgi_app = writer.serve.get_asgi_app(app_path, mode)
    uvicorn.run(asgi_app,
                host="0.0.0.0",
                port=8080,
                log_level="debug",
                ws_max_size=writer.serve.MAX_WEBSOCKET_MESSAGE_SIZE)
except Exception as e:
    logging.error(f"An error occurred: {e}")
