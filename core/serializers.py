from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
# from .models import Product, Order, OrderItem


User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {
            'email' : {
              'validators': [UniqueValidator(queryset=User.objects.all())], 
            },
            'password': {'write_only': True, 'min_length' : 8},
            
            'role': {'read_only': True},
            'is_premium': {'read_only': True},
            'is_blocked': {'read_only': True},
            
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
        

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(
        help_text="The refresh token to blacklist (as returned by /api/token/)."
    )
        
# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = ['id', 'name', 'price', 'image', 'image_url']
#         model = Product
#         read_only_fields = ['id']
        
#     image = serializers.ImageField(required=False)
#     image_url = serializers.SerializerMethodField()
    
#     def get_image_url(self, obj):
#         request = self.context.get('request')
#         if obj.image and request:
#             return request.build_absolute_uri(obj.image.url)
#         return None


# class OrderItemSerializer(serializers.ModelSerializer):
#     product = ProductSerializer(read_only=True)
#     product_id = serializers.PrimaryKeyRelatedField(queryset =Product.objects.all(), source='product', write_only=True)
    
#     class Meta:
#         model = OrderItem
#         fields = ['product_id', 'product', 'quantity']
#         read_only_fields = ['id']
    
    

# class OrderSerializer(serializers.ModelSerializer):
#     items = OrderItemSerializer(
#         source='orderitem_set', many=True
#     )
#     total = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = Order
#         fields = ['id', 'user', 'status',  'items', 'total']
#         read_only_fields = ['id', 'user', 'total']

#     def get_total(self, obj):
#         return sum(item.product.price * item.quantity for item in obj.orderitem_set.all())

#     def create(self, validated_data):
#         items_data = validated_data.pop('orderitem_set')
#         user = self.context['request'].user
#         order = Order.objects.create(user=user, **validated_data)
#         for item in items_data:
#             OrderItem.objects.create(order=order, **item)
#         return order