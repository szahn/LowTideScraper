import requests 
import re
from bs4 import BeautifulSoup
import soupsieve as sv

cities = ["Half Moon Bay, California", "Huntington Beach", "Providence, Rhode Island", "Wrightsville Beach, North Carolina"]

def scrape(city):
  city_url_id = re.sub(r'[\s,]+', "-", city, 0)
  city_url = "https://www.tide-forecast.com/locations/" + city_url_id + "/tides/latest"
  r = requests.get(url = city_url)
  html = r.text
  soup = BeautifulSoup(html, 'html.parser')
  tr = sv.select(".tide-table > tr",  soup)

  curr_date = ""
  timeofday = ""

  for el in tr:
    dateInst = sv.select_one(".date", el)
    if dateInst != None:
      curr_date = dateInst.text.strip()

    tide_time = ""
    tide_time_inst = sv.select_one(".time", el)
    if tide_time_inst != None:
      tide_time = tide_time_inst.text.strip()
    
    timezone = ""
    timezone_inst = sv.select_one(".time-zone", el)
    if tide_time_inst != None:
      timezone = timezone_inst.text.strip()
    
    level = ""
    level_inst = sv.select_one(".level", el)
    if level_inst != None:
      level = level_inst.text.strip()
    

    tide_phase = ""
    tide_phase_inst = sv.select_one(".tide:last-child", el)
    if tide_phase_inst != None:
      tide_phase = tide_phase_inst.text.strip()
    else:
      timeofday_inst = sv.select_one("td:last-child", el)
      if timeofday_inst != None:
        timeofday_val = timeofday_inst.text.strip()
        if timeofday_val == "Sunrise":
          timeofday = timeofday_val
        elif timeofday_val == "Sunset":
          timeofday = timeofday_val
        else:
          timeofday = ""

    if tide_phase == "Low Tide" and (timeofday == "Sunrise" or timeofday == "Sunset"):
      print('{0} {1} {2} {3} {4}'.format(city, curr_date, tide_time, timezone, level))

for city in cities:
  scrape(city)

