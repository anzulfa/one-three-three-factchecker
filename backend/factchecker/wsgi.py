from factchecker import app

if __name__ == "__main__":
    print("Running wsgi app on port 8080...")
    from waitress import serve
    serve(app, host="127.0.0.1", port=8080)
