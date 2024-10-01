# from rest_framework import serializers
#
# from products.models import Product, ProductImage
#
#
# class ProductSerializer(serializers.ModelSerializer):
#     category = serializers.SlugRelatedField(slug_field='name', read_only=True)
#
#     class Meta:
#         model = Product
#         fields = ('id', 'name', 'description', 'price', 'quantity', 'category')
#
#
# class ProductImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductImage
#         fields = ('image', 'product')
