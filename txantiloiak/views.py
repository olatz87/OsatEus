from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth import authenticate, login
from .models import Espezialitatea,Atala,Txostena,EdukiaAtala,EdukiaAzpiatala
from datetime import datetime
from django.contrib.auth.models import User
from subprocess import Popen, PIPE
import subprocess
from django.http import JsonResponse
#from django.forms.models import inlineformset_factory,modelformset_factory
#from .forms import EspezialitateaForm,EspezialitateaInlineForm

# Create your views here.
#from .analizatzailea_eu import *



class IndexView(generic.ListView):
    template_name = 'txantiloiak/index.html'
    context_object_name = 'espezialitateen_zerrenda'


    def get_queryset(self):
        """Return all the Espezialitateak."""
        return Espezialitatea.objects.order_by('izena')
        
    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args,**kwargs)
        context["egindako_txostenak"] = Txostena.objects.filter(egilea=self.request.user)
        return context


class EspezialitateaView(generic.DetailView):
    model = Espezialitatea
    template_name = 'txantiloiak/espezialitatea.html'

    
    def get_context_data(self,*args,**kwargs):
        context = super(EspezialitateaView, self).get_context_data(*args,**kwargs)
        
        txosList = Txostena.objects.filter(id=self.kwargs.get("txosten_id",None))
        if txosList:
            txos = txosList[0]
            context["txostena"] = txos
            if txos:
                for ed_atal in txos.edukiaatala_set.all():
                    context["atal"+str(ed_atal.atala.id)] = ed_atal.testua
                    if ed_atal.edukiaazpiatala_set.exists():
                        for ed_azpiatal in ed_atal.edukiaazpiatala_set.all():
                            context["azpiatal"+str(ed_azpiatal.azpiatala.id)] = ed_azpiatal.testua
        return context


def analizatzailea(request, param):
        print(request.GET['param']) 
        subprocesLortu = subprocess.Popen(['python3', '/sc01a4/users/aelorz003/KBP/osasunTxostenak/txantiloiak/analizatzailea_eu.py', request.GET['param']], stdout=PIPE, close_fds=True)
        analizatu = subprocesLortu.communicate()
        #print("1", analizatu)
        analizatu = analizatu[0].decode('utf-8')
        print("2", analizatu)
        return HttpResponse(analizatu)

def sct4text(request, param):
        subprocesLortu = subprocess.Popen(['python3', '/sc01a4/users/aelorz003/KBP/osasunTxostenak/txantiloiak/sct4text.py', '-f', request.GET['param'], '-l', 'eu'], stdout=PIPE, close_fds=True)
        fsn = subprocesLortu.communicate()
        fsn = fsn[0].decode('utf-8')
        print(fsn)
        return HttpResponse(fsn)


def gorde(request,espezialitatea_id):
    #import pdb; pdb.set_trace()
    if request.method == 'POST':
        momentuz_user = request.user
        p = get_object_or_404(Espezialitatea,pk=espezialitatea_id)
        t = Txostena(egilea = momentuz_user)
        t.save()
        atal_haut = request.POST.getlist('atalch')
        atalak = p.atala_set.all()
        azpiatal_hau = request.POST.getlist('azpich')
        #pdb.set_trace()
        for atal in atalak:
            if not atal.hautazkoa or atal.id in atal_haut:
                e = EdukiaAtala(txostena=t,atala=atal,testua=request.POST.get('testu'+str(atal.id)).strip())
                e.save()
                #import pdb; pdb.set_trace()
                for azp in atal.azpiatala_set.all():
                    id_lag = str(atal.id)+'_'+str(azp.id)
                    if not azp.hautazkoa or id_lag in azpiatal_hau:
                        ea = EdukiaAzpiatala(goiEdukia=e,azpiatala=azp,testua=request.POST.get('testu'+id_lag).strip())
                        ea.save()
                
        for azpi in request.POST.getlist('azpich'):
            a_id,az_id = azpi.split('_')
        return HttpResponseRedirect(reverse('txantiloiak:laburpena',args=(t.id,)))
    else:
        pass


def gordeAldatua(request,txostena_id):
    #import pdb; pdb.set_trace()
    if request.method == 'POST':
        t = get_object_or_404(Txostena,pk=txostena_id)
        atal_haut = request.POST.getlist('atalch')
        edukiatalak = t.edukiaatala_set.all()
        azpiatal_hau = request.POST.getlist('azpich')
        #pdb.set_trace()
        for e in edukiatalak:
            atal = e.atala
            if not atal.hautazkoa or atal.id in atal_haut:
                e.testua = request.POST.get('testu'+str(atal.id))
                #e = EdukiaAtala(txostena=t,atala=atal,testua=request.POST.get('testu'+str(atal.id)))
                e.save()
                #import pdb; pdb.set_trace()
                azp_aldatuak = set()
                for ea in e.edukiaazpiatala_set.all():
                    azp = ea.azpiatala
                    id_lag = str(atal.id)+'_'+str(azp.id)
                    if not azp.hautazkoa or id_lag in azpiatal_hau:
                        ea.testua = request.POST.get('testu'+id_lag)
                        ea.save()
                        azp_aldatuak.add(id_lag)
                #print("azp_aldatuak",azp_aldatuak)
                for azp in atal.azpiatala_set.all():
                    id_lag = str(atal.id)+'_'+str(azp.id)
                    #print(id_lag)
                    if (not azp.hautazkoa or id_lag in azpiatal_hau) and id_lag not in azp_aldatuak :
                        ea = EdukiaAzpiatala(goiEdukia=e,azpiatala=azp,testua=request.POST.get('testu'+id_lag))
                        ea.save()
                
        for azpi in request.POST.getlist('azpich'):
            a_id,az_id = azpi.split('_')
        return HttpResponseRedirect(reverse('txantiloiak:laburpena',args=(t.id,)))
    else:
        pass
        

class LaburpenaView(generic.DetailView):
    model = Txostena
    template_name = 'txantiloiak/laburpena.html'
    
# def gehitua(request):
#     return HttpResponse("Gehitua")

# def probaform_view(request,espezialitatea_id):
#     espe = Espezialitatea.objects.get(pk=espezialitatea_id)
#     EspezialitateaFormSet = modelformset_factory(Espezialitatea,fields=('izena',))
#     AtalaFormSet = inlineformset_factory(Espezialitatea,Atala, fields=('izenburua',),formset=EspezialitateaInlineForm)
#     if request.method == "POST":
#         formset = AtalaFormSet(request.POST, request.FILES)
#         if formset.is_valid():
#             formset.save()
#             # Do something. Should generally end with a redirect. For example:
#             return HttpResponseRedirect('gehitua')
#     else:
#         formset = AtalaFormSet(instance=espe)
#     return render(request,"txantiloiak/proba.html", {"formset": formset})


