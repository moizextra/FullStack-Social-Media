from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.models import Post
from .models import Comment
from .serializers import CommentSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def comment_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'GET':
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, c_auther=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)