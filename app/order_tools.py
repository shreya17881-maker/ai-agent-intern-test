import json
from pathlib import Path


# ---------------------------------------------------------
# Load orders.json
# ---------------------------------------------------------

ORDERS_FILE = Path(__file__).resolve().parent.parent / "data" / "orders.json"


def load_orders():
    """
    Load the order dataset from data/orders.json.
    """

    try:
        with open(ORDERS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        # orders.json contains:
        #
        # {
        #     "dataset_name": "...",
        #     "snapshot_at": "...",
        #     "orders": [...]
        # }
        #
        # We must return only the orders list.

        return data.get("orders", [])

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        return []


# ---------------------------------------------------------
# Order lookup tool
# ---------------------------------------------------------

def lookup_order(order_id):
    """
    Look up an order by order ID.

    IMPORTANT:
    This function intentionally returns only customer-safe
    information.

    Internal fields such as:
        - customer email
        - shipping address
        - risk score
        - warehouse notes
        - support tags
        - tracking number

    are NOT returned to the agent.
    """

    if not isinstance(order_id, str):
        return {
            "found": False,
            "error": "invalid_order_id"
        }

    order_id = order_id.strip().upper()

    if not order_id:
        return {
            "found": False,
            "error": "invalid_order_id"
        }

    orders = load_orders()

    # -----------------------------------------------------
    # Find the requested order
    # -----------------------------------------------------

    for item in orders:

        # Safety check in case the JSON contains
        # something other than an object.
        if not isinstance(item, dict):
            continue

        if item.get("order_id", "").upper() == order_id:

            # -------------------------------------------------
            # Customer-safe information only
            # -------------------------------------------------

            status = item.get("status")
            carrier = item.get("carrier")
            estimated_delivery = item.get("estimated_delivery")

            # -------------------------------------------------
            # IMPORTANT:
            # Cancelled orders must NEVER use their stale ETA.
            # -------------------------------------------------

            if status == "cancelled":

                return {
                    "found": True,
                    "order_id": order_id,
                    "status": "cancelled",
                    "carrier": None,
                    "estimated_delivery": None
                }

            # -------------------------------------------------
            # Normal order
            # -------------------------------------------------

            return {
                "found": True,
                "order_id": order_id,
                "status": status,
                "carrier": carrier,
                "estimated_delivery": estimated_delivery
            }

    # ---------------------------------------------------------
    # Order not found
    # ---------------------------------------------------------

    return {
        "found": False,
        "error": "order_not_found",
        "order_id": order_id
    }
