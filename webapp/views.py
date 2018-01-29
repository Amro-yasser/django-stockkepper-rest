# from django.shortcuts import render
# from django.http import HttpResponse
# from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from . import models
from . import serializers
# Create your views here.
# product
class ListCreateProduct(APIView):
	def get(self, request, format = None):
		pur = models.Product.objects.all()
		ser = serializers.ProductSerializer(pur, many=True) # we are passing multiple item instead of single item
		return Response(ser.data)

	def post(self, request, format = None):
		ser = serializers.ProductSerializer(data=request.data)
		ser.is_valid(raise_exception=True)
		ser.save()
		return Response(ser.data, status=status.HTTP_201_CREATED)

class RetrieveUpdateDestroyProduct(generics.RetrieveUpdateDestroyAPIView):
	queryset = models.Product.objects.all()
	serializer_class = serializers.ProductSerializer

# purchase
# class ListCreatePurchase(generics.ListCreateAPIView):
# 	queryset = models.Purchase.objects.all()
# 	serializer_class = serializers.PurchaseSerializer
class ListCreatePurchase(APIView):
	def get(self, request, format = None):
		pur = models.Purchase.objects.all()
		ser = serializers.PurchaseSerializer(pur, many=True) # we are passing multiple item instead of single item
		return Response(ser.data)

	def post(self, request, format = None):
		ser = serializers.PurchaseSerializer(data=request.data)
		ser.is_valid(raise_exception=True)
		ser.save()
		return Response(ser.data, status=status.HTTP_201_CREATED)

class RTU(APIView):
	def get(self, request, product_pk=None):
		pur_set = models.PurchaseItem.objects.all().filter(product=product_pk)
		ser = serializers.ProductPurchaseItemSerializer(pur_set, many=True) # we are passing multiple item instead of single item
		return Response(ser.data)

# in dashboard
class PurchaseAllItems(APIView):
	def get(self, request):
		pur_set = models.PurchaseItem.objects.all()
		ser = serializers.PurchaseAllItemsSerializer(pur_set, many=True) # we are passing multiple item instead of single item
		raw_data = ser.data
		for r in raw_data:
			allocated = 0
			for alloc in r['item_allocations']:
				allocated += alloc['quantity']
			r['available_quantity'] = r['original_quantity'] - allocated
		return Response(raw_data)

class getPurchaseAllocatedItem(APIView):
	def get(self, request, purchase_pk=None, product_pk=None):
		alloc = models.AllocatedItem.objects.all().filter(product=product_pk, purchase=purchase_pk)
		ser = serializers.AllocationForSerializer(alloc, many=True) # we are passing multiple item instead of single item
		return Response(ser.data)

class RetrieveUpdateDestroyPurchase(generics.RetrieveUpdateDestroyAPIView):
	queryset = models.Purchase.objects.all()
	serializer_class = serializers.PurchaseSerializer

# purchase item
class ListCreatePurchaseItem(generics.ListCreateAPIView):
	queryset = models.PurchaseItem.objects.all()
	serializer_class = serializers.PurchaseItemSerializer

class RetrieveUpdateDestroyPurchaseItem(generics.RetrieveUpdateDestroyAPIView):
	queryset = models.PurchaseItem.objects.all()
	serializer_class = serializers.PurchaseItemSerializer

# request
class ListCreateRequest(generics.ListCreateAPIView):
	queryset = models.Request.objects.all()
	serializer_class = serializers.RequestSerializer

class RetrieveUpdateDestroyRequest(generics.RetrieveUpdateDestroyAPIView):
	queryset = models.Request.objects.all()
	serializer_class = serializers.RequestSerializer

# request item
class ListCreateRequestItem(generics.ListCreateAPIView):
	queryset = models.RequestItem.objects.all()
	serializer_class = serializers.RequestItemSerializer

class RetrieveUpdateDestroyRequestItem(generics.RetrieveUpdateDestroyAPIView):
	queryset = models.RequestItem.objects.all()
	serializer_class = serializers.RequestItemSerializer

# allocate request item
class ListCreateAllocatedItem(generics.ListCreateAPIView):
	queryset = models.AllocatedItem.objects.all()
	serializer_class = serializers.AllocatedItemSerializer
	
	def get(self, request, request_item_pk=None):
		pur_set = models.AllocatedItem.objects.all().filter(request_item=request_item_pk)
		ser = serializers.AllocatedItemSerializer(pur_set, many=True) # we are passing multiple item instead of single item
		return Response(ser.data)
	
	def get_queryset(self):
		self.queryset.filter(request_item=self.kwargs.get('request_item_pk'))

class RetrieveUpdateDestroyAllocatedItem(generics.RetrieveUpdateDestroyAPIView):
	queryset = models.AllocatedItem.objects.all()
	serializer_class = serializers.AllocatedItemSerializer