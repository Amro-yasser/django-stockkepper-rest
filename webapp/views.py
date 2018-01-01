# from django.shortcuts import render
# from django.http import HttpResponse
# from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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
		ser = serializers.ProductSerializer(data=request.data)
		ser.is_valid(raise_exception=True)
		ser.save()
		return Response(ser.data, status=status.HTTP_201_CREATED)

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

	def get_queryset(self):
		self.queryset.filter(purchase=self.kwargs.get('purchase_pk'))

class RetrieveUpdateDestroyAllocatedItem(generics.RetrieveUpdateDestroyAPIView):
	queryset = models.AllocatedItem.objects.all()
	serializer_class = serializers.AllocatedItemSerializer