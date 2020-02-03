
from app import app
import argparse
import logging
ap = argparse.ArgumentParser()
ap.add_argument("--port", default=8080, type=int, dest="port")
args = ap.parse_args()

if __name__ == "__main__":
    logging.info(f"DocTour Running on port {args.port}")
    app.run(host="0.0.0.0", port=args.port, debug=False)
