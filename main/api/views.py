from rest_framework import views, generics, status, response
from django.urls import path
from main.api.serializers import *
from auth.middleware import view_allow_any, view_authenticate
from extensions.helpers import serializer_to_json
from extensions.mixins import APIViewMixin


@view_authenticate()
class AddNewInterestView(APIViewMixin, generics.CreateAPIView):
    serializer_class = AddInterestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        interest = serializer.validated_data

        result = {
            'interest': interest.name,
        }

        return self.get_response(message='Successfully Added Interest', result=result)


@view_authenticate()
class AddInterestView(APIViewMixin, generics.CreateAPIView):
    serializer_class = AddUserInterestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)

        return self.get_response(message='Successfully Added Interest')


@view_authenticate()
class ListUserInterests(APIViewMixin, generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        user = self.request.current_user
        interests_list = serializer_to_json(ListInterestSerializer, user.interests.all())
        message = 'Successfully Retrieved Interests for user {}'.format(user.user_name)

        return self.get_response(message=message, result=interests_list)

# Followers
@view_authenticate()
class FollowUserView(APIViewMixin, generics.CreateAPIView):
    serializer_class = FollowUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        result = serializer.validated_data

        return self.get_response(message='Successfully Followed User', result={'followed': result.user_name, 'me': self.request.current_user.user_name})


@view_authenticate()
class ListUserFollowedView(APIViewMixin, generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        user = self.request.current_user
        interests_list = serializer_to_json(ListUsersSerializer, user.get_followed)
        message = 'Successfully Retrieved Followed users for {}'.format(user.user_name)

        return self.get_response(message=message, result=interests_list)


@view_authenticate()
class ListUserMatchesView(APIViewMixin, generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        user = self.request.current_user
        message = 'Successfully Most Similar Matches for {}'.format(user.user_name)

        return self.get_response(message=message, result=user.get_matches())


urlpatterns = [
    # user

    path('me/matches/', ListUserMatchesView.as_view(), name='list_matches'),

    # matches
    path('me/interest/add_new/', AddNewInterestView.as_view(), name='add_new_interest'),
    path('me/interest/add/', AddInterestView.as_view(), name='add_interest'),

    path('me/interest/list/all', ListUserInterests.as_view(), name='list_all_interest'),
    path('me/interest/list/', ListUserInterests.as_view(), name='list_interest'),

    # followers
    path('me/follow/user/', FollowUserView.as_view(), name='follow_user'),
    path('me/follow/all/', ListUserFollowedView.as_view(), name='all_people_followed'),



]
