from flask import Flask
server = Flask(__name__)

@server.route("/")
def helloWorld():
    return "Hello World"

def main():
    server.run(host='0.0.0.0', port='80')

if __name__ == "__main__":
    main()
