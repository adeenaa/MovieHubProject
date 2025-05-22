from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin
from rest_framework import authentication,permissions
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.serializers import UserSerializer,MovieSerializer,ReviewSerializer,GenrereadSerializer
from myapp.models import Movies,Reviews,Genres

# Create your views here.

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user==obj.user
    
class UsersView(ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()
    model=User
    http_method_names=["post"]

class MovieView(GenericViewSet,ListModelMixin,RetrieveModelMixin):
    serializer_class=MovieSerializer
    queryset=Movies.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    #authentication_classes=[JWTAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    @action(methods=["post"],detail=True)
    def add_review(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        movie_obj=Movies.objects.get(id=id)
        user_obj=request.user
        serializer=ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(movie=movie_obj,user=user_obj)
            return Response(data=serializer.data)
        return Response(data=serializer.errors)
    
    @action(methods=["get"],detail=False)
    def genres(self,request,*args,**kwargs):
        qs=Genres.objects.all().values_list("genre",flat=True).distinct()
        return Response(data=qs)
    def list(self,request,*args,**kwargs):
        qs=Movies.objects.all()
        if "genre" in request.query_params:
            genre_name=request.query_params.get("genre")
            genre_obj=Genres.objects.get(genre=genre_name)
            qs=genre_obj.movies_set.all()
        serializer=MovieSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    
class ReviewView(GenericViewSet,UpdateModelMixin,DestroyModelMixin):
    serializer_class=ReviewSerializer
    queryset=Reviews.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    #authentication_classes=[JWTAuthentication]
    permission_classes=[IsOwner]