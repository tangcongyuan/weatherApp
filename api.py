import urllib2
import json

location = "Auburn, AL"
URL = "http://api.wunderground.com/api/e72a9ce05ccca20e/almanac/q/{0}/{1}.json"
state = location.split(',')[1].strip()
city = location.split(',')[0].strip()
print URL.format(state, city)
f = urllib2.urlopen(URL.format(state, city))
json_string = f.read()
parsed_json = json.loads(json_string)
print parsed_json['almanac']['temp_low']['normal']['F']
print parsed_json['almanac']['temp_high']['normal']['F']
# temp_f = parsed_json['current_observation']['temp_f']
# print "Current temperature in %s is: %s" % (location, temp_f)
f.close()



URL = "http://api.wunderground.com/api/e72a9ce05ccca20e/conditions/q/{0}/{1}.json"
state = location.split(',')[1].strip()
city = location.split(',')[0].strip()
print URL.format(state, city)
f = urllib2.urlopen(URL.format(state, city))
json_string = f.read()
parsed_json = json.loads(json_string)
print parsed_json['current_observation']['temp_f']
print parsed_json['current_observation']['weather']
# temp_f = parsed_json['current_observation']['temp_f']
# print "Current temperature in %s is: %s" % (location, temp_f)
f.close()
