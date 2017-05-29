from django import template

register = template.Library()


@register.filter()
def hautazkoaCollapse(value):
    if value:
        return "display: none"
    else:
        return ""
    
