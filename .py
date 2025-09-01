import requests

url = "https://booking-com.p.rapidapi.com/v1/attractions/calendar"

querystring = {"attraction_id":"PRFZkGSVnM5d","currency":"AED","locale":"en-gb"}

headers = {
	"x-rapidapi-key": "4e260b8961msh2435cc7ba8e0b55p128f7cjsne80ee811c4fd",
	"x-rapidapi-host": "booking-com.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())