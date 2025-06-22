from django.contrib.auth import get_user_model
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import UserSerializer
from .permissions import IsAdminOrReadOnly
from .serializers import LogoutSerializer
User = get_user_model()
class UserRegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes=[AllowAny]
    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

class RefreshTokenView(TokenRefreshView):
    permission_classes = [AllowAny]

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except TokenError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_serializer(self, *args, **kwargs):
        return LogoutSerializer(*args, **kwargs)

# # Products
# class ProductListCreateView(generics.ListCreateAPIView):
#     """
#     GET  /products/     → list all products
#     POST /products/     → create new product
#     """
    
    
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [IsAdminOrReadOnly]  # Ensure only admins can create products


# class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
#     """
#     GET    /products/{pk}/   → retrieve product
#     PUT    /products/{pk}/   → update product
#     DELETE /products/{pk}/   → delete product
#     """
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
    
#     permission_classes = [IsAdminOrReadOnly]  # Ensure only authenticated users can modify products

# #Products ViewSet:

# class ProductViewSet(viewsets.ModelViewSet):
#     """
#     A viewset for viewing and editing product instances.
#     """
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [IsAdminOrReadOnly]  # Ensure only admins can create, update or delete products

# # Orders
# class OrderListCreateView(generics.ListCreateAPIView):
#     """
#     GET  /orders/       → list all orders
#     POST /orders/       → create new order
#     """

#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated] 
    
#     def get_queryset(self):
#         return Order.objects.filter(user=self.request.user)

# class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
#     """
#     GET    /orders/{pk}/    → retrieve order
#     PUT    /orders/{pk}/    → update order
#     DELETE /orders/{pk}/    → delete order
#     """
   
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated] 
    
#     def get_queryset(self):
#         return Order.objects.filter(user=self.request.user)