from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
# category, gender, 
class address(models.Model):
    STATE_CHOICES = (
     ('Andaman and Nicobar','Andaman and Nicobar'),
     ('Assam','Assam'),
     ('Andhra Pradesh','Andhra Pradesh'),
     ('Arunachal Pradesh','Arunachal Pradesh'),
     ('Bihar','Bihar'),
     ('Chhattisgarh','Chhattisgarh'),
     ('Dadar and Nagar Haveli','Dadar and Nagar Haveli'),
     ('Daman and Diu','Daman and Diu'),
     ('Goa','Goa'),
     ('Gujarat','Gujarat'),
     ('Haryana','Haryana'),
     ('Himachal Pradesh	','Himachal Pradesh	'),
     ('Jharkhand','Jharkhand'),
     ('Karnataka','Karnataka'),
     ('Kerala','Kerala'),
     ('Madhya Pradesh','Madhya Pradesh'),
     ('Maharashtra','Maharashtra'),
     ('Manipur','Manipur'),
     ('Meghalaya','Meghalaya'),
     ('Mizoram','Mizoram'),
     ('Nagaland','Nagaland'),
     ('Odisha','Odisha'),
     ('Punjab','Punjab'),
     ('Rajasthan','Rajasthan'),
     ('Sikkim','Sikkim'),
     ('Tamil Nadu','Tamil Nadu'),
     ('Telangana','Telangana'),
     ('Tripura','Tripura'),
     ('Uttar Pradesh','Uttar Pradesh'),
     ('Uttarakhand','Uttarakhand'),
     ('West Bengal','West Bengal'),
)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null =True )
    add_place = models.TextField()
    state = models.CharField(max_length=50,choices=STATE_CHOICES)
    pin_code = models.IntegerField()

    def __str__(self):
        return str(self.id)
    

class gender(models.Model):
    gender_list=[
    ('M','male'),
    ('F','female'),
    ]
    name = models.CharField(max_length=1,choices=gender_list)
    def __str__(self):
        return self.name
        
class category(models.Model):
    category_list = [
        ('TopWears','Top Wears'),
        ('FrontWears','Front Wears'),
        ('Stationary','Stationary'),
        ('Electronics','Electronics'),
        ('DailyNeeds','Daily needs'),
        ('  ','services'),
        ('Fashion','Fashion'),
        ('Mobiles','Mobiles'),
        ('Laptop','Laptop')
    ]
    name = models.CharField(max_length=20,choices=category_list)
    def __str__(self):
        return self.name


class seller(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null =True )
    name = models.CharField(max_length=30)
    phone_number = models.IntegerField()
    email = models.EmailField(max_length=254)
  #  address = models.ForeignKey("address",on_delete=models.SET_NULL,null=True)
    gen = models.ForeignKey("gender",on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return str(self.id)
    


class product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to="productimg",null=True)
    selling_price = models.FloatField()
    discount_price = models.FloatField()
    Quantity = models.IntegerField()
    category = models.ForeignKey("category",on_delete=models.CASCADE,null=True)
    seller = models.ForeignKey("seller",on_delete = models.CASCADE,null =True)
    def __str__(self):
        return str(self.id)
    


#many to many table between seller and product
#class seller_sells_products(models.Model):
   # seller_id = models.ForeignKey("seller",on_delete=models.CASCADE)
   # product_id = models.ForeignKey("product", on_delete = models.CASCADE)

    #def __str__(self):
       # return str(self.id)

class buyer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=20)
    gen = models.ForeignKey("gender",on_delete=models.SET_NULL,null=True)
   # address = models.ForeignKey("address",on_delete=models.SET_NULL,null=True)
    email = models.EmailField(max_length=250)
    phone_number = models.IntegerField()

    def __str__(self):
        return str(self.id)

class cart(models.Model):
    #user = user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    buyer = models.ForeignKey("buyer",on_delete=models.CASCADE)
    product = models.ForeignKey("product",on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    @property
    def total_cost(self):
        return self.quantity*self.product.discount_price


class order_placed(models.Model):
    STATUS_CHOICES = (
        
        ('Accepted','Accepted'),    
        ('Packed','Packed'),
        ('Delivered','Delivered'),  
        ('Canceled','Canceled')
    )
    deliveryaddress = models.ForeignKey("address",on_delete=models.CASCADE,null=True)
    buyer = models.ForeignKey("buyer",on_delete=models.CASCADE)
    product = models.ForeignKey("product",on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default = 1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')
   # seller_who_sold = models.ForeignKey("seller_sells_products",on_delete = models.CASCADE)
    @property
    def total_cost(self):
        return self.quantity*self.product.discount_price
