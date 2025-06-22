from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Transaction, Category

class CategorySerializer(serializers.ModelSerializer):
    """
    - Enforces that each user can’t create duplicate category names.
    - Assigns the current user automatically on create.
    """
    # this field will never show up in the browsable API,
    # but DRF will automatically fill it with request.user
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Category
        fields = ['id', 'name', 'user']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
        'name': {
            'trim_whitespace': True,  # Clean up accidental spaces
            'allow_blank': False,     # Explicitly disallow empty names
            'max_length': 100         # Mirror model's max_length
        }
    }
                # enforce uniqueness at the serializer layer too
        validators = [
            UniqueTogetherValidator(
                queryset=Category.objects.all(),
                fields=['user', 'name'],
                message="You already have a category with this name."
            )
        ]
        
    
    def validate_name(self, value):
        user =  self.context['request'].user
        if Category.objects.filter(user=user, name__iexact=value).exists():
            raise serializers.ValidationError("You already have a category with this name.")
        return value
    
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
    
    
class TransactionSerializer(serializers.ModelSerializer):
    """
    - Validates that the category belongs to the requesting user.
    - Validates positive amount.
    - Exposes category name for read operations.
    """
    

    # date = serializers.DateField(input_formats=["%m-%d-%y"]) 
    category = serializers.PrimaryKeyRelatedField(
         queryset=Category.objects.none()
    )
    
    category_name = serializers.CharField(
        source='category.name', read_only=True
    )
    
    date = serializers.DateField(required=False,)


    class Meta:
        model = Transaction
        fields = [
            'id',
            'type',
            'amount',
            'date',
            'note',
            'category',
            'category_name',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        # Enforce at API level
        extra_kwargs = {
        'amount': {
            'min_value': 0.01,          # API-level validation
            'max_digits': 10,           # Mirror model
            'decimal_places': 2          # Mirror model
        },
        'date': {
            'required': False,           # Explicit even if model has null=False
            'input_formats': ['%Y-%m-%d'] # Standardize date format
        },
        'note': {
            'trim_whitespace': True,
            'allow_blank': True,         
            'required': False            
        },
        'type': {
            'required': True            
        }
    }
        
    def get_fields(self):
        fields = super().get_fields()

        # Check if user categories are already passed in the context
        if 'user_categories' in self.context:
            fields['category'].queryset = self.context['user_categories']
        # else:
        #     # If not, dynamically filter categories based on the logged-in user (This will not happen)
        #     user = self.context['request'].user
        #     fields['category'].queryset = Category.objects.filter(user=user)
        
        return fields

    def validate_category(self, category):
        """
        Ensure user isn't assigning someone else's category.
        """
        user = self.context['request'].user
        if category.user != user:
            raise serializers.ValidationError("Cannot use a category you don’t own.")
        return category

    def validate_amount(self, value):
        """
        Ensure the transaction amount is positive.
        """
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value


class DashboardSummarySerializer(serializers.Serializer):
    """
    Read-only representation of the user’s current financial snapshot.
    All three fields are returned as strings (the standard DRF
    representation for DecimalField) with two decimal places.
    """
    total_income  = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    total_expense = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    balance       = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )