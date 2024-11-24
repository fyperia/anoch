import re

from django import template
from django.template.defaultfilters import stringfilter

from rules_db.models import Effect

register = template.Library()


@register.simple_tag
def is_active_chapter(chapter, path):
    return chapter.is_active(path)


@register.filter
def get_dict_item(dictionary, key):
    return dictionary.get(key)


@register.filter(name='replace_tooltip')
@stringfilter
def replace_tooltip(value):
    new_string = value
    matches = re.finditer("@+[+[a-z]+:+[a-z]+]", value, re.IGNORECASE)
    for match in matches:
        if "status" in match.group():
            syntax = replace_status(match.group())
            new_string = value.replace(match.group(), syntax)
    return value.replace(value, new_string)


def replace_status(value):
    # value = "@[status:tripped]"
    status = re.search("(?<=:)[a-z]+", value, re.IGNORECASE).group()
    duration = ""
    try:
        obj = Effect.objects.get(name=status)
    except Effect.DoesNotExist:
        tooltip = ("Status not found. Please report this to the Webmaster using the 'Report a Problem' "
                   "link at the bottom of the page.")
    else:
        if obj.duration == -1:
            duration = " until the effect is cured"
        elif obj.duration < 60:
            duration = " for " + str(obj.duration) + " seconds"
        else:
            # convert seconds to minutes, and add an s if more than 1 minute
            duration = " for " + str(int(obj.duration / 60)) + " minute"
            if (obj.duration / 60) > 1:
                duration += "s"
        s = obj.description + " " + obj.mechanics
        tooltip = s.replace("@[duration]", duration)
    syntax = "<span class='hover_text'>" + status + "<span class='tooltip'>" + tooltip + "</span></span>"
    return syntax
