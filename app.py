from flask import Flask
app = Flask(__name__)
@app.route('/') # it defines the starting point
def hello_world():
    return 'Hello world'
