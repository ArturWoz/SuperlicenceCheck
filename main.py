from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
from re import sub


def kebab(s):
    return '-'.join(
        sub(r"(\s|_|-)+"," ",
        sub(r"[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+",
        lambda mo: ' ' + mo.group(0).lower(), s)).split())


with open("points.json", encoding='utf-8-sig') as json_file:
    points_list = json.load(json_file)

with open("series.json", encoding='utf-8-sig') as json_file:
    series_list = json.load(json_file)

print("Enter driver name: ")
name = input()
url = "https://www.driverdb.com/drivers/" + kebab(name)

page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")
year = soup.find_all("div", {"class": "TableRow_col1__oD_pW"})
series = soup.find_all("div", {"class": "TableRow_col2__y1FvI"})
position = soup.find_all("div", {"class": "TableRow_col5__ZKCzs"})
table = []
for y, s, p in zip(year, series, position):
    try:
        if int(y.string) in [2023, 2022, 2021, 2020]:
            table.append([y.string, s.string, p.string])
    except ValueError:
        pass
    except TypeError:
        pass

counted = {
        "2023": {
            "series": "",
            "points": 0
        },
        "2022": {
            "series": "",
            "points": 0
        },
        "2021": {
            "series": "",
            "points": 0
        },
        "2020": {
            "series": "",
            "points": 0
        }
}

# if table[0][1] == 'FIA Formula 1 World Championship':
#     print("Is F1 Driver!")

for el in table:
    if el[1] == 'FIA Formula 1 World Championship':
        print("Was F1 Driver!")
    current_points = 0
    try:
        current_points = points_list[series_list[el[1]]][el[2]]
    except:
        pass
    if current_points > counted[el[0]]["points"]:
        counted[el[0]]["series"] = el[1]
        counted[el[0]]["points"] = current_points

#print(counted)

pts = [counted["2023"]["points"], counted["2022"]["points"], counted["2021"]["points"], counted["2020"]["points"]]
pts.remove(min(pts))
points = sum(pts)
license_status = points > 40

print("Points: " + str(points) + "/40")
if license_status:
    print("Eligible for superlicense")
else:
    print("Ineligible for superlicense")