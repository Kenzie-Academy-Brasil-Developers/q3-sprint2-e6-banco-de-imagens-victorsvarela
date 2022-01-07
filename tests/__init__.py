from flask import Flask

app = Flask(__name__)

@app.post("/upload")
def upload():
    pass