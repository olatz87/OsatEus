from django.contrib import admin

# Register your models here.
from .models import Atala,Espezialitatea,Txostena,EdukiaAtala,Azpiatala,EdukiaAzpiatala

class AzpiatalaInline(admin.StackedInline):
    model = Azpiatala
    fieldsets = [('Zehaztapenak',{'fields':['izenburua','hautazkoa','ordena','testua'],'classes':['collapse']})]
    extra = 0

class AtalaAdmin(admin.ModelAdmin):
    list_display = ('espezialitatea','izenburua','ordena','azpiatal_kopurua','defektuzkoTestua')
    fieldsets=[
        (None,{'fields':['izenburua','hautazkoa','ordena','espezialitatea']}),
        ('Defektuzko testua',{'fields':['testua'],'classes':['collapse']}),
    ]
    inlines = [AzpiatalaInline]



class AtalaInline(admin.StackedInline):
    model = Atala
    fieldsets=[
        (None,{'fields':['izenburua','hautazkoa','ordena']}),
        ('Defektuzko testua',{'fields':['testua'],'classes':['collapse']}),
    ]
    extra = 0
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        kwargs["queryset"] = Atala.objects.filter(espezialitatea = request.path.split('/')[-2])
        return super(AtalaInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

class EspezialitateaAdmin(admin.ModelAdmin):
    fields=['izena']
    inlines = [AtalaInline]

    
class EdukiaAzpiatalaInline(admin.TabularInline):
    model = EdukiaAzpiatala
    extra = 0
class EdukiaInline(admin.TabularInline):
    model = EdukiaAtala
    ordering = ()
    extra = 0

class TxostenaAdmin(admin.ModelAdmin):
    list_display = ('id','data','egile_izena')
    inlines = [EdukiaInline]

class EdukiaAtalaAdmin(admin.ModelAdmin):
    list_display = ('id','txostena','atala','azpiatal_kopurua')
    inlines = [EdukiaAzpiatalaInline]

admin.site.register(Espezialitatea,EspezialitateaAdmin)
admin.site.register(Atala,AtalaAdmin)
admin.site.register(Txostena,TxostenaAdmin)
admin.site.register(EdukiaAtala,EdukiaAtalaAdmin)
