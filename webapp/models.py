from django.db import models

# Create your models here.

class Product(models.Model):
	name=models.CharField(max_length=300)
	
class Purchase(models.Model):
	rtn = models.CharField(max_length=128)
	pon = models.CharField(max_length=128)
	notes = models.CharField(max_length=300, default='')

	def __str__(self):
		return "%s" % (self.pon)

class PurchaseItem(models.Model):
	location = models.CharField(max_length=128)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	purchase = models.ForeignKey(Purchase, related_name='products', on_delete=models.CASCADE)
	original_quantity = models.IntegerField()
	allocated_quantity = models.IntegerField(default=0)

class Request(models.Model):
	req_from=models.CharField(max_length=300)
	notes = models.CharField(max_length=300, default='')

class RequestItem(models.Model):
	request = models.ForeignKey(Request, related_name='items', on_delete=models.CASCADE)
	project_id = models.CharField(max_length=128)
	product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
	quantity = models.IntegerField()

class AllocatedItem(models.Model):
	request = models.ForeignKey(Request, related_name='allocations', on_delete=models.CASCADE)
	request_item = models.ForeignKey(RequestItem, on_delete=models.DO_NOTHING)
	product = models.ForeignKey(Product, related_name='product_allocations', on_delete=models.DO_NOTHING)
	purchase = models.ForeignKey(Purchase, on_delete=models.DO_NOTHING)
	purchase_item = models.ForeignKey(PurchaseItem, related_name='item_allocations', on_delete=models.DO_NOTHING)
	quantity = models.IntegerField()

