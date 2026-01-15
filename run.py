import uvicorn

if __name__ == "__main__":
    # "app.main:app" refers to package 'app', file 'main.py', object 'app'
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
