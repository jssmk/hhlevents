# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.db import models
from django_markdown.admin import MarkdownModelAdmin, AdminMarkdownWidget
from django_markdown.models import MarkdownField
from happenings.models import Event as HappeningsEvent
from happenings.admin import EventAdmin as HappeningsEventAdmin
from happenings.admin import CancellationInline
from django.utils.translation import ugettext as _

from .models import MessisEvent

from .models import Event, Person, Registration

class EventAdmin(HappeningsEventAdmin):
    fieldsets = (
        (None, {
            'fields': ('start_date', 'end_date', 'all_day', 'repeat',
                       'end_repeat', 'title', 'description',
                       'created_by', 'extra_url', 'gforms_url', 'image',
                       )
        }),
        ('Location', {
            'fields': ('location',)
        }),
        ('Registrations', {
            'fields': ( 'registration_requirement', 'max_registrations', 'close_registrations',
                        'event_cost', 'materials_cost', 'materials_mandatory',
                        'payment_due', 'hide_join_checkbox',
                       )
        }),
        ('Category', {
            'classes': ('collapse',),
            'fields': ('categories',)
        }),
        ('Tag', {
            'classes': ('collapse',),
            'fields': ('tags',)
        }),
        ('Color', {
            'classes': ('collapse',),
            'fields': (
                ('background_color', 'background_color_custom'),
                ('font_color', 'font_color_custom'),
            )
        }),
    )
    formfield_overrides = {
        MarkdownField: {'widget': AdminMarkdownWidget},
        models.TextField: {'widget': AdminMarkdownWidget},
    }
    list_display = ('title', 'start_date', 'duration', 'repeat', 'registration_requirement', 'formLink')
    list_filter = ['start_date']
    search_fields = ['title']
    date_hierarchy = 'start_date'
    inlines = [CancellationInline]

class MessisEventAdmin(HappeningsEventAdmin):
    # prevent users from adding new Messis Events through admin interface
    # messis events should be added at www.messis.fi event manager
    def has_add_permission(self, request):
        return False
    readonly_fields = (
        #(None, {
        #    'fields': (
                       'messis_slug',
                       'start_date', 'end_date', 'all_day', 'repeat',
                       'end_repeat', 'title', 'description',
                       'created_by', 'extra_url', 'image',
        #               )
        #}),
    )
    
    fieldsets = (
        ('Messis', {
        	'fields': ('messis_slug', 'start_date', 'end_date',
        	           'all_day', 'repeat',
                       'end_repeat', 'title', 'description',
                       'created_by', 'extra_url', 'image')
        }),
        #(None, {
        #    'fields': ('start_date', 'end_date', 'all_day', 'repeat',
        #               'end_repeat', 'title', 'description',
        #              'created_by', 'extra_url', 'image',
        #               )
        #}),
        ('Location', {
            'fields': ('location',)
        }),
        ('Registrations', {
            'fields': ( 'registration_requirement', 'max_registrations', 'close_registrations',
                        'event_cost', 'materials_cost', 'materials_mandatory',
                        'payment_due',
                       )
        }),
        ('Category', {
            'classes': ('collapse',),
            'fields': ('categories',)
        }),
        ('Tag', {
            'classes': ('collapse',),
            'fields': ('tags',)
        }),
        ('Color', {
            'classes': ('collapse',),
            'fields': (
                ('background_color', 'background_color_custom'),
                ('font_color', 'font_color_custom'),
            )
        }),
    )
    formfield_overrides = {
        MarkdownField: {'widget': AdminMarkdownWidget},
        models.TextField: {'widget': AdminMarkdownWidget},
    }
    list_display = ('title', 'start_date', 'duration','formLink','messisLink')
    list_filter = ['start_date']
    search_fields = ['title']
    date_hierarchy = 'start_date'
    inlines = [CancellationInline]


class RegistrationAdmin(admin.ModelAdmin):
    search_fields = ['event__title', 'person__first_name', 'person__last_name', 'person__email']
    list_filter = ['state']
    list_display = ('person','event', 'state')


# Remove the happenings event admin
admin.site.unregister(HappeningsEvent)
# And use our own
admin.site.register(Event, EventAdmin)
admin.site.register(MessisEvent, MessisEventAdmin)
admin.site.register(Person)
admin.site.register(Registration, RegistrationAdmin)   
