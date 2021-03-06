from flask import Flask
app = Flask(__name__)

@app.route('/ping')
def ping():
    return 'pong'

@app.route('/gated_ping')
def gatedPing():
    return 'gated_pong'

@app.route('/secure_ping')
def loggedInPing():
    return 'secure_pong'

if __name__ == '__main__':
    app.run(host='0.0.0.0')