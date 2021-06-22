from django.contrib import admin


from .models import alllaptops, dell, gaminglaptop, homesite , homepagemobile, msi, razerblade,dell,hp,asus,acer,apple,lenovo

class alllaptopsAdmin(admin.ModelAdmin):
    list_display=('laptopname','price','site')
class acerAdmin(admin.ModelAdmin):
    list_display=['site','price']
class homepagemobileAdmin(admin.ModelAdmin):
    list_display=('mobilename','price')

admin.site.register(homesite)
admin.site.register(gaminglaptop)
admin.site.register(homepagemobile)
admin.site.register(msi)
admin.site.register(dell)
admin.site.register(hp)
admin.site.register(razerblade)
admin.site.register(asus)
admin.site.register(acer)
admin.site.register(apple)
admin.site.register(lenovo)
admin.site.register(alllaptops,alllaptopsAdmin)

