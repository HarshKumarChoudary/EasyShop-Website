from django.contrib import admin
from .models import cart,order_placed,buyer,seller,address,gender,category,product

@admin.register (address)
class address_admin(admin.ModelAdmin):
    list_display = ['id','user','add_place','state','pin_code']

@admin.register (gender)
class gender_Admin(admin.ModelAdmin):
    list_display = ['id','name']

@admin.register (category)
class category_admin(admin.ModelAdmin):
    list_display = ['id','name']

@admin.register (product)
class product_admin(admin.ModelAdmin):
    list_display = ['id','title','description','image','selling_price','discount_price','Quantity','category','seller']

@admin.register (seller)
class seller_admin(admin.ModelAdmin):
    list_display = ['id','user','name','gen','email','phone_number']


#@admin.register (seller_sells_products)
#class seller_sells_products_admin(admin.ModelAdmin):
    #list_display = ['id','seller_id','product_id']


@admin.register (buyer)
class buyer_admin(admin.ModelAdmin):
    list_display = ['id','user','name','gen','email','phone_number']
    

@admin.register (cart)
class cart_admin(admin.ModelAdmin):
    list_display = ['id','buyer','product','quantity']

@admin.register (order_placed)
class order_placed_admin(admin.ModelAdmin):
    list_display = ['id','deliveryaddress','buyer','product','quantity','ordered_date','status']




    




    


