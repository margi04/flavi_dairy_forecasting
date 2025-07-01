from flask import Flask

app = Flask(__name__)

@app.before_first_request
def init():
    print("✅ Flask .before_first_request is working.")

@app.route('/')
def home():
    return "Hello, Flavi Dairy!"

if __name__ == '__main__':
    app.run(debug=True)
