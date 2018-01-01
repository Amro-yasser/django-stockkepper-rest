from rest_framework import serializers
from . import models

class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Product
		fields = '__all__'

class PurchaseItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.PurchaseItem
		fields = ('location', 'product', 'original_quantity', 'allocated_quantity')
	
class PurchaseSerializer(serializers.ModelSerializer):
	products = PurchaseItemSerializer(many=True)
	
	class Meta:
		model = models.Purchase
		fields = ('id', 'rtn', 'pon', 'notes', 'products')

	def create(self, validated_data):
		products_data = validated_data.pop('products')
		purchase = models.Purchase.objects.create(**validated_data)
		for product_data in products_data:
			models.PurchaseItem.objects.create(purchase=purchase, **product_data)
		return purchase

class RequestSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Request
		fields = '__all__'

class RequestItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.RequestItem
		fields = '__all__'



class RequestSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Request
		fields = '__all__'

class AllocatedItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.AllocatedItem
		fields = '__all__'
