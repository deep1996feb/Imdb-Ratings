from django.urls import path, include
#from watchme.apis.views import movie_list, movie_details  #Used fir Function based API
from rest_framework.routers import DefaultRouter
from watchme.apis.views import WatchListView, WatchListDetailView, StreamPlatformList, StreamDetailView, ReviewsList, ReviewDetails, ReviewCreate, StreamPlatFormVS
router = DefaultRouter()

router.register('stream', StreamPlatFormVS, basename='streamplatform')


urlpatterns = [
    # path('list/', movie_list, name='movie_list'),
    # path('<int:pk>', movie_details, name='movie_details'), #For Function Based.

    path('list/', WatchListView.as_view(), name='movielist'),
    path('<int:pk>/', WatchListDetailView.as_view(), name='moviedetail'),
    #path('stream/', StreamPlatformList.as_view(), name='Streamlist'),
    #path('stream/<int:pk>/', StreamDetailView.as_view(), name='streamdetail'), #We comment this because we use default router for this two urls

    path('', include(router.urls)), #Do not use ' ' in router.urls


    path('<int:pk>/reviews/', ReviewsList.as_view(), name='review_list'), #For a Particular Movie
    path('reviews/<int:pk>/', ReviewDetails.as_view(), name='review-details'), #For Individual Review
    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    #path('reviews/',  ReviewsList.as_view(), name='review-list'),
    #path('reviews/<int:pk>', ReviewDetails.as_view(), name='review-detail'),
    
]



#.as_view() is basically used in class based APIVIEW
