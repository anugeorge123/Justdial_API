import os
import requests
import urllib.request
import json
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from accounts import utils as ut
from accounts.models import User, Category, Service, City,Subcategory, Item, Review
from .serializers import SocialLoginSerializer,UserSerializer,UserLoginSerializer,\
     UserProfileUpdateSerializer, ChangePasswordSerializer, UserProfileSerializer, \
    PasswordResetSerializer, PasswordResetConfirmSerializer,ItemSerializer, ReviewSerializer, \
    SubcategorySerializer,CategorySerializer,ServiceSerializer,ItemSearchSerializer
from django.db.models import Q

class SocialLoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SocialLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        signup_method = serializer.data.get('signup_method')

        # Facebook
        if signup_method == 'facebook':
            signup_method = serializer.data.get('signup_method')
            access_token = serializer.data.get('access_token')
            url = 'https://graph.facebook.com/v3.2/me?fields=id,name,email,picture&access_token=' + serializer.data['access_token']
            data = requests.get(url).json()
            # check data values
            email = data["email"]
            username = data['name']
            user = User.objects.filter(email=email)
            if not user.exists():
                user = User(email=email)
                if len(username.split(' ')) > 1:
                    user.first_name = username.split(' ')[0]
                    user.last_name = username.split(' ')[1]
                else:
                    user.first_name = username

                image_url = 'https://graph.facebook.com/' + data['id'] + '/picture?type=large'
                img = urllib.request.urlretrieve(image_url, user.first_name + ".jpg")
                user.userImage = img[0]
                r = requests.get(image_url)
                with open('staticfiles/media/'+ user.first_name + ".jpg", 'wb') as f:
                    f.write(r.content)
                os.remove(user.first_name + ".jpg")
                user.username = email.split('@')[0].lower() + '_facebook'
                user.email_verified = True
                user.signup_method = signup_method
                user.save()
            else:
                user = user[0]

        token, created = Token.objects.get_or_create(user=user)
        return Response(data={'response':{'access_token': token.key, "userId":user.id,},
                              "message": "Login Successful",
                              }, status=status.HTTP_200_OK)


class SignupView(viewsets.ModelViewSet):
    # parser_class = (FileUploadParser,)
    http_method_names = ['post', ]
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        phone = serializer.data.get('phone')
        email = serializer.data.get('email')
        dob = serializer.data.get('dob')
        gender = serializer.data.get('gender')
        image = serializer.validated_data.get('userImage')
        user = User()
        user.set_password(serializer.data.get('password'))
        user.email = email
        user.username = username
        user.phone = phone
        user.userImage = image
        user.gender = gender
        user.dob = dob
        # ut.confirmation_email(email, user)
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response(data={'status': status.HTTP_200_OK,'token':token.key},
                        status=status.HTTP_200_OK)


class LoginView(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['post']
    serializer_class = UserLoginSerializer

    def create(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        uname = serializer.data.get('username')
        username = User.objects.get(username=uname)
        pwd = serializer.data.get('password')
        user = authenticate(username=username, password=pwd)

        token, created = Token.objects.get_or_create(user=user)
        if not user:
            return Response({'message': 'Invalid credentials'},
                            status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(data={'status': status.HTTP_200_OK, 'message': 'Success',
                                  'token': token.key}, status=status.HTTP_200_OK)


class PasswordResetView(viewsets.ViewSet):
    serializer_class = PasswordResetSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        ut.password_reset_link_email(email, request)
        return Response(data={"message": "Password reset email has been sent."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        token = request.GET.get('token')
        user = User.objects.filter(rp_otp=token).first()
        if user:
            return Response(data={'message': 'Success', 'token': token}, status=status.HTTP_200_OK)
        else:
            return Response(data={'message': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.data.get('password')
        token = serializer.data.get('token')
        user = User.objects.filter(rp_otp=token).first()
        if user:
            user.set_password(password)
            user.rp_otp = ''
            user.save()
            return Response(data={"message": "Your password has been reset successfully."}, status=status.HTTP_200_OK)
        else:
            return Response(data={'message': 'User not found'}, status=status.HTTP_401_UNAUTHORIZED)


class ChangePasswordView(viewsets.ViewSet):
    serializer_class = ChangePasswordSerializer
    http_method_names = ['post']
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        user.set_password(serializer.data.get("new_password"))
        user.save()
        return Response(data={'message': 'Password changed successfully'}, status=status.HTTP_200_OK)


class UserProfile(viewsets.ModelViewSet):
    http_method_names = ['get','delete']
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()

    def list(self, request, **kwargs):
        return Response(data=(self.serializer_class(request.user)).data)

    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'message': 'successful'}, status=status.HTTP_200_OK)


class UserProfileUpdate(viewsets.ModelViewSet):
    http_method_names = ['post']
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserProfileUpdateSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserProfileUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if User.objects.filter(email=serializer.data.get('email')).exclude(id=user.id).exists():
            return Response(data={'email error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=serializer.data.get('username')).exclude(id=user.id).exists():
            return Response(data={'username error': 'username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.data.get('phone'):
            if User.objects.filter(phone=serializer.data.get('phone')).exclude(id=user.id).exists():
                return Response(data={'phone error': 'phone number already exists'}, status=status.HTTP_400_BAD_REQUEST)
        # old_email = user.email
        user.first_name = serializer.data.get('first_name', user.first_name)
        user.last_name = serializer.data.get('last_name', user.last_name)
        user.email = serializer.data.get('email', user.email)
        user.save()
        user.username = serializer.data.get('username', user.username)
        user.save()
        # user.bio = serializer.data.get('bio', user.bio)
        old_num = user.phone
        if serializer.data.get('phone'):
            user.phone = serializer.data.get('phone')
        user.save()
        return Response(data={'message': 'updated'}, status=status.HTTP_200_OK)


class CategoryView(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    http_method_names = ['get']

    def list(self, request, **kwargs):
        # categoryObj = Category.get_annotated_list()
        categoryObj = Category.objects.all()
        if categoryObj:
            return Response({'data': self.serializer_class(categoryObj, many=True).data}, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "No results found"}, status=status.HTTP_200_OK)


class ServiceView(viewsets.ModelViewSet):
    http_method_names = ['get']
    permission_classes = (permissions.AllowAny,)
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


    def list(self, request, **kwargs):
        serviceObj = Service.objects.all()
        service = serviceObj.values('serviceName')
        return Response(data={'data': service, "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)


class SubcategoryView(viewsets.ModelViewSet):
    http_method_names = ['get']
    permission_classes = (permissions.AllowAny,)
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer

    # def list(self, request, **kwargs):
    #     subcategory = Subcategory.objects.all().values('subcategoryId','subcategoryName','categoryName')
    #     serializer = self.get_serializer(subcategory, many=True)
    #     return Response(data={'data':serializer.data ,"status": status.HTTP_200_OK}, status=status.HTTP_200_OK)


    def list(self, request, **kwargs):
        subcategoryObj = Subcategory.objects.all()
        # subcategoryObj = Subcategory.get_annotated_list()

        if subcategoryObj:
            return Response({'data': self.serializer_class(subcategoryObj, many=True).data}, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "No results found"}, status=status.HTTP_200_OK)


class ItemView(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete', 'patch']
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def create(self, request, *args, **kwargs):
        serializer = ItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        if Item.objects.filter(itemName=serializer.data.get('itemName')).exists():
            return Response(data={'Error': 'Item already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            service_id = serializer.data.get('serviceName')
            service = Service.objects.get(serviceId=service_id)
            category_id = serializer.data.get('categoryName')
            category = Category.objects.get(categoryId=category_id)
            subcategory_id = serializer.data.get('subcategoryName')
            subcategory = Subcategory.objects.get(subcategoryId=subcategory_id)

            city_id = serializer.data.get('cityName')
            city = City.objects.get(id=city_id)
            item = serializer.data.get('itemName')
            address = serializer.data.get('address')
            phone_number = serializer.data.get('phoneNumber')
            itemStatus = serializer.data.get('status')
            businessInfo = serializer.data.get('businessInfo')
            itemImage = serializer.validated_data.get('itemImage')
            print("item image",itemImage)
            time = serializer.data.get('availableTime')
            social_media_link = serializer.data.get('socialMediaLink')
            item_obj, created = Item.objects.get_or_create(item_addedBy=user,serviceName=service, categoryName=category, \
                                subcategoryName=subcategory,itemName=item,address=address,phoneNumber=phone_number, \
                                status=itemStatus, businessInfo=businessInfo,itemImage=itemImage,availableTime=time,\
                                socialMediaLink=social_media_link,cityName=city)
            item_obj.save()
            return Response(data={'message': 'Item saved successfully'}, status=status.HTTP_200_OK)


    def list(self, request, **kwargs):
        # itemObj = Item.objects.all().values('cityName','serviceName','categoryName','subcategoryName','itemName',
        #                        'address','phoneNumber','status','businessInfo','itemName','availableTime','socialMediaLink')
        itemObj = Item.objects.all()
        serializer = self.get_serializer(itemObj, many=True)
        return Response(data={'data': serializer.data, "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)


    def update(self, request, *args, **kwargs):
            itemObj = Item.objects.get(pk=kwargs['pk'])
            city = request.data.get('cityName')
            itemObj.cityName = City.objects.get(id=city)
            service = request.data.get('serviceName')
            itemObj.serviceName = Service.objects.get(serviceId=service)
            category = request.data.get('categoryName')
            itemObj.categoryName = Category.objects.get(categoryId=category)
            subcategory = request.data.get('subcategoryName')
            itemObj.subcategoryName = Subcategory.objects.get(subcategoryId=subcategory)
            itemObj.itemName = request.data.get('itemName')
            itemObj.address = request.data.get('address')
            itemObj.phoneNumber = request.data.get('phoneNumber')
            itemObj.status = request.data.get('status')
            itemObj.businessInfo = request.data.get('businessInfo')
            itemObj. itemImage = request.data.get('item_image')
            itemObj.availableTime = request.data.get('availableTime')
            itemObj.socialMediaLink = request.data.get('socialMediaLink')
            itemObj.save()
            return Response(data={'message': 'Item updated', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Item deleted successfully'}, status=status.HTTP_200_OK)


class ReviewView(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch']
    permission_classes = (permissions.AllowAny,)
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        item_id = serializer.data.get('item_id')
        itemName = Item.objects.get(itemId=item_id)
        comment = serializer.data.get('comment')
        review_obj, created = Review.objects.get_or_create(reviewBy=user,item=itemName,comment=comment)
        review_obj.save()
        return Response(data={"message": "Review Added successfuly"}, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        reviewObj = Review.objects.all()
        if reviewObj:
            return Response({'review': self.serializer_class(reviewObj, many=True).data},
                            status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "No results found"}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
            reviewObj = Review.objects.get(pk=kwargs['pk'])
            reviewObj.rating = request.data.get('rating')
            reviewObj.save()
            return Response(data={'message': 'success', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)


class SearchItemView(viewsets.ViewSet):
    http_method_names = ['get']
    permission_classes = (permissions.AllowAny,)
    serializer_class = ItemSearchSerializer

    def list(self, request):
        try:

            text = request.GET.get('q', '')
            search_result = Item.objects.filter(
                Q(serviceName__serviceName__icontains=text) | Q(categoryName__categoryName__icontains=text) |
                Q(subcategoryName__subcategoryName__icontains=text) |
                Q(itemName__icontains=text) | Q(cityName__cityName__icontains=text))
            if search_result is not None:
                serializer = self.serializer_class(search_result, many=True, context={'request': request})
                return Response(data=serializer.data, status=status.HTTP_200_OK)

        except:
            return Response(data={'message': 'Error Fetching details !'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
