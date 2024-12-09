from django.shortcuts import render

from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView,RetrieveUpdateDestroyAPIView

from api.serializers import UserSerializer,LoginSerializer,PostSerializer,CommentSerializer

from rest_framework.views import APIView

from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token

from rest_framework.response import Response

from rest_framework import authentication,permissions

from api.models import Post,Comment

class SignUpView(CreateAPIView):

    serializer_class=UserSerializer


class GetTokenView(APIView):

    serializer_class=LoginSerializer

    def post(self,request,*args,**kwargs):

        serializer_instance=self.serializer_class(data=request.data)

        if serializer_instance.is_valid():

            uname=serializer_instance.validated_data.get("username")

            pwd=serializer_instance.validated_data.get("password")

            user_object=authenticate(request,username=uname,password=pwd)

            if user_object:

                token,created=Token.objects.get_or_create(user=user_object)
                
                return Response(data=token.key)
        return Response(data={"message":"invalid credential"})
                                

class PostListCreateView(ListAPIView,CreateAPIView):

    queryset=Post.objects.all()

    serializer_class=PostSerializer

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        
        return serializer.save(owner=self.request.user)
    

class PostDetailView(RetrieveAPIView):

    serializer_class=PostSerializer

    queryset=Post.objects.all()

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]


class AddLikeView(APIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        post_object=Post.objects.get(id=id)

        if request.user in post_object.liked_by.all():

            post_object.liked_by.remove(request.user)
        else:
            post_object.liked_by.add(request.user)
        


        return Response(data={"message":"liked"})
    



class AddCommentView(CreateAPIView):


    serializer_class=CommentSerializer

    
    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]


    def perform_create(self, serializer):
        
        id=self.kwargs.get("pk")

        post_object=Post.objects.get(id=id)

        serializer.save(owner=self.request.user,post_object=post_object)



class CommentRetrieveUpdateDeleteView(RetrieveAPIView,UpdateAPIView,DestroyAPIView):

    serializer_class=CommentSerializer

    queryset=Comment.objects.all()

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]




# FrontEnd (React)

# Monday

