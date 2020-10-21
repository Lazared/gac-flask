import requests

r = requests.get("https://anthropologistics.com")
print(r.status_code)
print(r.ok)
