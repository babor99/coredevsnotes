from django.shortcuts import render
from django.contrib import auth
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
import jwt
import datetime

from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .permissions import CustomDjangoModelPermissions
from .models import *
from .serializers import *
# Create your views here.

class CustomTokenObtainView(generics.GenericAPIView):
    serializer_class = UserSerializer
    def post(self, request):
        data = request.data
        if not data:
            return Response({'error': True, 'message': 'No data provided'})
        username = data['username']
        password = data['password']

        user = auth.authenticate(username=username, password=password)

        if user:
            auth_token = jwt.encode({'username':user.username}, settings.JWT_SECRET_KEY, algorithm="HS256")
            serializer = UserSerializer(user)
            data = {'error':False,'user':serializer.data, 'token':auth_token}
            return Response(data)
        else:
            return Response({'error':True,'message':'Invalid credentials given.'})



class SignupViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny,]
    def create(self, request):
        print('signup request: ', request.data)
        _username = request.data['username']
        password = request.data['password1']
        password2 = request.data['password2']
        all_users = User.objects.all()
        for user in all_users:
            if user.username == _username:
                return Response({'error':True, 'message':f"username {_username} already taken. Choose another username."})
        if password == password2:
            user_obj = User.objects.create_user(username=_username, password=password)
            user_obj.groups.add(2)
            user_obj.save()
            profile_obj = Profile.objects.create(user=user_obj)
            profile_obj.save()
            res = {'error':False, 'message':'Success! Signup successful'}
        else:
            res = {'error':True, 'message':'Failed! Signup unsuccessful',}
        return Response(res)
        return Response({'message':'hello'})
        


class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def list(self, request):
        subscribed_users = Profile.objects.filter(is_subscribed=True)
        total_subscribed_users = len(subscribed_users)
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True, context={'request':request})
        if request.user.is_authenticated:
            return Response({'error':False, 'message':"Success! Profile data fetched successfully.", 'total_subscribed_users':total_subscribed_users, 'data':serializer.data})
        else:
            return Response({'error':True, 'message':"Failed! Can't fetch Profile data."})
    
    def retrieve(self, request, pk=None):
        user_obj = User.objects.get(id=pk)
        profile = Profile.objects.get(user=request.user)
        user_subscriptions = UserSubscription.objects.filter(user=request.user)
        if len(user_subscriptions) >= 1:
            profile.is_subscribed = True
            profile.save()
        serializer = ProfileSerializer(profile, context={'request':request})
        if request.user.is_authenticated:
            return Response({'error':False, 'message':"Success! Profile data retrieved successfully.", 'data':serializer.data})
        else:
            return Response({'error':True, 'message':"Failed! Cann't fecth single Profile data."})

    def create(self, request):
        data = request.data
        try:
            serializer = ProfileSerializer(data=data, context={'request':request})
            serializer.is_valid()
            if request.user.is_authenticated:
                serializer.save()
            res = {'error':False, 'message':'Success! Profile data saved successfully.'}
        except:
            res = {'error':True, 'message':'Failed! Error during saving Profile data.'}
        return Response(res)
    
    def update(self, request, pk=None):
        try:
            user_obj = User.objects.get(id=pk)
            print(user_obj)
            user_obj.first_name = request.data['first_name']
            user_obj.last_name = request.data['last_name']
            user_obj.email = request.data['email']
            if request.user.is_authenticated:
                user_obj.save()
                res = {'error':False, 'message':'Success! Profile data updated successfully.'}
        except Exception as e:
            res = {'error':True, 'message':"Failed! Can't update Profile data."}
            print(e)
        return Response(res)

    def destroy(self, request, pk=None):
        class_obj = Profile.objects.get(id=pk)
        print('id ', pk)
        if request.user.is_authenticated:
            class_obj.delete()
            res = {'error':False, 'message':'Success! Profile data has been deleted.'}
        else:
            res = {'error':True, 'message':"Failed! Can't delete Profile data."} 
        return Response(res)



class NotesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]
    queryset = Note.objects.all()
    serializer_class = NotesSerializer

    def list(self, request):
        user = request.user
        user_dict = {}
        user_group = UserSerializer(user).data
        for key, value in user_group.items():
            user_dict[key] = value
        if int(user_dict['groups'][0]) == 1:
            _today = datetime.date.today()
            today_notes = Note.objects.filter(created_at__date=_today)
            today_notes = len(today_notes)
            queryset = Note.objects.all()
            serializer = NotesSerializer(queryset, many=True, context={'request':request})
            if request.user.is_authenticated:
                return Response({'error':False, 'message':"Success! Note data fetched successfully.", 'today_notes':today_notes, 'data':serializer.data})
        elif int(user_dict['groups'][0]) == 2:
            queryset = Note.objects.filter(user=user)
            serializer = NotesSerializer(queryset, many=True, context={'request':request})
            if request.user.is_authenticated:
                return Response({'error':False, 'message':"Success! Note data fetched successfully.", 'data':serializer.data})
        
        return Response({'error':True, 'message':"Failed! Can't fetch Note data."})
    
    def retrieve(self, request, pk=None):
        queryset = Note.objects.get(id=pk)
        serializer = NotesSerializer(queryset, context={'request':request})
        if request.user.is_authenticated:
            return Response({'error':False, 'message':"Success! Note data retrieved successfully.", 'data':serializer.data})
        else:
            return Response({'error':True, 'message':"Failed! Cann't fecth single Note data."})

    def create(self, request):
        user = request.user
        _delta = datetime.timezone(datetime.timedelta(hours=0))
        _today = datetime.date.today()
        if request.user.is_authenticated:
            user_subs = UserSubscription.objects.filter(user=user)
            if len(user_subs) == 0:
                pass
            elif len(user_subs) > 0:
                user_sub = user_subs[0]

                today_notes = Note.objects.filter(user=user, created_at__date=_today )
                print(_today)
                print('today notes :', today_notes)
                print(user_sub.subscription_id.day_limit)
                if user_sub.subscription_id.day_limit == 1:
                    print(len(today_notes))
                    if len(today_notes) <= 2:
                        note_obj = Note.objects.create(user=user, title=request.data['title'], date=request.data['date'])
                        note_obj.save()
                        return Response({'error':False, 'message':'Success! Note data saved successfully.'}) 
                    else:
                        return Response({'error':True, 'message':f"You have reached your per day notes creation limit of 3. Please try next day or subscribe to a better package"})
                elif user_sub.subscription_id.day_limit == 4:
                    if len(today_notes) <= 7:
                        note_obj = Note.objects.create(user=user, title=request.data['title'], date=request.data['date'])
                        note_obj.save()
                        return Response({'error':False, 'message':'Success! Note data saved successfully.'}) 
                    else:
                        return Response({'error':True, 'message':f"You have reached your per day notes creation limit of 8. Please try next day or subscribe to a better package"})
                elif user_sub.subscription_id.day_limit == 7:
                    if len(today_notes) <= 11:
                        note_obj = Note.objects.create(user=user, title=request.data['title'], date=request.data['date'])
                        note_obj.save()
                        return Response({'error':False, 'message':'Success! Note data saved successfully.'}) 
                    else:
                        return Response({'error':True, 'message':f"You have reached your per day notes creation limit of 12. Please try next day or subscribe to a better package"})
                elif user_sub.subscription_id.day_limit == 30:
                    if len(today_notes) <= 19:
                        note_obj = Note.objects.create(user=user, title=request.data['title'], date=request.data['date'])
                        note_obj.save()
                        return Response({'error':False, 'message':'Success! Note data saved successfully.'}) 
                    else:
                        return Response({'error':True, 'message':f"You have reached your per day notes creation limit of 20. Please try next day or subscribe to a better package"})

        return Response({'error':True, 'message':'Failed! Error during saving Note data.'})
    
    def partial_update(self, request, pk=None):
        try:
            note_obj = Note.objects.get(id=pk)
            note_obj.user = request.user
            note_obj.title = request.data['title']
            note_obj.date = request.data['date']
            note_obj.save()
            res = {'error':False, 'message':'Success! Note data updated successfully.'}
        except:
            res = {'error':True, 'message':"Failed! Can't update Note data."}
        return Response(res)

    def destroy(self, request, pk=None):
        note_obj = Note.objects.get(id=pk)
        if request.user.is_authenticated:
            note_obj.delete()
            res = {'error':False, 'message':'Success! Note data has been deleted.'}
        else:
            res = {'error':True, 'message':"Failed! Can't delete Note data."} 
        return Response(res)



class SubscriptionsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionsSerializer

    def list(self, request):
        queryset = Subscription.objects.all()
        serializer = SubscriptionsSerializer(queryset, many=True, context={'request':request})
        if request.user.is_authenticated:
            return Response({'error':False, 'message':"Success! Subscription data fetched successfully.", 'data':serializer.data})
        else:
            return Response({'error':True, 'message':"Failed! Can't fetch Subscription data."})
    
    def retrieve(self, request, pk=None):
        queryset = Subscription.objects.get(id=pk)
        serializer = SubscriptionsSerializer(queryset, context={'request':request})
        if request.user.is_authenticated:
            return Response({'error':False, 'message':"Success! Subscription data retrieved successfully.", 'data':serializer.data})
        else:
            return Response({'error':True, 'message':"Failed! Cann't fecth single Subscription data."})

    def create(self, request):
        data = request.data
        title = request.data['title']
        subscription_type = request.data['subscription_type']
        day_limit = request.data['day_limit']
        price = request.data['price']
        description = request.data['description']
        try:
            subs_obj = Subscription.objects.create( title=title, subscription_type=subscription_type, day_limit=day_limit, price=price, description=description)
            if request.user.is_authenticated:
                subs_obj.save()
            res = {'error':False, 'message':'Success! Note data saved successfully.'}
            return Response(res)
        except:
            res = {'error':True, 'message':'Failed! Error during saving Note data.'}
        return Response(res)
    
    def update(self, request, pk=None):
        try:
            data = request.data
            queryset = Subscription.objects.get(id=pk)
            serializer = SubscriptionsSerializer(queryset, data=data, context={'request':request})
            serializer.is_valid()
            serializer.save()
            res = {'error':False, 'message':'Success! Subscription data updated successfully.'}
        except:
            res = {'error':True, 'message':"Failed! Can't update Subscription data."}
        return Response(res)

    def destroy(self, request, pk=None):
        class_obj = Subscription.objects.get(id=pk)
        print('id ', pk)
        if request.user.is_authenticated:
            class_obj.delete()
            res = {'error':False, 'message':'Success! Subscription data has been deleted.'}
        else:
            res = {'error':True, 'message':"Failed! Can't delete Subscription data."} 
        return Response(res)



class UserSubscriptionsViewSet(viewsets.ModelViewSet):
    permission_classes = [ IsAuthenticated, CustomDjangoModelPermissions ]
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionsSerializer

    def list(self, request):
        user_subs = UserSubscription.objects.filter(user=request.user)
        profile_obj = Profile.objects.get(user=request.user)
        if len(user_subs) == 0:
            serializer = UserSubscriptionsSerializer(user_subs, many=True, context={'request':request})
            profile_obj.is_subscribed = False
            profile_obj.save()
            return Response({'error':False, 'message':"Success! UserSubscription data fetched successfully.", 'data':serializer.data})
        elif len(user_subs) > 0:
            user_subs = user_subs[0]
            expiry_date = user_subs.created_at + datetime.timedelta(days=user_subs.subscription_id.day_limit)
            _delta = datetime.timezone(datetime.timedelta(hours=0))
            _today = datetime.datetime.now(tz=_delta)
            if request.user.is_authenticated:
                if _today >= expiry_date:
                    profile_obj.is_subscribed = False
                    profile_obj.save()
                    user_subs.delete()
                else:
                    queryset = UserSubscription.objects.filter(user=request.user)
                    serializer = UserSubscriptionsSerializer(queryset, many=True, context={'request':request})
                    return Response({'error':False, 'exp_date':expiry_date, 'message':"Success! UserSubscription data fetched successfully.", 'data':serializer.data})
        else:
            return Response({'error':True, 'message':"Failed! Can't fetch UserSubscription data."})
      

    def retrieve(self, request, pk=None):
        queryset = UserSubscription.objects.get(id=pk)
        serializer = UserSubscriptionsSerializer(queryset, context={'request':request})
        if request.user.is_authenticated:
            return Response({'error':False, 'message':"Success! UserSubscription data retrieved successfully.", 'data':serializer.data})
        else:
            return Response({'error':True, 'message':"Failed! Cann't fecth single UserSubscription data."})

    def create(self, request):
        subs_id = request.data['subs_id']
        print('subs_id :',subs_id)
        try:
            subscription_obj = Subscription.objects.get(id=subs_id)
            user_all_subs = UserSubscription.objects.filter(user=request.user)
            if request.user.is_authenticated:
                if len(user_all_subs) >= 1:
                    return Response({'error':True, 'message':"You have already a subscription. To subscribe to a new package, unsubscribe from the previous one."})
                else:
                    user_subscription = UserSubscription.objects.create(user=request.user, subscription_id=subscription_obj)
                    user_subscription.save()
                    res = {'error':False, 'message':'Success! UserSubscription successful.'}
        except:
            res = {'error':True, 'message':'Failed! Error during saving UserSubscription data.'}
        return Response(res)
    
    def update(self, request, pk=None):
        try:
            data = request.data
            queryset = UserSubscription.objects.get(id=pk)
            serializer = UserSubscriptionsSerializer(queryset, data=data, context={'request':request})
            serializer.is_valid()
            serializer.save()
            res = {'error':False, 'message':'Success! UserSubscription data updated successfully.'}
        except:
            res = {'error':True, 'message':"Failed! Can't update UserSubscription data."}
        return Response(res)

    def destroy(self, request, pk=None):
        user_subs_obj = UserSubscription.objects.get(id=pk)
        if request.user.is_authenticated:
            user_subs_obj.delete()
            total_user_subs = UserSubscription.objects.filter(user=request.user)
            user_profile = Profile.objects.get(user=request.user)
            if len(total_user_subs) == 0:
                user_profile.is_subscribed = False
            elif len(total_user_subs) > 0:
                user_profile.is_subscribed = True
            user_profile.save()
            res = {'error':False, 'message':'Success! You have been unsubscribed'}
        else:
            res = {'error':True, 'message':"Failed! Can't delete UserSubscription data."} 
        return Response(res)



class NotesFullCalendarViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]
    queryset = Note.objects.all()
    serializer_class = NotesSerializer

    def list(self, request):
        user = request.user
        queryset = Note.objects.filter(user=user)
        serializer = NotesFullCalendarSerializer(queryset, many=True, context={'request':request})
        if request.user.is_authenticated:
            return Response({'error':False, 'message':"Success! Note data fetched successfully.", 'data':serializer.data})
        else:
            return Response({'error':True, 'message':"Failed! Can't fetch Note data."})



class SubscriptionTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, CustomDjangoModelPermissions]
    queryset = SubscriptionType.objects.all()
    serializer_class = SubscriptionTypeSerializer

    # def list(self, request):
    #     user = request.user
    #     queryset = Note.objects.filter(user=user)
    #     serializer = NotesFullCalendarSerializer(queryset, many=True, context={'request':request})
    #     if request.user.is_authenticated:
    #         return Response({'error':False, 'message':"Success! Note data fetched successfully.", 'data':serializer.data})
    #     else:
    #         return Response({'error':True, 'message':"Failed! Can't fetch Note data."})