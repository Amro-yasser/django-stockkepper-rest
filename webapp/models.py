from django.db import models

# Create your models here.

class Product(models.Model):
	name=models.CharField(max_length=300)
	
class Purchase(models.Model):
	rtn = models.CharField(max_length=128)
	pon = models.CharField(max_length=128)
	notes = models.CharField(max_length=300, default='')

class PurchaseItem(models.Model):
	location = models.CharField(max_length=128)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	purchase = models.ForeignKey(Purchase, related_name='products', on_delete=models.CASCADE)
	original_quantity = models.IntegerField()
	allocated_quantity = models.IntegerField(default=0)

class Request(models.Model):
	notes=models.CharField(max_length=300)

class RequestItem(models.Model):
	request = models.ForeignKey(Request, on_delete=models.DO_NOTHING)
	project_id = models.CharField(max_length=128)
	product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
	quantity = models.IntegerField()

class AllocatedItem(models.Model):
	request_item = models.ForeignKey(RequestItem, on_delete=models.DO_NOTHING)
	purchase = models.ForeignKey(Purchase, on_delete=models.DO_NOTHING)
	quantity = models.IntegerField()
	notes = models.CharField(max_length=300)

