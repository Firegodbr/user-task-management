if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="server.app:app", port=8000, host="0.0.0.0", reload=True)