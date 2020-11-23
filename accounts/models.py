from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible
from treebeard.mp_tree import MP_Node

@python_2_unicode_compatible
class User(AbstractUser):
    userImage = models.FileField(blank=True, null=True)
    fullname = models.CharField(max_length=255,null=True, blank=True)
    gender = models.CharField(max_length=255,null=True, blank=True)
    dob = models.CharField(max_length=255,null=True, blank=True)
    email = models.CharField(max_length=255,null=True, blank=True)
    phone = models.CharField(max_length=15,null=True, blank=True)
    signup_method = models.CharField(max_length=255,null=True, blank=True)
    rp_otp = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = ('User')


class Service(models.Model):
    serviceId =  models.AutoField(primary_key=True)
    serviceName = models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
        return self.serviceName

    class Meta:
        verbose_name_plural = ('Service')


class Category(MP_Node):
    categoryId = models.AutoField(primary_key=True)
    categoryName = models.CharField(max_length=255,null=True,blank=True)
    serviceName = models.ForeignKey(Service,on_delete=models.CASCADE)

    node_order_by = ['categoryName']

    def __str__(self):
        return self.categoryName

    def __unicode__(self):
        return 'Category: %s' % self.categoryName

    class Meta:
        verbose_name_plural = ('Category')



class Subcategory(MP_Node):
    subcategoryId = models.AutoField(primary_key=True)
    categoryName = models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategoryName = models.CharField(max_length=255,null=True,blank=True)

    node_order_by = ['subcategoryName']

    def __str__(self):
        return self.subcategoryName

    def __unicode__(self):
        return 'Subcategory: %s' % self.subcategoryName

    class Meta:
        verbose_name_plural = ('Subcategory')


class Country(models.Model):
    countryName = models.CharField(max_length=30,null=True, blank=True)

    def __str__(self):
        return self.countryName

    class Meta:
        verbose_name_plural = ('Country')


class State(models.Model):
    stateName = models.CharField(max_length=30,null=True, blank=True)
    countryName = models.ForeignKey(Country,on_delete=models.CASCADE,)

    def __str__(self):
        return self.stateName

    class Meta:
        verbose_name_plural = ('State')


class City(models.Model):
    cityName  = models.CharField(max_length=30,null=True, blank=True)
    stateName = models.ForeignKey(State,on_delete=models.CASCADE)

    def __str__(self):
        return self.cityName

    class Meta:
        verbose_name_plural = ('City')

class TimeStampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

class Item(models.Model):
    item_addedBy = models.ForeignKey(User, on_delete=models.deletion.CASCADE, related_name='itemAddedBy')
    itemId = models.AutoField(primary_key=True)
    serviceName= models.ForeignKey(Service,on_delete=models.CASCADE,default='')
    categoryName = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategoryName =  models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    itemName = models.CharField(max_length=255,null=True,blank=True)
    address = models.TextField()
    phoneNumber = models.CharField(max_length=255,null=True,blank=True)
    status = models.CharField(max_length=255,null=True,blank=True)
    businessInfo = models.TextField()
    itemImage = models.FileField(null=True,blank=True)
    cityName = models.ForeignKey(City,on_delete=models.CASCADE)
    availableTime = models.CharField(max_length=255,null=True,blank=True)
    socialMediaLink = models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
        return self.itemName

    class Meta:
        verbose_name_plural = ('Items')


class Review(models.Model):
    reviewId = models.AutoField(primary_key=True)
    reviewBy =  models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    comment = models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
        return self.item.itemName

    class Meta:
        verbose_name_plural = ('Review')

