from django.contrib.auth.models import Group
from rest_framework import serializers

from control_panel_api.models import App, S3Bucket, User


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'name', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'url', 'name')


class AppSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = App
        fields = ('id', 'url', 'name', 'slug', 'repo_url')


class S3BucketSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = S3Bucket
        fields = ('id', 'url', 'name', 'arn')
