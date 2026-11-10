from flask import Flask, render_template


app=Flask(__name__)

clients = [
    {"name": "Acme Corporation", "industry": "Technology", "status": "Active"},
    {"name": "Global Tech Logistics", "industry": "Supply Chain", "status": "Active"},
    {"name": "Apex Financial Group", "industry": "Finance", "status": "Active"},
]

@app.route('/')
def home():
    return render_template('home.html')
#jinja2 template engine is used to render the html pages in flask

  
@app.route("/custom/about")
def custom_about():
    return render_template('about.html', clients=clients)
    
    

if __name__=="__main__":
    app.run(debug=True)