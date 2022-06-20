#from re import M
from distutils.file_util import move_file
from multiprocessing import context
from platform import platform
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from watchme.apis.serializers import StreamPlatformSerializer,  WatchListSerializer, ReviewSerializer
from watchme .models import Watch_List, StreamPlatform, Review
from rest_framework.response import Response
#from rest_framework.decorators import api_view #It used in Function based class
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from watchme.apis.permissions import AdminOrReadOnly, ReviewUserOrReadOnly
# <Function Based API starts>


# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movies.objects.all()
#         serializer = MovieSerializer(movies, many=True) #Many=True is used when we have multiple objects to show.
#         return Response(serializer.data)
#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):
#     if request.method == 'GET':
#         try:
#             movie = Movies.objects.get(pk=pk)
#         except Movies.DoesNotExist:
#             return Response({'Error': 'Movie Not Found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     if request.method == 'PUT':
#         movie = Movies.objects.get(pk=pk)
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
#     if request.method == 'DELETE':
#         movie = Movies.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


#      <Function Based API Ends>



# <Class based APIVIEW Starts>

# <ConCrete View Classes>

class ReviewCreate(generics.CreateAPIView):  #Only Post method allowed not GET.
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.all()
        
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = Watch_List.objects.get(pk=pk)

        review_user = self.request.user  #It is use because the same user could not post the review the second time of the same movie.
        review_queryset = Review.objects.filter(watchlist=movie, review_user = review_user )
        if review_queryset.exists():
            raise ValidationError('You already reviewed this movie.')

        if movie.number_ratings == 0:
            movie.avg_rating = serializer.validated_data['ratings']
        else:
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['ratings'])/2
            movie.number_ratings = movie.number_ratings + 1
            movie.save()
            serializer.save(watchlist=movie, review_user=review_user)
        


class ReviewsList(generics.ListAPIView):  #It gives Post and Get methods just in two lines of codes
   # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)

class ReviewDetails(generics.RetrieveUpdateDestroyAPIView): #It give put, delete, get methods to us just in two lines of codes.
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]

#  <Using Generics and Mixin to create a review class>

# class ReviewDetails(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

# class ReviewsList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class =  ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

class WatchListView(APIView):
    def get(self, request):
        movies = Watch_List.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WatchListDetailView(APIView):
    def get(self, request,pk):
        try:
            movie = Watch_List.objects.get(pk=pk)
        except Watch_List.DoesNotExist:
            return Response({'Error': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        movie = Watch_List.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = Watch_List.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Using Viewsets in StreamPlatFormLisList and StreamDetailView
# <Start ViewList in Stream>

#Note: A ModelViewset can perform all the things like GET PoST DELETE UPDATE


class StreamPlatFormVS(viewsets.ModelViewSet):
     queryset = StreamPlatform.objects.all()
     serializer_class = StreamPlatformSerializer


#< Start viewsets.Viewset >
# class StreamPlatFormVS(viewsets.ViewSet):

#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)

#     def create(self,request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# <end of viewsets.Viewset>

class StreamPlatformList(APIView):
    def get(self, request):
        platform = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platform, many=True) # context = {request:request} It used when we used HyperlinkRelatedfield
        return Response(serializer.data)

    def post(self,request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class StreamDetailView(APIView):
    def get(self, request,pk):
        try:
            movie = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'Error': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        serializer =StreamPlatformSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        movie = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = StreamPlatform.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)