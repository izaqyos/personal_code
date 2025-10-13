from flask import Flask
app = Flask(__name__)

@app.route('/')
def is_alive():
    return "Hello Flask server is alive"

@app.route('/hello/<name>')
def hello_name(name):
    return f"Hello {name}"

def main():
    app.run(port=3333, debug=True)
if __name__=="__main__":
    main()



