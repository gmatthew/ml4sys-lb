import sys

from fetcher import Fetcher
import time
import argparse
import logging

DATA_RETRIEVAL_INTERVAL_SECONDS = 5

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(stream=sys.stdout,
                    filemode="w",
                    format=LOG_FORMAT,
                    level=logging.ERROR)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def main(output):
  fetcher = Fetcher(output, logger)

  while True:
    logger.info("Processing...")
    fetcher.process()

#    logger.info("Sleeping...")
    #time.sleep(DATA_RETRIEVAL_INTERVAL_SECONDS)


if __name__ == "__main__":
  try:
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=str, required=True, help="output file path")
    args = parser.parse_args()

    main(args.output)
  except KeyboardInterrupt:
    print('stopped!')
