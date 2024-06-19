from rest_framework import serializers

from .models import MyLinks, MyToken


class MytokensSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyToken
        fields = ['doc_id', 'tokens']


class MylinksSerializer(serializers.ModelSerializer):
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = MyLinks
        fields = ['id', 'link', 'title', 'icon', 'body', 'tokens']

    def get_tokens(self, obj):
        tokens = MyToken.objects.filter(doc_id=obj.id).values_list('tokens', flat=True)
        return tokens
