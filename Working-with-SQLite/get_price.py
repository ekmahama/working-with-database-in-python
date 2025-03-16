import requests
import datetime
import csv
coin_id = "ethereum"
currency = "usd"

# url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={currency}"

# data = requests.get(url).json()

# coin_price = data[coin_id][currency]

# print(f"{coin_id},{currency}, 1.0, 1, {datetime.datetime.now()}")


def import_investments(csv_file):
    with open(csv_file) as f:
        rdr = csv.reader(f, delimiter=",")
        rows = list(rdr)
        # sql = "INSERT INTO investments VALUES(?,?,?,?,?);"
        # cur.executemany(sql, rows)
        # database.commit()

        # print(f"Imported {len(rows)} investments from {csv_file}")

import_investments("investments.csv")