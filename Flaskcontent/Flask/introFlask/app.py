from flask import Flask


app=Flask(__name__)

@app.route('/')
def hello():
    return "Hello this is my flask server"

@app.route('/about')
def about():
    return "This is about page of my flask server"


if __name__=="__main__":
    app.run(debug=True)