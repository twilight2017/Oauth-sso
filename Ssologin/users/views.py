from django.shortcuts import render
from . import forms
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Article
from .serializers import ArticleSerializer


@api_view(['GET', 'POST'])
def article_list(request, format=None):
    """
    List all articels, or create a new article
    :param request:
    :return:
    """
    if request.method == 'GET':
        articles = Article.objetcs.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # 用post中携带的数据更新article列表
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            # Very important, Associate request.user with author
            serializer.save(author=request.user)  # read-only字段在创建article实例时进行手动绑定
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


# 单个article的相关功能
@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, pk, format=None):
    """
    Retrieve: update or delete an article instance
    :param request:
    :param pk:
    :return:
    """
    try:
        article = Article.objetcs.get(pk=pk)
    except Article:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serilizer = ArticleSerializer(article, request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data)
        return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
