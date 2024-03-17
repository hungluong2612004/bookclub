from django.template import Library;register = Library()

@register.filter(name='times') 
def times(number):
    if (number == None):
        return range(0)
    else:
        k = int(round(number))
        return range(k)

@register.filter(name='times_left') 
def times_left(number):
    if (number == None):
        return range(5)
    else:
        k = 5 - int(round(number))
        return range(k)