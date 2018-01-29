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

class ProductPurchaseItemSerializer(serializers.ModelSerializer):
	# purchase = serializers.SlugRelatedField(
    #     many=False,
    #     read_only=True,
    #     slug_field='pon'
    #  )
	purchase_pon = serializers.CharField(source='purchase.pon')
	class Meta:
		model = models.PurchaseItem
		fields = ('id', 'location', 'product', 'original_quantity', 'allocated_quantity', 'purchase', 'purchase_pon')
		extra_kwargs = {'id': {'required': False, 'read_only': False}}

class AllocatedItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.AllocatedItem
		fields = ('id', 'request_item', 'product', 'request', 'purchase', 'purchase_item', 'quantity')
		extra_kwargs = {'id': {'required': False, 'read_only': False}}
	
class PurchaseAllItemsSerializer(serializers.ModelSerializer):
	product_name = serializers.CharField(source='product.name')
	purchase_pon = serializers.CharField(source='purchase.pon')
	item_allocations = AllocatedItemSerializer(many=True)
	class Meta:
		model = models.PurchaseItem
		fields = ('id', 'location', 'product', 'original_quantity', 'allocated_quantity', 'purchase', 'product_name', 'purchase_pon', 'item_allocations')
		extra_kwargs = {'id': {'required': False, 'read_only': False}}

class AllocationForSerializer(serializers.ModelSerializer):

	class Meta:
		model = models.AllocatedItem
		fields = ('id', 'request', 'request_item', 'product',  'purchase', 'purchase_item', 'quantity')
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

class RawPurchaseSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Purchase
		fields = ('id', 'rtn', 'pon', 'notes', 'product')
		extra_kwargs = {'id': {
				'required': False,
				'read_only': False
			}
		}

class RequestItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.RequestItem
		fields = ('id', 'project_id', 'product', 'quantity')
		extra_kwargs = {'id': {'required': False, 'read_only': False}}

class RequestSerializer(serializers.ModelSerializer):
	items = RequestItemSerializer(many=True)
	allocations = AllocatedItemSerializer(many=True)
	
	class Meta:
		model = models.Request
		fields = ('id', 'notes', 'items', 'allocations')
		extra_kwargs = {'id': {
				'required': False,
				'read_only': False
			},
			'notes': {'required': 'False'}
		}
	
	def create(self, validated_data):
		items = validated_data.pop('items')
		allocations = validated_data.pop('allocations')
		request = models.Request.objects.create(**validated_data)
		for itm in items:
		 	models.RequestItem.objects.create(request=request, **itm)
		# for alc in allocations:
		#  	models.AllocatedItem.objects.create(request=request, **alc)
		return request

	def update(self, instance, validated_data):
		items_data = validated_data.pop('items')
		allocations = validated_data.pop('allocations')
		inc = -1
		for p in items_data:
			try:
				id = p['id']
			except Exception as e:
				p['id'] = inc
				inc -= 1
		instance_item_mapping = {item.id: item for item in instance.items.all()}
		validated_data_mapping = {item['id']: item for item in items_data}
		instance.notes = validated_data.get('notes', instance.notes)
		instance.save()
		ret = []
		for item_id, data in validated_data_mapping.items():
			item = instance_item_mapping.get(item_id, None)
			if item is None:
				ret.append(models.RequestItem.objects.create(request=instance, 
				project_id=data['project_id'],
				product=data['product'],
				quantity=data['quantity'],
				))
			else:
				item.project_id = data['project_id']
				item.quantity = data['quantity']
				item.product = data['product']
				item.save()
				ret.append(item)
		
		instance.items.set(ret)
		return instance


