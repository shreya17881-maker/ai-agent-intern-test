from app.order_tools import lookup_order


test_ids = [
    "ORD-1007",
    "ord-1007",
    " ORD-1007 ",
    "ORD-999999",
    "hello"
]


for order_id in test_ids:

    print("\n==============================")
    print("LOOKUP:", repr(order_id))
    print("==============================")

    result = lookup_order(order_id)

    print(result)
