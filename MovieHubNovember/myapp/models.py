from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Genres(models.Model):
    genre=models.CharField(max_length=120,unique=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.genre

class Movies(models.Model):
    name=models.CharField(max_length=250,unique=True)
    genres=models.ManyToManyField(Genres,null=True)
    year=models.CharField(max_length=200)
    options=(
        ("malayalam","malayalam"),
        ("telungu","telungu"),
        ("thamil","thamil"),
        ("english","english"),
        ("hindi","hindi")
    )
    language=models.CharField(max_length=200,choices=options,default="malayalam")
    runtime=models.FloatField()
    poster_image=models.ImageField(upload_to="images",null=True,blank=True)
    description=models.CharField(max_length=200,null=True)

    @property
    def genre_names(self):
        return self.genres.all()
    
    @property
    def reviews(self):
        return Reviews.objects.filter(movie=self)
    @property
    def avg_rating(self):
        ratings=Reviews.objects.filter(movie=self).values_list("rating",flat=True)
        return sum(ratings)/len(ratings) if ratings else 0

    def __str__(self):
        return self.name
    
class Reviews(models.Model):
    movie=models.ForeignKey(Movies,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comment=models.CharField(max_length=200)
    rating=models.PositiveIntegerField()
    


    


