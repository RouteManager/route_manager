from flask import Flask
from route_manager.route_manager import RouteManager
import signal
import sys

app = Flask(__name__)


@app.route("/")
def hello():
    route_manager.calc_fitness_for_routes()
    return "Hello from Route Optimizer+ Running in port 6001."


def handler(signum, frame):
    print("Signal handler called with signal", signum)
    sys.exit(0)


# Set the signal handler
signal.signal(signal.SIGTERM, handler)

if __name__ == "__main__":
    # Wellington Arch. Use static not to burden nominatum
    location_point = (51.5025031, -0.15081986768597055)

    route_manager = RouteManager(location_point, 900, "skate")
    route_manager._load_graph()
    route_manager.add_shortest_path_route("test_route", 60852813, 26389730)

    app.run(host="0.0.0.0", port=6001, use_reloader=True)
