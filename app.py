from fake_api import *

from flask import Flask, request, jsonify, session, render_template
from flask_session import Session

app = Flask(__name__)

# Configure session
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'  # Use filesystem-based sessions
Session(app)
def process_symbol(s):
    lines = s.split('\n')
    if lines and lines[0] == "```html" and lines[-1] == "```":
        return '\n'.join(lines[1:-1])  # 删除第一行和最后一行
    return s
# Mock processing function
def process_message(message):
    # Example: Convert message to uppercase as the processing logic
    result=api_answer(message)

    return process_symbol(result)

@app.before_request
def initialize_session():

    if 'messages' not in session:
        system_prompt = "针对用户的需求写出html代码，直接给出代码，以```html为第一行，```为最后一行。尽量多使用emoji，多使用渐变色，多增加互动内容，比如动画和鼠标悬浮气泡弹窗。我会将html放入一个小的容器里，所以尽可能简洁"

        session['messages'] = []  # Initialize an empty list for messages
        session['messages'].append(message_template('system',system_prompt))# Initialize an empty list for messages
@app.route('/')
def index():
    session.clear()  # 清除会话数据
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    if 'message' not in data:
        return jsonify({"error": "Message content is required."}), 400

    user_message = data['message']

    # Append the message to the user's session list
    session['messages'].append(message_template('user',user_message))
    session.modified = True
    print(session['messages'])
    # Process the message
    response_message = process_message(session['messages'])
    # response_message = "text"
    session['messages'].append(message_template('assistant',response_message))

    # Return the processed message
    return jsonify({"response": response_message})

if __name__ == '__main__':
    app.run(debug=True)
