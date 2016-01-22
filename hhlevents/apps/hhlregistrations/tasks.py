# cron tasks

from .models import MessisEvent
import json, requests
from datetime import datetime
from pytz import timezone
from django.conf import settings


def getUpcomingEventsURL():
    return 'http://messis.fi/fi/?json=messis/get_upcoming_events&owner='+settings.MESSIS_ID_NUM

def SyncMessis():
    try:
        r = requests.get(url=getUpcomingEventsURL(),
                         headers={'User-Agent': 'Mozilla/5.0'})
    except requests.exceptions.Timeout:
        return
    except requests.exceptions.RequestException as e:
        print(e)
        return
            
    json_text = r.text
    serialized = json.loads(json_text)
    
    for ev in serialized['events']:
        cev = MessisEvent.objects.filter(messis_slug = ev['slug'])
        if not cev:
            DownloadMessisEvent( ev['slug'],
                                 ev['event_name'],
                                 ev['event_start_date'],
                                 ev['event_start_time'],
                                 ev['event_end_date'],
                                 ev['event_end_time'],
                                 ev['post_content'],
                                 ev['image_url'])
        elif cev[0]:
            UpdateMessisEvent(   cev[0],
                                 ev['event_name'],
                                 ev['event_start_date'],
                                 ev['event_start_time'],
                                 ev['event_end_date'],
                                 ev['event_end_time'],
                                 ev['post_content'],
                                 ev['image_url'])


def DownloadMessisEvent(slug, event_name, start_date, start_time, end_date, end_time, description, image):
    new_event = MessisEvent()
    new_event.set_title(event_name)
    
    concat_start_time = start_date+" "+start_time
    concat_end_time = end_date+" "+end_time
    tz = timezone('Europe/Helsinki')
    
    new_event.set_start(tz.localize(datetime.strptime(concat_start_time, '%Y-%m-%d %H:%M:%S') ) )
    new_event.set_end(tz.localize(datetime.strptime(concat_end_time, '%Y-%m-%d %H:%M:%S') ) )
    
    new_event.set_content(description, image)
    new_event.save(slug)


def UpdateMessisEvent(event_obj, event_name, start_date, start_time, end_date, end_time, description, image):
    event_obj.set_title(event_name)
    
    concat_start_time = start_date+" "+start_time
    concat_end_time = end_date+" "+end_time
    tz = timezone('Europe/Helsinki')
    
    event_obj.set_start(tz.localize(datetime.strptime(concat_start_time, '%Y-%m-%d %H:%M:%S') ) )
    event_obj.set_end(tz.localize(datetime.strptime(concat_end_time, '%Y-%m-%d %H:%M:%S') ) )
    event_obj.set_content(description, image)
    event_obj.save()
