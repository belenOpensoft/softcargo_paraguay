def rol_pestana(request):
    return {'rol_pestana': getattr(request, 'rol_pestana', None)}