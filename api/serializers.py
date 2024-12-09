

from rest_framework import serializers

from django.contrib.auth.models import User

from api.models import Post,Comment



class UserSerializer(serializers.ModelSerializer):

    password1=serializers.CharField(write_only=True)

    password2=serializers.CharField(write_only=True)


    class Meta:

        model=User

        fields=["id","username","email","password","password1","password2"]

        read_only_fields=["password"]


    def create(self,validated_data):

        password1=validated_data.pop("password1")

        password2=validated_data.pop("password2")

        if password1!=password2:

            raise serializers.ValidationError("password missa match")

        return User.objects.create_user(**validated_data,password=password1)
    


class LoginSerializer(serializers.Serializer):

    username=serializers.CharField()

    password=serializers.CharField()



class PostSerializer(serializers.ModelSerializer):

    likes=serializers.SerializerMethodField(method_name="get_like_count",read_only=True)

    liked_by=serializers.StringRelatedField(many=True)

    comment_count=serializers.SerializerMethodField(method_name="get_comment_count",read_only=True)

    comments=serializers.SerializerMethodField(method_name="get_comments",read_only=True)

    class Meta:

        model=Post

        fields="__all__"

        read_only_fields=["id","owner","liked_by","created_date","updated_date","is_active"]

    def get_like_count(self,object):

        return object.liked_by.all().count()
    
    def get_comment_count(self,object):

        return Comment.objects.filter(post_object=object).count()
    
    def get_comments(self,object):

        qs=Comment.objects.filter(post_object=object) #query set => python native type

        serializer_instance=CommentSerializer(qs,many=True)

        return serializer_instance.data












class CommentSerializer(serializers.ModelSerializer):

    owner=serializers.StringRelatedField(read_only=True)


    class Meta:

        model=Comment

        fields="__all__"

        read_only_fields=[
            "id",
            "owner",
            "post_object",
            "created_date",
            "updated_date",
            "is_active"
        ]
