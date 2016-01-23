import datetime
import uuid
from glob import glob
from os.path import basename
from django.db import models
from django_markdown.models import MarkdownField
from django_markdown.fields import MarkdownFormField
from happenings.models import Event as HappeningsEvent
from happenings.utils.next_event import get_next_event
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _ # _lazy required
from django.utils.functional import lazy
from datetime import date
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Always get a fresh list of png-images from static/img/
def IMAGES():
    return [ ("/static/img/"+basename(x),basename(x)) for x in glob(settings.HHLREGISTRATIONS_ROOT+"/static/img/*.png") ]

class AbstractEvent(HappeningsEvent):
    REG_REQUIREMENT = ( ('RQ', 'Required'),
                        ('OP', 'Optional'),
                        ('NO', 'None'),
                        ('HA', 'Handled by the organiser' ))
    
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    extra_url = models.URLField(blank=True)
    registration_requirement = models.CharField(max_length=2, choices=REG_REQUIREMENT, default='NO')
    max_registrations = models.PositiveSmallIntegerField(default=None)
    close_registrations = models.DateTimeField(blank=True, null=True)
    payment_due = models.DateTimeField(blank=True, null=True)
    event_cost = models.PositiveSmallIntegerField(default=None)
    materials_cost = models.PositiveSmallIntegerField(default=None)
    materials_mandatory = models.BooleanField(default=False)
    image = models.CharField(max_length=100, choices=lazy(IMAGES, tuple)())  # 100 liian vähän?
    class Meta:
        abstract = True
    
    def classname(self):
        return self.__class__.__name__
    def isPast(self):
        if self.repeats('NEVER') and timezone.now() > self.end_date:
            return True
        elif not self.repeats('NEVER') and self.end_repeat < self.end_date.date():
            # Error state, handle somehow differently later on
            return False
        elif not self.repeats('NEVER') and self.end_repeat <= timezone.now().date():
            return True
        return False
    def isCancelled(self):
        if self.check_if_cancelled(timezone.now()):
            return True
        return False
    def isRepeating(self):
        if self.repeats('NEVER'):
            return False
        return True
    def getNextEvent(self): # next occurrence of this happening
        if self.repeats('NEVER'):
            return self.start_date
        elif self.end_repeat > timezone.now().date():
            next = get_next_event([self], timezone.now())
            pvm = date(next[0], next[1], next[2])
            return pvm
        # in case repetition has ended, show nothing
        return None


class Event(AbstractEvent):
    # Options for registration requirements, also option for not accepting registrations

    gforms_url = models.URLField(blank=True)
    hide_join_checkbox = models.BooleanField(default=False) # pois!
    
    def formLink(self):
        if self.registration_requirement in ('RQ', 'OP'):
            return  '<a href="' + reverse('registrations:register', args=[str(self.id)]) + '">Event page and form</a>'
        return '<a href="' + reverse('registrations:register', args=[str(self.id)]) + '">Event page</a>'
    formLink.allow_tags = True
    formLink.short_description = _('Event page and form')
    
    def getParticipants(self):
        return Registration.objects.all().filter(event = self.event).order_by('state', 'registered')
    
    def getStatsHTML(self):
        n_AC = Registration.objects.all().filter(event = self.event).filter(state = 'AC').count()
        n_CC = Registration.objects.all().filter(event = self.event).filter(state = 'CC').count()
        n_CP = Registration.objects.all().filter(event = self.event).filter(state = 'CP').count()        
        n_WL = Registration.objects.all().filter(event = self.event).filter(state = 'WL').count()
        n_CA = Registration.objects.all().filter(event = self.event).filter(state = 'CA').count()
        n_CR = Registration.objects.all().filter(event = self.event).filter(state = 'CR').count()
        n_WB = Registration.objects.all().filter(event = self.event).filter(state = 'WB').count()
        return u'Assumed coming (AC): %s<br/>Confirmed coming (CC): %s</br>Confirmed, pre-payments OK (CP): %s<br/>Waiting-list (WL): %s<br/>Cancelled (CA): %s</br>Cancelled, refunded (CR): %s<br/>Waiting-list (due to ban) (WB): %s' % (n_AC, n_CC, n_CP, n_WL, n_CA, n_CR, n_WB)
    
    class Meta:
        ordering = ["-end_date"]
        verbose_name = _('event')
        verbose_name_plural = _('events')
        # abstract = True # tämä vaaditaan seuraavaksi!
        

class MessisEvent(AbstractEvent):
    messis_slug = models.CharField(max_length=255)#, editable=False)#, primary_key=True) # pituus maksimi??
    #update_hash = models.CharField(max_length=255)
    #aikatiedot, onko jokin field-tyyppi jota ei voi muokata??
    
    #repeat = 'NEVER' #vakio
    class Meta:
        ordering = ["-end_date"]
        verbose_name = _('Messis event')
        verbose_name_plural = _('Messis events')
    

    def __init__(self, *args, **kwargs):
        super(MessisEvent, self).__init__(*args, **kwargs)
        try:
            messis_user = User.objects.get(username = 'Messis')
        except ObjectDoesNotExist:
            messis_user = User.objects.create_user('Messis', '', uuid.uuid4())
            messis_user.save()
        self.created_by = messis_user
    
    def save(self, new_slug=""):
        if new_slug != "":
            self.messis_slug = new_slug
            self.extra_url="http://messis.fi/fi/tapahtumat/"+new_slug
        super(MessisEvent, self).save()
        
    def set_title(self, new_title):
        self.title = new_title
    def set_start(self, new_date):
        self.start_date = new_date
    def set_end(self, new_date):
        self.end_date = new_date
    def set_content(self, new_desc, new_img):
        self.description = new_desc
        self.image = new_img # tallentuu kaikesta huolimatta dataan ja näkyy esim. /register/issä
    
    def messisLink(self):
        tag = self.messis_slug
        if self.extra_url != "":
            tag = '<a href="' + self.extra_url + '">'+self.messis_slug+'</a>'
        return tag
    messisLink.allow_tags = True
    messisLink.short_description = _('Event on www.messis.fi')
    
#    def __init__(self):
#        self.event = Event()
#        self.event.repeat = 'NEVER' # voi olla että ei tarvi, default on Never
#    def formLink(self):
#        self.event.formLink()
#    def getNextEvent(self):
#        return self.start_date # never repeats
#    def isRepeating(self):
#        return False # never repats
#    def isCancelled(self):
#        self.event.isCancelled()
#    def isPast(self):
#        if timezone.now() > self.end_date:
#            return True
#        return False
#    def getStatsHTML(self):
#        self.event.getStatsHTML()
#    def getParticipants(self):
#        self.event.getParticipants()
 



class Person(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    banned = models.DateTimeField(blank=True, null=True, verbose_name=u'Automatically put to waiting list')

    def __unicode__(self):
        return self.formatted_email

    @property
    def formatted_email(self):
        return u'%s, %s <%s>' % (self.last_name, self.first_name, self.email)
    
    class Meta:
        ordering = ["last_name"]
        verbose_name = _('participant')
        verbose_name_plural = _('participants')

class Registration(models.Model):
    STATES = (
        ( 'AC', 'Assumed coming'),
        ( 'CC', 'Confirmed coming'),
        ( 'CP', 'Confirmed, pre-payments OK'),
        ( 'WL', 'Waiting-list'),
        ( 'CA', 'Cancelled'),
        ( 'CR', 'Cancelled, refunded'),        
        ( 'WB', 'Waiting-list (due to ban)'),
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    paid = models.DateTimeField(blank=True, null=True)
    event = models.ForeignKey(Event, related_name='persons', on_delete=models.CASCADE)
    person = models.ForeignKey(Person, related_name='events', on_delete=models.CASCADE)
    registered = models.DateTimeField(default=datetime.datetime.now)
    cancelled = models.DateTimeField(blank=True, null=True)
    state = models.CharField(max_length=2, choices=STATES)
    wants_materials = models.BooleanField(default=False)
#   ajankohta milloin ilmoittautui? jonottaminen?

    class Meta:
        unique_together = (('event', 'person'),)
        ordering = ["event"]
        verbose_name = _('registration')
        verbose_name_plural = _('registration')
    
    def __unicode__(self):
        return u'%s, %s <%s> (%s)' % (self.person.last_name, self.person.first_name, self.person.email, self.state)
