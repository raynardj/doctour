
from app import app
import argparse
import logging
import os
from doctour.base.utils import startup_log
ap = argparse.ArgumentParser()
ap.add_argument("--port", default=8080, type=int, dest="port")
args = ap.parse_args()

logging.info(startup_log(port=args.port))

if __name__ == "__main__":
    logging.info(f"DocTour Running on port {args.port}")
    app.run(host="0.0.0.0", port=args.port, debug=False)
