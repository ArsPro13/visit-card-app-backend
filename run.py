from flask import Flask

app = Flask(__name__)

@app.route('/login', methods=['GET'])
def login():
    return "Hello from /login over HTTPS!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
