from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Espezialitatea(models.Model):
    izena = models.CharField(max_length=50)
    MOTA_AUKERAK = (
        ('AL','Alta txostena'),
        ('EB','Ebolutiboa'),
    ) 
    mota = models.CharField(max_length=2,
                            choices=MOTA_AUKERAK)

    def __str__(self):
        return self.izena

class Atala(models.Model):
    izenburua = models.CharField(max_length=50)
    hautazkoa = models.BooleanField(default=False)
    espezialitatea = models.ForeignKey('Espezialitatea')
#    goiatala = models.ForeignKey('self',blank=True,null=True)
    testua = models.TextField(blank=True,default='')
    ordena = models.IntegerField()
    def __str__(self):
        return self.espezialitatea.izena + ' -- '+self.izenburua
    class Meta:
        ordering = ['espezialitatea','ordena']
    def azpiatal_kopurua(self):
        return str(len(self.azpiatala_set.all()))
    def defektuzkoTestua(self):
        if self.testua=='':
            return False
        else:
            return True
    defektuzkoTestua.boolean = True

class Azpiatala(models.Model):
    izenburua = models.CharField(max_length=50)
    hautazkoa = models.BooleanField(default=False)
    goiatala = models.ForeignKey(Atala)
    testua = models.TextField(blank=True,default='')
    ordena = models.IntegerField()
    def __str__(self):
        return self.goiatala.izenburua + ' -- '+self.izenburua
    class Meta:
        ordering = ['goiatala','ordena']

class Txostena(models.Model):
    egilea = models.ForeignKey(User)
    data = models.DateTimeField(default=datetime.now,blank=True)
    txosten_testua = models.ManyToManyField(Atala,through='EdukiaAtala')
    
    def __str__(self):
        return str(self.id)
    def egile_izena(self):
        return self.egilea.username
    def get_espezialitatea(self):
        return self.txosten_testua.all()[0].espezialitatea.izena

    class Meta:
        ordering = ["-data"]

class EdukiaAtala(models.Model):
    txostena = models.ForeignKey(Txostena)
    atala = models.ForeignKey(Atala)
    testua = models.TextField(blank=True)
    azpiatalak = models.ManyToManyField(Azpiatala,through='EdukiaAzpiatala')
    def __str__(self):
        return str(self.id)+' -- '+self.testua[:20]
    def azpiatal_kopurua(self):
        return str(len(self.edukiaazpiatala_set.all()))
    class Meta:
        ordering = ['atala__espezialitatea','atala__ordena']

class EdukiaAzpiatala(models.Model):
    goiEdukia = models.ForeignKey(EdukiaAtala)
    azpiatala = models.ForeignKey(Azpiatala)
    testua = models.TextField(blank=True)
    def __str__(self):
        return self.testua[:20]
