import logging
import os
from logging.handlers import RotatingFileHandler

from peerberrypy import API
from peerberrypy.exceptions import InsufficientFunds

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

    loans = api_client.get_loans(min_interest_rate=10,
                                 max_remaining_term=60,
                                 group_guarantee=True,
                                 exclude_invested_loans=True,
                                 sort="interest_rate",
                                 quantity=100,
                                 raw=True)

    logging.info(f"Found {len(loans)} loans matching criteria")

    for loan in loans:
        logging.info(f"Purchasing #" + loan["loanId"])
        try:
            api_client.purchase_loan(loan["loanId"], AMOUNT_TO_BUY)
        except InsufficientFunds:
            logging.info("No funds left. Halting purchases.")
            break

    api_client.logout()
    logging.info("Logged out.")
