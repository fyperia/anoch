from django import template
register = template.Library()


@register.simple_tag
def is_active_chapter(chapter, path):
    return chapter.is_active(path)
