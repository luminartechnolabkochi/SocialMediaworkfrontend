from django.db import models

from django.contrib.auth.models import User

from django.db.models.signals import post_save


class BaseModel(models.Model):

    created_date=models.DateTimeField(auto_now_add=True)

    update_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)


class UserProfile(BaseModel):

    bio=models.CharField(max_length=200,null=True)

    profile_picture=models.ImageField(upload_to="profilepictures",null=True)

    address=models.TextField(null=True)

    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")

class Post(BaseModel):

    caption=models.CharField(max_length=200)

    picture=models.ImageField(upload_to="postimages",null=True)

    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")

    liked_by=models.ManyToManyField(User,related_name="likes")

    def __str__(self):

        return self.caption
    

class Comment(BaseModel):

    owner=models.ForeignKey(User,on_delete=models.CASCADE)

    message=models.CharField(max_length=200)

    post_object=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")

    def __str__(self):

        return self.message
  


def create_profile(sender,instance,created,**kwargs):

    if created:

        UserProfile.objects.create(owner=instance)



post_save.connect(create_profile,User)



    





