from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
    return ('ok', 200)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, port=5000)