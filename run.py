import uvicorn
import sys
import asyncio

if __name__ == "__main__":
    # Fix for Playwright on Windows: "NotImplementedError" in asyncio
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    # "app.main:app" refers to package 'app', file 'main.py', object 'app'
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
