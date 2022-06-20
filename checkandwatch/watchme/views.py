# from django.shortcuts import render
# from .models import Movies
# from django.http import  JsonResponse
# # Create your views here.

# def MovieList(request):
#     movies = Movies.objects.all()
#     data = {
#         'movies': list(movies.values())
#         }

#     return JsonResponse(data)

# def MoviesDetail(request, pk):
#     movie = Movies.objects.get(pk=pk)
#     data = {
#         'name' : movie.name,
#         'description' : movie.description,
#         'active' : movie.active 
#     }
#     return JsonResponse(data)