from django import template
register = template.Library()


def addclasses(value, arg):
    return value
    # return value.as_widget(attrs={'class': arg})

def filtro_menu(value):
    return value.replace("_"," ")

register.filter(filtro_menu)
register.filter(addclasses)