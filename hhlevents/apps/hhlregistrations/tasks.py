# cron tasks

from .models import MessisEvent
from happenings.models import Location
import json, requests
from datetime import datetime
from pytz import timezone
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


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
    
    
    # Create or update locations, note 255 char limits
    locations = serialized['locations']
    for loc in locations.values():
        try:
            this_location = Location.objects.get(name = loc['location_name'][:255])
            this_location.address_line_1 = loc['location_address'][:255]
            this_location.city           = loc['location_town'][:255]
            this_location.save()
        except ObjectDoesNotExist:
            this_location = Location.objects.create(name           = loc['location_name'][:255],
                                                    address_line_1 = loc['location_address'][:255],
                                                    city           = loc['location_town'][:255])
            this_location.save()
    
    # Create or update (only) upcoming events
    for ev in serialized['events']:
        cev = MessisEvent.objects.filter(messis_slug = ev['slug'])
        
        if not cev:
            m_event = MessisEvent()
        else:
            m_event = cev[0]
        
        #for loc in locations:
        #   print(ev['location_id'])
        #   print(dir(loc))
        #   try:
        #      m_location = loc[ev['location_id']][0]
        #      print(dir(m_location))
        #      m_event.set_location(m_location['location_name'],
        #                           m_location['location_address'],
        #                           m_location['location_town'],
        #                           m_location['latitude'],
        #                           m_location['longitude'])
        #   except:
        #      # KeyError etc.
        #      continue
                
        m_event.set_title(ev['event_name'])
        
        concat_start_time = ev['event_start_date']+" "+ev['event_start_time']
        concat_end_time = ev['event_end_date']+" "+ev['event_end_time']
        tz = timezone('Europe/Helsinki')
        
        m_event.set_start(tz.localize(datetime.strptime(concat_start_time, '%Y-%m-%d %H:%M:%S') ) )
        m_event.set_end(tz.localize(datetime.strptime(concat_end_time, '%Y-%m-%d %H:%M:%S') ) )
        
        m_event.set_content(ev['post_content'], ev['image_url'])
        m_event.save(ev['slug'])
        

        
        #if not cev:
        #    DownloadMessisEvent( ev['slug'],
        #                         ev['event_name'],
        #                         ev['event_start_date'],
        #                         ev['event_start_time'],
        #                         ev['event_end_date'],
        #                         ev['event_end_time'],
        #                         ev['post_content'],
        #                         ev['image_url'])
        #elif cev[0]:
        #    UpdateMessisEvent(   cev[0],
        #                         ev['event_name'],
        #                         ev['event_start_date'],
        #                         ev['event_start_time'],
        #                         ev['event_end_date'],
        #                         ev['event_end_time'],
        #                         ev['post_content'],
        #                         ev['image_url'])


#def DownloadMessisEvent(slug, event_name, start_date, start_time, end_date, end_time, description, image):
#    new_event = MessisEvent()
#    new_event.set_title(event_name)
#    
#    concat_start_time = start_date+" "+start_time
#    concat_end_time = end_date+" "+end_time
#    tz = timezone('Europe/Helsinki')
#    
#    new_event.set_start(tz.localize(datetime.strptime(concat_start_time, '%Y-%m-%d %H:%M:%S') ) )
#    new_event.set_end(tz.localize(datetime.strptime(concat_end_time, '%Y-%m-%d %H:%M:%S') ) )
#    
#    new_event.set_content(description, image)
#    new_event.save(slug)
#
#
#def UpdateMessisEvent(event_obj, event_name, start_date, start_time, end_date, end_time, description, image):
#    event_obj.set_title(event_name)
#    
#    concat_start_time = start_date+" "+start_time
#    concat_end_time = end_date+" "+end_time
#    tz = timezone('Europe/Helsinki')
#    
#    event_obj.set_start(tz.localize(datetime.strptime(concat_start_time, '%Y-%m-%d %H:%M:%S') ) )
#    event_obj.set_end(tz.localize(datetime.strptime(concat_end_time, '%Y-%m-%d %H:%M:%S') ) )
#    event_obj.set_content(description, image)
#    
#    event_obj.save()

