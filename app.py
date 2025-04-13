from flask import Flask, request, render_template

app = Flask(__name__)
messages = []

app = Flask(__name__)

def process_input(link, message):
  print("Received link:", link)
  print("Received message:", message)

@app.route("/", methods=["GET", "POST"])
def index():
  if request.method == "POST":
      link = request.form.get("link")
      message = request.form.get("message")  
      # Call the function
      process_input(link, message)
  return render_template("index.html")
