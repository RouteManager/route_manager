from flask import Flask
import signal
import sys

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello from Route Optimizer+ Running in port 6001."


def handler(signum, frame):
    print("Signal handler called with signal", signum)
    sys.exit(0)


# Set the signal handler
signal.signal(signal.SIGTERM, handler)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6001, use_reloader=True)
