from rest_framework import serializers
from . import models

class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Product
		fields = '__all__'

class PurchaseItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.PurchaseItem
		fields = ('id', 'location', 'product', 'original_quantity', 'allocated_quantity')
		extra_kwargs = {'id': {'required': False, 'read_only': False}}
	
class PurchaseSerializer(serializers.ModelSerializer):
	products = PurchaseItemSerializer(many=True)
	
	class Meta:
		model = models.Purchase
		fields = ('id', 'rtn', 'pon', 'notes', 'products')
		extra_kwargs = {'id': {
				'required': False,
				'read_only': False
			}
		}
	
	def create(self, validated_data):
		products_data = validated_data.pop('products')
		purchase = models.Purchase.objects.create(**validated_data)
		for product_data in products_data:
			models.PurchaseItem.objects.create(purchase=purchase, **product_data)
		return purchase

	def update(self, instance, validated_data):
		products_data = validated_data.pop('products')
		inc = -1
		for p in products_data:
			try:
				id = p['id']
			except Exception as e:
				p['id'] = inc
				inc -= 1
		# garbage_items = validated_data.pop('garbageItems')
		# garbage_items_mapping = {item['id']: item for item in garbage_items}
		product_mapping = {product.id: product for product in instance.products.all()}
		data_mapping = {item['id']: item for item in products_data}
		instance.rtn = validated_data.get('rtn', instance.rtn)
		instance.pon = validated_data.get('pon', instance.pon)
		instance.notes = validated_data.get('notes', instance.notes)
		instance.save()
		ret = []
		for item_id, data in data_mapping.items():
			product = product_mapping.get(item_id, None)
			if product is None:
				# delattr(data, 'id')
				ret.append(models.PurchaseItem.objects.create(purchase=instance, 
				location=data['location'],
				product=data['product'],
				allocated_quantity=data['allocated_quantity'],
				original_quantity=data['original_quantity'],
				))
			else:
				print(data['location'])
				product.location = data['location']
				product.original_quantity = data['original_quantity']
				product.product = data['product']
				product.save()
				ret.append(product)
		
		# for item_id, data in garbage_items_mapping.items():
		# 	product = product_mapping.get(item_id, None)
		# 	if product is not None:
		# 		product.delete()
		instance.products.set(ret)
		return instance

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
