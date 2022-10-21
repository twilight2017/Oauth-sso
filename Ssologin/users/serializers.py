from rest_framework import serializers
from .models import Article
from django.contrib.auth import get_user_model

User = get_user_model()


class ArticleSerializer(serializers.Serializer):
    author = serializers.ReadOnlyField(source="author.name")
    full_status = serializers.ReadOnlyField(source="get_status_display")
    cn_status = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('id', 'author', 'create_date')

    def get_cn_status(self, obj):
        if obj.status == 'p':
            return "已发表"
        elif obj.status == 'd':
            return "草稿"
        else:
            return ''


class UserSerializer(serializers.Serializer):
    profile = ProfileSerializer()

    class Meta:
        model=User
        field=('username', 'email', 'profile')

    def create(self, validate_data):
        profile_data = validate_data.pop('profile')
        user = User.objects.create(**validate_data)
        Profil