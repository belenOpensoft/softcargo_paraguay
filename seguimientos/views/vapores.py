from mantenimientos.models import Vapores
from seguimientos.models import Seguimiento


def comprobar_vapores(request):
    try:
        seguimientos = Seguimiento.objects.all()
        for x in seguimientos:
            if x.vapor is not None and len(x.vapor) > 0:
                vapor = Vapores.objects.filter(nombre=x.vapor)
                if vapor.count() > 0:
                    x.vaporcli = vapor[0].id
                    x.save()
    except Exception as e:
        print(e)