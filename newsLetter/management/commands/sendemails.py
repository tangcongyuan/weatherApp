from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from newsLetter.models import Subscriber
import urllib2
import json

class Command(BaseCommand):
    help = 'Send email to all subscribers (from certain point of time)'

    def add_arguments(self, parser):
        # 'from_date' could be used to force send emails to subscribers who's been advertised before.
        # For now, we're just sending emails to subscribers who hasn't been advertised.
        parser.add_argument('from_date', nargs='?', type=str, help='Please input date in MMDDYYYY format.')

    def handle(self, *args, **options):
        try:
            from_date = datetime.strptime(options['from_date'], '%m%d%Y')
        except:
            from_date = None

        sendEmailFromDate(from_date)

        self.stdout.write(self.style.SUCCESS('Successfully sent emails to all subscribers'))

def sendEmailFromDate(from_date):
    subscribers = None
    avgTmpCache = {}
    currentTmpCache = {}
    weatherCache = {}
    if from_date == None:
        subscribers = Subscriber.objects.filter(advertisedDate = None)
    for subscriber in subscribers:
        try:
            subject = getSubject(subscriber.location, currentTmpCache, avgTmpCache, weatherCache)
            message = "This part is intentionally left blank."
            from_email = "tangcongyuan@gmail.com"

            send_mail(
                subject,
                message,
                from_email,
                [subscriber.email_address],
                fail_silently=False,
            )

            # Update advertisedDate accordingly
        except:
            # Error handling logic
            pass


def getSubject(location, currentTmpCache, avgTmpCache, weatherCache):
    try:
        if getCurrentTmp(location, currentTmpCache) - getAvgTmp(location, avgTmpCache) > 5:
            return "It's nice out! Enjoy a discount on us."
        elif getCurrentWeather(location, weatherCache) == "Rain":
            return "Not so nice out? That's okay, enjoy a discount on us."
        elif getCurrentTmp(location, currentTmpCache) - getAvgTmp(location, avgTmpCache) < -5:
            return "Not so nice out? That's okay, enjoy a discount on us."
    except:
        raise Exception

    return "Enjoy a discount on us."

def getCurrentTmp(location, currentTmpCache):
    if currentTmpCache.get(location) != None:
        return currentTmpCache[location]
    else:
        URL = "http://api.wunderground.com/api/e72a9ce05ccca20e/conditions/q/{0}/{1}.json"
        state = location.split(',')[1].strip()
        city = location.split(',')[0].strip()

        f = urllib2.urlopen(URL.format(state, city))
        json_string = f.read()
        parsed_json = json.loads(json_string)
        try:
            temp_f = parsed_json['current_observation']['temp_f']
            currentTmpCache[location] = temp_f
        except:
            raise Exception
        finally:
            f.close()

        return temp_f

def getAvgTmp(location, avgTmpCache):
    if avgTmpCache.get(location) != None:
        return avgTmpCache[location]
    else:
        URL = "http://api.wunderground.com/api/e72a9ce05ccca20e/almanac/q/{0}/{1}.json"
        state = location.split(',')[1].strip()
        city = location.split(',')[0].strip()

        f = urllib2.urlopen(URL.format(state, city))
        json_string = f.read()
        parsed_json = json.loads(json_string)
        try:
            temp_avg = ((float)(parsed_json['almanac']['temp_low']['normal']['F']) + (float)(parsed_json['almanac']['temp_high']['normal']['F']))/2
            avgTmpCache[location] = temp_avg
        except:
            raise Exception
        finally:
            f.close()

        return temp_avg

def getCurrentWeather(location, weatherCache):
    if weatherCache.get(location) != None:
        return weatherCache[location]
    else:
        URL = "http://api.wunderground.com/api/e72a9ce05ccca20e/conditions/q/{0}/{1}.json"
        state = location.split(',')[1].strip()
        city = location.split(',')[0].strip()

        f = urllib2.urlopen(URL.format(state, city))
        json_string = f.read()
        parsed_json = json.loads(json_string)
        try:
            weather = str(parsed_json['current_observation']['weather'])
            weatherCache[location] = weather
        except:
            raise Exception
        finally:
            f.close()

        return weather
