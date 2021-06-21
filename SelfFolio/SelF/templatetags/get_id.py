from django import template

register = template.Library()

@register.filter
def get_id(course):
    return course.id