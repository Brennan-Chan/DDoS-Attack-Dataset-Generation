from flask import Flask, request, session, redirect, url_for, render_template_string, jsonify
from flask_socketio import SocketIO, send
from collections import defaultdict
likes = defaultdict(int)
comments = defaultdict(list)


app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')
app.secret_key = 'superfake'  # Needed for sessions


fake_stories = {
    "1": "Aliens Found in Wisconsin!",
    "2": "Elon Musk Buys the Moon",
    "3": "AI Now Predicts Your Lunch"
}


@app.route('/')
def index():
    return "<h1>Welcome to Fake News Network</h1><p><a href='/shop'>Shop</a> | <a href='/login'>Login</a></p>"


@app.route('/like/<id>')
def like(id):
    likes[id] += 1
    return redirect(url_for('story', id=id))


comments = defaultdict(list)

@socketio.on('message')
def handle_message(msg):
    print(f"Websocket Received: {msg}")
    send(f"E: {msg}")

@app.route('/story/<id>', methods=['GET', 'POST'])
def story(id):
    if request.method == 'POST':
        text = request.form.get('comment')
        if text:
            comments[id].append(text)
        return redirect(url_for('story', id=id))


    story_title = fake_stories.get(id, 'Story Not Found')
    story_comments = ''.join(f"<li>{c}</li>" for c in comments[id])
    return f'''
        <a href="/">Home</a> | <a href="/stories">Back to Stories</a><br>
        <h2>{story_title}</h2>
        <p>Likes: {likes[id]} <a href="/like/{id}">[+]</a></p>
        <form method="POST">
                <input name="comment" placeholder="Leave a comment">
                <button>Post</button>
        </form>
        <h3>Comments:</h3>
        <ul>{story_comments}</ul>
    '''


@app.route('/stories')
def stories():
    links = ''.join([f'<li><a href="/story/{k}">{v}</a></li>' for k, v in fake_stories.items()])
    return f'''
        <a href="/">Home</a><br>
        <h1>News Feed</h1>
        <ul>{links}</ul>
    '''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form.get('username')
        return redirect(url_for('stories'))
    return '''
        <a href="/">Home</a><br>
        <form method="POST">
            Username: <input name="username"><br>
            Password: <input name="password"><br>
            <button type="submit">Login</button>
        </form>
    '''


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    return f"<h1>Welcome, {session['user']}</h1>"


@app.route('/shop')
def shop():
    return '''
        <a href="/">Home</a><br>
        <h1>Fake News Store</h1>
        <ul>
            <li>Conspiracy Mug - $12</li>
            <li>Tinfoil Hat - $7</li>
        </ul>
        <form action="/shop/checkout" method="POST">
            <input type="text" name="item" placeholder="Item">
            <input type="number" name="qty" placeholder="Qty">
            <button>Checkout</button>
        </form>
    '''

@app.route('/shop/checkout', methods=['POST'])
def checkout():
    return f"Thanks for buying {request.form['qty']} x {request.form['item']}!"


@app.route('/api/data', methods=['GET', 'POST'])
def api_data():
    return jsonify({
            "status": "ok",
            "data": request.json if request.method == 'POST' else "Sample API response"
    })


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=443, ssl_context='adhoc')
