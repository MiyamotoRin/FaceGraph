#Flask
from flask import Flask, render_template, request, Blueprint
from datetime import datetime as dt 
import json

import numpy as np
app = Flask(__name__,  static_folder="static")  
style = "../static/style.css"

@app.route("/")  
def index():
        img_path=["../static/result.png","../static/result_long.png"]
        

        return render_template('index.html', img_path = img_path,style=style)

if __name__ == "__main__":  
        app.run(debug=False, host='0.0.0.0', port=11000)