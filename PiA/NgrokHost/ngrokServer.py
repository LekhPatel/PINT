from flask import Flask, request, render_template_string, redirect
from SendTextMessage import send_message, webreq

app = Flask(__name__)

URL_FILE = "recipient_url.txt"
MESSAGE_FILE = "message_to_send.txt"
MESSAGE_HISTORY_FILE = "message_history.txt"
WEB_HISTORY_FILE = "web_history.txt"
latest_received_message = "No message yet."
status_message = "No messages sent yet."

def save_url(url):
    with open(URL_FILE, "w") as f:
        f.write(url.strip())

def load_url():
    try:
        with open(URL_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""

def save_message_to_send(msg):
    with open(MESSAGE_FILE, "w") as f:
        f.write(msg.strip())

def save_message_history(msg):
    with open(MESSAGE_HISTORY_FILE, "a") as f:
        f.write(msg.strip() + '\n')

def save_web_history(msg):
    with open(WEB_HISTORY_FILE, "a") as f:
        f.write(msg.strip() + '\n')

        
def load_web_history():
    try:
        with open(WEB_HISTORY_FILE, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def load_history():
    try:
        with open(MESSAGE_HISTORY_FILE, "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def load_message_to_send():
    try:
        with open(MESSAGE_FILE, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""

@app.route('/email', methods=['GET', 'POST'])
def email():
    global status_message

    recipient_url = load_url()
    msg_to_send = load_message_to_send()
    message_history = load_history()

    if request.method == 'POST':
        if 'save_url' in request.form:
            save_url(request.form['url'])
            status_message = f" URL saved: {request.form['url']}"

        elif 'send_message' in request.form:
            message = request.form['message']
            save_message_to_send(message)
            url = load_url()
            
            status_message = send_message(url, message)
            print(status_message[-16:-1])
            if status_message[-16:-1] == "Message receive":
                save_message_history("Sent: " + message + "<br>" + "\n")
            else:
                save_message_history("Message sending failed" + "<br>" + "\n")
    
    return render_template_string("""
        <h2> Pi Communication Interface</h2>

        <form method="POST">
            <label><b>Recipient URL:</b></label><br>
            <input name="url" type="text" size="50" value="{{ url }}"><br>
            <input type="submit" name="save_url" value="Save URL">
        </form>

        <hr>

        <form method="POST">
            <label><b>Message to Send:</b></label><br>
            <input name="message" type="text" size="50" value="{{ msg }}"><br>
            <input type="submit" name="send_message" value="Send Message">
        </form>

        <hr>

        <h3>Status:</h3>
        <p>{{ status }}</p>

        <h3> Latest Received Message:</h3>
        <p>{{ latest }}</p>
        <h3> Message History:</h3>
        <p>{{ history | safe }}</p>
    """, url=recipient_url, msg=msg_to_send, status=status_message, latest=latest_received_message, history = message_history)

@app.route('/browse', methods=['GET', 'POST'])
def browse():
    message_history = load_web_history()
    status_message = "" 
    url = load_url() 
    if request.method == 'POST':
        if 'web_request' in request.form:
            save_web_history(request.form['web_req'])

            status_message = f" web_req saved: {request.form['web_req']}"

            web_url = request.form['web_req']
            
            status_message = webreq(url, web_url)
            print(status_message)
            print(web_url)
            
    url = load_url()

    return render_template_string("""
        <h2> Browse PINT websites</h2>

        <form method="POST">
            <label><b>Request URL:</b></label><br>
            <input name="web_req" type="text" size="50" value="{{ url }}"><br>
            <input type="submit" name="web_request" value="Search">
        </form>

        <hr>

        <hr>

        <h3>Status:</h3>
        <p>{{ status }}</p>

        <h3> Visit history:</h3>
        <p>{{ history | safe }}</p>
        <a href = "/visit"> Visit </a>
    """, url=url, status=status_message, history = message_history)

@app.route('/visit')
def visit():
    try:
        with open("/index.txt", "r") as f:
            webpage_content = f.read()
    except FileNotFoundError:
        webpage_content = "<p><i>index.txt not found.</i></p>"

    return render_template_string("""
        <h2> Visiting Website from Peer B</h2>
        <hr>
        {{ content | safe }}
    """, content=webpage_content)


@app.route('/')
def home():
   return render_template_string("""
        <a href = "/email"> email </a> <br>
        <a href = "/browse"> browse </a>
    """) 

@app.route('/receive', methods=['POST'])
def receive():
    global latest_received_message
    latest_received_message = request.form.get('text', '[No message]')
    save_message_history("Received: " + latest_received_message + "<br>" + "\n")
    print("Received:", latest_received_message)
    return "Message received"

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save(f"/{file.filename}")
    return f"{file.filename} received!"

@app.route('/webreq', methods=['POST'])
def webreq_receiver():
    text = request.form.get('text', '[No website]')
    print("Website requested:", text)
    # Optionally save or handle the text
    files = {'file': open('/Host/index.txt', 'rb')}
    upload_web_files(url, files)
    return "Website request received"



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
