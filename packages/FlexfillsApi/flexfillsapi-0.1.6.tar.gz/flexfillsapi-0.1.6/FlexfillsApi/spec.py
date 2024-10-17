import json
import time
import os
import functools
import logging
# import nest_asyncio
# import asyncio
# import FlexfillsApi

from flexfillsapi import initialize, FlexfillsConnectException

# Apply nest_asyncio to handle nested event loops
# nest_asyncio.apply()


# ******************
# Configuration
# ******************


latest_clusters_file = 'E:/RedStone/Analitic/latest_clusters.json'
pair = "BTC/USDT"
quantity = 0.001
exchanges = ["HUOBI", "OKEX", "BITFINEX", "HITBTC", "BITGET"]
TTL = 5  # Time-to-live for orders before cancellation
flexfills_api = None  # Global FlexfillsApi object
order_filled = False  # Flag to track if the order is filled

max_tries = 5
retry_delay = 5  # Seconds between reconnection attempts


# *************************************
# Decorator for handling Exceptions
# *************************************


def handleAPIException(max_retries=max_tries, delay=retry_delay):
    def decorator_retry(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except FlexfillsConnectException:
                    # handling API connection Error
                    attempts += 1
                    print(
                        f"Flexfills API connection was closed, retrying: {attempts}")
                    logging.warning(
                        f"Flexfills API connection was closed, retrying: {attempts}")

                    login_flexfills()
                    time.sleep(delay)
                except Exception as e:
                    # handling Function excution Error
                    attempts += 1
                    print(
                        f"Failed to excute {func}, retrying: {attempts}")
                    logging.warning(f"Failed to excute {
                                    func}, retrying: {attempts}")

                    time.sleep(delay)

            logging.error(f"Failed after {
                          max_retries} attempts while excuting {func}")
            raise Exception(
                f"Failed after {max_retries} attempts while excuting {func}")

        return wrapper
    return decorator_retry

# --------------------------------
# Login to Flexfills API
# --------------------------------


def login_flexfills():
    global flexfills_api

    print("Initializing FlexfillsApi with provided credentials...")
    logging.info("Initializing FlexfillsApi with provided credentials...")

    flexfills_api = initialize(
        '100000_german', 'abc123', is_test=True)

    print("FlexfillsApi initialized successfully!")
    logging.info("FlexfillsApi initialized successfully!")


# --------------------------------
# Load cluster data from JSON
# --------------------------------


def load_cluster_data():
    try:
        if os.path.exists(latest_clusters_file):
            with open(latest_clusters_file, 'r') as file:
                cluster_data = json.load(file)
            return cluster_data.get("buy_cluster"), cluster_data.get("sell_cluster")
        else:
            print(f"[ERROR] Latest clusters file not found at {
                  latest_clusters_file}")
            logging.error(f"Latest clusters file not found at {
                          latest_clusters_file}")

    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to decode JSON file: {e}")
        logging.error(f"[ERROR] Failed to decode JSON file: {e}")
    except Exception as e:
        print(f"[ERROR] Unexpected error loading cluster data: {e}")
        logging.error(f"[ERROR] Unexpected error loading cluster data: {e}")

    return None, None


# --------------------------------
# Place order function
# This should be bulk process
# --------------------------------


def generate_orders(instrument, side, quantity, price):
    orders = []
    for exchange in exchanges:
        print(f"Generating {side} order on {exchange} for {
            instrument} at price {price} and quantity {quantity}")

        orders.append({
            "globalInstrumentCd": instrument,
            "exchange": exchange,
            "orderType": "LIMIT",
            "direction": side,
            "timeInForce": "GTC",  # Good Till Canceled
            "amount": quantity,
            "price": price
        })

    return orders


@handleAPIException(max_tries, retry_delay)
def place_orders(flexfills_api, orders):
    # Log that we're about to send the order to the exchange
    print(f"Sending orders...")

    # Direct synchronous API call (no await needed)
    order_responses = flexfills_api.create_order(orders)

    for order_response in order_responses:
        if order_response.get('event') == 'GET':
            print(f"Order created successfully: {order_response}")
            logging.info(f"Order created successfully: {order_response}")
            # active_orders.remove(order_data)
        else:
            print(f"Failed to create order: {order_response}")
            logging.warning(f"Failed to create order: {order_response}")


# --------------------------------
# Cancel order function
# This should be bulk process
# --------------------------------


@handleAPIException(max_tries, retry_delay)
def cancel_orders(flexfills_api, order_datas):
    # Log that we're about to send the order to the exchange
    print(f"Cancelling orders...")

    # Direct synchronous API call (no await needed)
    order_responses = flexfills_api.cancel_order(order_datas)

    for order_response in order_responses:
        # Handle the ACK response
        if order_response.get('event') == 'GET':
            print(f"Order cancelled successfully: {order_response}")
            logging.info(f"Order cancelled successfully: {order_response}")

            # active_orders.remove(order_data)
        else:
            print(f"Failed to cancel order: {order_response}")
            logging.warning(f"Failed to cancel order: {order_response}")


# --------------------------------
# Get balances
# This should be bulk process
# --------------------------------


@handleAPIException(max_tries, retry_delay)
def check_balances(flexfills_api, currencies):
    print("Checking balances for currencies:", currencies)
    logging.info("Checking balances for currencies:", currencies)

    # Send the subscription request
    balance_response = flexfills_api.get_balance(currencies)

    # Check if the response has the correct structure
    if 'data' in balance_response:
        print(f"[BALANCE] Balances received: {balance_response['data']}")
        logging.info(f"[BALANCE] Balances received: {
                     balance_response['data']}")

        # Iterate through the data and print the balance information
        balances = balance_response.get('data', [])

        first_balance = next(balance for balance in balances if balance.get(
            'currencyCode') == currencies[0])

        if first_balance:
            return first_balance.get('balance') > 0
        else:
            logging.error(
                f"Could not find balance data for {currencies[0]}")
            raise Exception(
                f"Could not find balance data for {currencies[0]}")

    else:
        logging.error("Balance data is empty")
        raise Exception("Balance data is empty")


# --------------------------------
# Check Order Books
# This should be bulk process
# --------------------------------


def get_order_books_stream(resp):
    print("Checking Order Books data:")
    print(resp)


@handleAPIException(max_tries, retry_delay)
def check_order_books(flexfills_api, pair):
    print("Checking Order Books of ", pair)

    # Send the subscription request
    flexfills_api.subscribe_order_books([pair], get_order_books_stream)


# --------------------------------------------------------------------
# Manually implement get_active_orders to query the active orders
# This should be bulk process
# --------------------------------------------------------------------


@handleAPIException(max_tries, retry_delay)
def get_active_orders(flexfills_api):
    active_orders = []

    print(f"Retrieving active orders ...")
    logging.info("Retrieving active orders ...")

    # Send the request manually to retrieve active orders
    active_orders_response = flexfills_api.get_open_orders_list([pair])

    # Check and log the response
    if 'data' in active_orders_response:
        print(f"Active Orders:")
        active_orders_data = active_orders_response.get('data', [])
        for order in active_orders_data:
            print(f"* Order ID: {order.get('clientOrderId')}, Price: {
                order.get('price')}, Amount: {order.get('amount')}")
            logging.info(f"* Order ID: {order.get('clientOrderId')}, Price: {
                order.get('price')}, Amount: {order.get('amount')}")

            active_orders.append(order)
    else:
        print(f"No active orders found: {active_orders_response}")
        logging.error(f"No active orders found: {active_orders_response}")

    return active_orders


# --------------------------------------------
# Monitor suggested prices and place orders
# --------------------------------------------


def monitor_and_trade(flexfills_api, quantity):
    while True:
        # Load buy and sell suggestions from the JSON file
        suggested_buy, suggested_sell = load_cluster_data()

        # Check balances
        is_sell = check_balances(flexfills_api, pair.split('/'))

        order_datas = []

        if is_sell == False and suggested_buy is not None:
            print(f"[DEBUG] Suggested Buy Price: {suggested_buy}")
            logging.debug(f"[DEBUG] Suggested Buy Price: {suggested_buy}")

            # Place buy orders on all exchanges
            orders = generate_orders(pair, "BUY", quantity, suggested_buy)
            order_datas.extend(orders)

        if is_sell and suggested_sell is not None:
            print(f"[DEBUG] Suggested Sell Price: {suggested_sell}")
            logging.debug(f"[DEBUG] Suggested Sell Price: {suggested_sell}")

            # Place sell orders on all exchanges
            orders = generate_orders(
                pair, "SELL", quantity, suggested_sell)
            order_datas.extend(orders)

        place_orders(flexfills_api, order_datas)

        # Wait for TTL and check if the order was filled or needs to be canceled
        time.sleep(TTL)

        # Check active orders
        active_orders = get_active_orders(flexfills_api)

        # Check order books
        # check_order_books(flexfills_api, pair)

        # Cancel unfilled orders and clean up active_orders list
        cancel_orders(flexfills_api, active_orders)


# ----------------------------------------
# Main function to run the application
# ----------------------------------------


def main():
    global flexfills_api

    # Login to Flexfills API
    login_flexfills()

    # Start monitoring and trading with suggested prices
    monitor_and_trade(flexfills_api, quantity)


# Run the main function using nest_asyncio.apply()
if __name__ == "__main__":
    main()
