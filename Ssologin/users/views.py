from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from .models import Article
from rest_framework import status
from .serializers import ArticleSerializer


class ArticleList(APIView):
    """
    List all articles, or create a new article
    """
    def get(self, request, format=None):
        articles = Article.objetcs.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer= ArticleSerializer(data=request.data)
        if serializer.is_valid():
            # 注意，手动绑定author
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticelDetail(APIView):
    """
    Retrieve, update or delete an article instance
    """
    def get_object(self, pk):
        try:
            return Article.objetcs.get(pk=pk)
        except Article.DoesNotExist:
            raise 404

    def get(self, request, pk, format=None):
        article = self.get_object(pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        article = self.get_object(pk=pk)
        serializer = ArticleSerializer(instance=article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        article= self.get_object(pk=pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
