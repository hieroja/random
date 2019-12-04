"""
A terminal based program that is used to calculate how much money one can make
with a method called "Bones to peaches" in Old School RuneScape.
It uses GE-Tracke's API for live price data.

An API-key is necessary for using this program. You can get one from GE-Trackers
site by signing up or in some cases, I can borrow mine if I know you IRL.

Author: Jere Liimatainen

"""
import requests

# Insert your API-key here.
API_KEY = ""

headers = {
"Accept": "application/x.getracker.v1+json",
"Authorization": "Bearer " + API_KEY,
}
url = "https://www.ge-tracker.com/api/items/multi/8015,561,1761"
response = requests.request("GET", url, headers=headers)
dct = response.json()

data = {}

for i in range(len(dct['data'])):
    data[dct['data'][i]['name']] = dct['data'][i]

b2b = data["Bones to peaches"]["overall"]
soft_clay = data["Soft clay"]["overall"]
nature_rune = data["Nature rune"]["overall"]


inv_time = 60 # How long it takes for one inventory to complete.
inv_space = 24 # Inventory space for soft clay.
servant_time = 7.2 # How long it takes for the servant to refill supplies.

profit_per_inv = 24 * b2b - (24 * soft_clay + 48 * nature_rune )
inv_per_hour = 3600 / (inv_time + servant_time)
servant_cost = (inv_per_hour / 8) * 10000
profit_per_hour = inv_per_hour * profit_per_inv - servant_cost

print(profit_per_hour)