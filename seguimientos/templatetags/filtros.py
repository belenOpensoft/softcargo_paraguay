from django import template
register = template.Library()


@register.filter(name='addclasses')
def addclasses(value, arg):
    return value
    # return value.as_widget(attrs={'class': arg})

