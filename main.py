import logging
import os
import sys
import time
from logging.handlers import RotatingFileHandler

from peerberrypy import API
from peerberrypy.exceptions import InsufficientFunds, TooManyRequestsException

if __name__ == "__main__":

    # amount in EUR to allocate to each loan
    AMOUNT_TO_BUY = 10

    logging.basicConfig(
        handlers=[RotatingFileHandler('log.txt', maxBytes=100000, backupCount=10),
                  logging.StreamHandler()],
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s %(message)s",
        datefmt='%Y-%m-%dT%H:%M:%S')

    api_client = API(
        email=os.environ['PEERBERRY_EMAIL'],
        password=os.environ['PEERBERRY_PASSWORD'],
    )
    logging.info("Logged in.")

    available_balance = api_client.get_overview()["availableMoney"]
    logging.info(f"Available balance: {available_balance}€")
    if not available_balance >= min(10, AMOUNT_TO_BUY):
        logging.info("Available balance below 10€ or below the purchase amount. Aborting.")
        sys.exit()

    # take a 20% margin (some loans will become unavailable for purchase by the time we try to purchase them
    loans_needed = int((available_balance * 1.2) // AMOUNT_TO_BUY)

    loans = api_client.get_loans(min_interest_rate=10,
                                 max_remaining_term=60,
                                 group_guarantee=True,
                                 exclude_invested_loans=True,
                                 sort="interest_rate",
                                 quantity=loans_needed,
                                 raw=True)

    logging.info(f"Found {len(loans)} loans matching criteria (max requested: {loans_needed})")

    for loan in loans:
        logging.info(f"Purchasing #" + str(loan["loanId"]))
        try:
            api_client.purchase_loan(loan["loanId"], 10)
        except TooManyRequestsException:
            logging.error("Too many API requests. Sleeping for 1 minute, then resuming purchases")
            time.sleep(60)
            continue
        except InsufficientFunds as e:
            # known cases:
            # - The remaining available loan amount after investment cannot be less than the minimum investment amount
            # - The loan is sold out
            logging.info("Failed buying, skipping")
            logging.info(f"Error message: {e}")
            continue
        time.sleep(2)

    api_client.logout()
    logging.info("Logged out.")
