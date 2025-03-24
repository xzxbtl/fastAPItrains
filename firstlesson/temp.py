import json

FILE_PATH = r'C:\Users\xzxbt\PycharmProjects\FastAPITraining\pythonProject1\firstlesson\donations.json'
all_ids = []


def test(order_id):
    with open(FILE_PATH, 'r') as f:
        all_contacts = json.load(f)
        for user_name, dates in all_contacts.items():
            for date, messages in dates.items():
                for message in messages:
                    payment_id = message.get("id")
                    if payment_id == int(order_id):
                        return {user_name: {"date": date, "payment_ID": payment_id}}
    return "ERROR"


# Пример вызова функции
print(test("161527595"))
