from base64 import b64decode
from uuid import uuid4

from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from django.utils.text import slugify

from rest_framework import serializers

from momus.models import UserProfile, Post


class ImageBase64Field(serializers.ImageField):
    def to_internal_value(self, data):
        try:
            decoded_image = b64decode(data.split(',')[1])
        except TypeError:
            raise serializers.ValidationError('Niepoprawny format zdjęcia.')
        data = ContentFile(decoded_image, name=str(uuid4()) + '.png')
        return super(ImageBase64Field, self).to_internal_value(data)


class UserSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')

    class Meta:
        model = User
        fields = ('username', 'firstName', 'lastName', 'email')
        read_only_fields = ('email', 'username')


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    birthDate = serializers.DateField(source='birth_date', allow_null=True, read_only=True)
    photo = ImageBase64Field()

    class Meta:
        model = UserProfile
        fields = ('user', 'photo', 'city', 'description', 'birthDate')

    def update(self, instance, validated_data):
        try:
            user_data = validated_data.pop('user')
        except KeyError:
            user_data = {}
        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name')

        if first_name:
            instance.user.first_name = first_name
        if last_name:
            instance.user.last_name = last_name

        if last_name or first_name:
            instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class PostSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)
    isPending = serializers.BooleanField(source='is_pending', read_only=True)
    tags = serializers.ListField(child=serializers.CharField(max_length=20, allow_blank=True))
    image = ImageBase64Field()

    class Meta:
        model = Post
        fields = ('author', 'title', 'slug', 'image', 'rate', 'tags', 'isPending')
        read_only_fields = ('slug', 'rate')

    def create(self, validated_data):
        slug = slugify(validated_data['title'])
        number = 0
        while Post.objects.filter(slug=slug).exists():
            number += 1
            slug = slugify('{}-{}'.format(validated_data['title'], str(number)))
        validated_data['slug'] = slug
        return super(PostSerializer, self).create(validated_data)