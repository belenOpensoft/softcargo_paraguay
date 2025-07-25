from django import template
register = template.Library()


def addclasses(value, arg):
    return value
    # return value.as_widget(attrs={'class': arg})

def filtro_menu(value):
    return value.replace("_"," ")


@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})

register.filter(filtro_menu)
register.filter(addclasses)
register.filter(add_class)