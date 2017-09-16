from requests import get
from bs4 import BeautifulSoup
import pandas as pd

url = 'http://forecast.weather.gov/MapClick.php?lat=47.6036&lon=-122.3294'

page = get(url)


soup = BeautifulSoup(page.content, 'html.parser')

seven_day = soup.find(id='seven-day-forecast-container')

forecast_items = seven_day.find_all(class_='forecast-tombstone')


period = [pt.get_text() for pt in seven_day.select(".forecast-tombstone .period-name")]
short_desc = [sd.get_text() for sd in seven_day.select(".forecast-tombstone .short-desc")]
temp = [temp.get_text() for temp in seven_day.select(".forecast-tombstone .temp")]


# s=  [t.split(" ") for t in temp]
# print s[0][1]
#print period, short_desc, temp

weather = pd.DataFrame(
	{
	"Description":short_desc,
	"Period":period,
	"Temperature":temp
	})

print weather
temp_nums = weather["Temperature"].str.extract("(?P<temp_num>\d+)", expand=False)
weather["temp_num"] = temp_nums.astype('int')

print 'Mean of  weather over 7 day : ' + str(weather['temp_num'].mean())

is_night = weather["Temperature"].str.contains("Low")
weather["is_night"] = is_night

print weather[is_night]

def convert_f_2_c(temp):
	return str((temp - 32) * 5/9)+ u'\xb0C' 

