from rest_framework import serializers
from .models import User
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import APIException
from rest_framework import status
from accounts.models import Category,Subcategory,Item, Review

class CustomizedValidation(APIException):
    status_code = status.HTTP_200_OK
    default_detail = 'A server error occurred.'

    def __init__(self, detail, status_code):
        if status_code is not None:self.status_code = self.status_code
        if detail is not None:
            self.detail = {'message':detail, 'status':status_code}
        else: self.detail = {'detail': force_text(self.default_detail)}

class SocialLoginSerializer(serializers.Serializer):
    signup_method = serializers.CharField()
    access_token = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username','userImage','email', 'password','phone','fullname','gender','dob')

    def validate(self, attrs):
        if len(attrs['password']) < 6:
            raise ValidationError({'message': 'Password should contain atleast 6 characters'})
        elif len(attrs['password']) > 16:
            raise ValidationError({'message': 'Password should not exceed more than 16 characters'})
        mail = User.objects.filter(email=attrs['email']).exists()
        phone_number = User.objects.filter(phone=attrs['phone']).exists()
        if mail == True and phone_number == True:
            raise CustomizedValidation(detail="Phone number and email are already registered",
                                       status_code=status.HTTP_400_BAD_REQUEST)
        if mail == False and phone_number == True:
            raise CustomizedValidation(detail="phone is already registered", status_code=status.HTTP_400_BAD_REQUEST)
        if mail == True and phone_number == False:
            raise CustomizedValidation(detail="email is already registered", status_code=status.HTTP_400_BAD_REQUEST)
        return attrs


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class CartSerializer(serializers.Serializer):
    category_name = serializers.CharField()


class UserProfileUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False, allow_blank=True)
    # bio = serializers.CharField(required=False, allow_blank=True)
    # profile_image = serializers.ImageField(required=False)
    username = serializers.CharField(required=False)
    # hidden = serializers.BooleanField(required=False)
    # delete = serializers.BooleanField(required=False)
    # enabled_two_factor_auth = serializers.BooleanField(required=False)

    # def validate_username(self, username):
    #     if 'peercrate' in username or 'facebook' in username or \
    #             'twitter' in username or 'instagram' in username:
    #         raise serializers.ValidationError('This username is not allowed')
    #     return username


    # def validate_phone(self, phone):
    #     p = phonenumbers.parse(phone, None)
    #     try:
    #         x = int(phone)
    #     except:
    #         raise serializers.ValidationError('Invalid phone number')
    #     if not phonenumbers.is_valid_number(p):
    #         raise serializers.ValidationError('Invalid phone number')
    #
    #     return phone


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, old_password):
        user = self.context.get('user')
        if not user.check_password(old_password):
            raise serializers.ValidationError("password is incorrect")
        return old_password


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'phone')


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    email = serializers.EmailField()

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("email is not registered")
        return email

class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128)
    token = serializers.CharField()

    def validate(self, attrs):
        try:
            user = User.objects.filter(rp_otp=attrs['token']).first()
        except:
            raise ValidationError({'message': 'User not found'})

        if len(attrs['password']) < 6:
            raise ValidationError({'message': 'Password should contain atleast 6 characters'})
        elif len(attrs['password']) > 16:
            raise ValidationError({'message': 'Password should not exceed more than 16 characters'})
        return attrs


class ItemSerializer(serializers.Serializer):
    cityName = serializers.CharField(max_length=255)
    serviceName = serializers.CharField(max_length=255)
    categoryName = serializers.CharField(max_length=255)
    subcategoryName = serializers.CharField(max_length=255)
    itemName = serializers.CharField(max_length=255)
    address = serializers.CharField(max_length=255)
    phoneNumber = serializers.CharField(max_length=255)
    status = serializers.CharField(max_length=255)
    businessInfo = serializers.CharField(max_length=255)
    itemImage = serializers.FileField()
    availableTime = serializers.CharField(max_length=255)
    socialMediaLink = serializers.CharField(max_length=255)

    def validate_itemName(self, itemName):
        if  Item.objects.filter(itemName=itemName).exists():
            raise serializers.ValidationError("ItemName already exists")
        return itemName

class ReviewSerializer(serializers.Serializer):
    item_id = serializers.CharField(max_length=255)
    item =serializers.CharField(max_length=255)
    comment = serializers.CharField(max_length=255)

    def get_item(self,obj):
        return obj.item.itemName

    class Meta:
        model = Review
        fields = ('itemId','item','rating')

class SubcategorySerializer(serializers.Serializer):
    categoryName = serializers.SerializerMethodField()
    subcategoryName = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()

    def get_subcategoryName(self,obj):
        return obj.subcategoryName

    def get_categoryName(self,obj):
        return obj.categoryName.categoryName

    def get_level(self,obj):
        return obj.depth

    class Meta:
        model = Subcategory
        fields = '__all__'

class CategorySerializer(serializers.Serializer):
    categoryName = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    serviceName=serializers.SerializerMethodField()

    def get_categoryName(self,obj):
        # return obj[0].categoryName
        return obj.categoryName

    def get_level(self,obj):
        # return obj[1]['level']
        return obj.depth

    def get_serviceName(self,obj):
        return obj.serviceName.serviceName

    class Meta:
        model = Category
        fields = 'categoryName'

class ServiceSerializer(serializers.Serializer):
    serviceName = serializers.CharField(max_length=255)

class ItemSearchSerializer(serializers.Serializer):
    itemId = serializers.CharField(max_length=255)
    serviceName = serializers.CharField(max_length=255)
    categoryName = serializers.CharField(max_length=255)
    subcategoryName = serializers.CharField(max_length=255)
    itemName = serializers.CharField(max_length=255)
    address = serializers.CharField(max_length=255)
    phoneNumber = serializers.CharField(max_length=255)
    status = serializers.CharField(max_length=255)
    businessInfo = serializers.CharField(max_length=255)
    itemImage = serializers.CharField(max_length=255)
    availableTime = serializers.CharField(max_length=255)
    socialMediaLink = serializers.CharField(max_length=255)

    def get_serviceName(self, obj):
        return obj.serviceName.serviceName

    def get_categoryName(self, obj):
        return obj.categoryName.categoryName

    def get_subcategoryName(self, obj):
        return obj.subcategoryName.subcategoryName

    def get_itemName(self, obj):
        return obj.itemName

    def get_itemId(self, obj):
        return obj.itemId

    def get_address(self, obj):
        return obj.address

    def get_phoneNumber(self, obj):
        return obj.phoneNumber

    def get_status(self, obj):
        return obj.status

    def get_businessInfo(self, obj):
        return obj.businessInfo

    def get_itemImage(self, obj):
        return obj.itemImage

    def get_availableTime(self, obj):
        return obj.availableTime

    def get_socialMediaLink(self, obj):
        return obj.socialMediaLink

    class Meta:
        model = Item
        fields = ('itemId', 'serviceName', 'categoryName', 'subcategoryName', 'address', 'phoneNumber'\
                  , 'status', 'businessInfo', 'itemImage', 'availableTime', 'socialMediaLink')


