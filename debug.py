import uvicorn

if __name__ == '__main__':
    uvicorn.run("app.app:app", host="0.0.0.0", port=8004, reload=False, log_level="debug", access_log=True)