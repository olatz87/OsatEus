from django import template
from txantiloiak.models import Espezialitatea,Atala,Txostena,EdukiaAtala,EdukiaAzpiatala,Azpiatala


register = template.Library()


@register.filter()
def hautazkoaChecked(value):
    if not value:
        return "checked disabled"
    elif value == "check":
        return "checked"
    else:
        return ""
    
@register.filter()
def hautazkoaCollapse(value):
    if not value or value == "check":
        return "display:block"
    else:
        return "display:none"

@register.filter()
def diagGorriz(value):
    if value.startswith('Diagnostiko'):
        return "diag"
    else:
        return "atal_lab"


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.simple_tag
def get_eduk_atala(txosten_id,atal_id):
    obj = EdukiaAtala.objects.filter(txostena=int(txosten_id),atala=int(atal_id))[0]
    return obj.testua

@register.simple_tag
def get_eduk_azpiatala(txosten_id,azpiatal_id,atal_id):
    edAt = EdukiaAtala.objects.get(txostena=int(txosten_id),atala=int(atal_id))
    obj = EdukiaAzpiatala.objects.filter(goiEdukia=int(edAt.id),azpiatala=int(azpiatal_id))
    if obj:
        return obj[0].testua
    else:
        default = Azpiatala.objects.get(pk = int(azpiatal_id))
        return default.testua

@register.simple_tag
def get_gord_azpiatala(txosten_id,azpiatal_id,atal_id):
    edAt = EdukiaAtala.objects.get(txostena=int(txosten_id),atala=int(atal_id))
    obj = EdukiaAzpiatala.objects.filter(goiEdukia=int(edAt.id),azpiatala=int(azpiatal_id))
    if obj:
        return "check"
    else:
        return True
