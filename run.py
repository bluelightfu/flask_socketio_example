from flask import Flask, request, abort, render_template, jsonify
from flask_socketio import SocketIO, emit
from apscheduler.schedulers.background import BackgroundScheduler
import eventlet
eventlet.monkey_patch(thread=True, time=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

@app.route("/status", methods=['GET'])
def upload():
    if not request.json:
        abort(400)

    d = request.json.get("data", 0)
    print("receive data:{}".format(d))
    # do something

    # 回傳給前端
    socketio.emit('status_response', {'data': d})
    return jsonify(
        {"response": "ok"}
    )


@app.route("/")
def home():
    return render_template('home.html', async_mode=socketio.async_mode)

def call():
    socketio.emit('status_response', {'data': 'hi'})

scheduler = BackgroundScheduler(daemon=True,timezone="Asia/Taipei")
scheduler.add_job(func=call,trigger='interval',seconds=5)
scheduler.start()
if __name__ == "__main__":
    socketio = SocketIO(app)
    socketio.run(app, debug=True,port=5050)
    # app.run(debug=True,port=5050,use_reloader=False)
    