import requests
from bs4 import BeautifulSoup

response = requests.get("https://www.aad.org/public/diseases/acne/causes/acne-causes")
soup = BeautifulSoup(response.text, "html.parser")

main = soup.find("main")
if not main:
    raise Exception("No main tag found")
content = main.find_all(lambda tag: tag.name != "section")
# print all text in content
print("\n".join(c.text for c in content))
