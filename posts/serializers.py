import os
import uuid
from PIL import Image
from rest_framework import serializers
from django.conf import settings
from rest_framework.fields import empty
from accounts.serializers import UserFeedSerializer


from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('post_id', 'picture', 'caption')

    def create(self, validated_data):
        image = validated_data.pop('picture', None)

        new_post = super(PostSerializer, self).create(validated_data)

        if image:
            new_filename = self.save_image(image)
            new_post.picture = new_filename
            new_post.save()

        return new_post

    def update(self, instance, validated_data):
        self.fields['picture'].required = False
        old_pic = str(instance.picture) if instance.picture else None
        new_pic = validated_data.pop('picture', None)
        instance = super(PostSerializer, self).update(instance, validated_data)
        if new_pic:
            new_filename = self.save_image(new_pic)
            instance.picture = new_filename
            instance.save()

        if new_pic and old_pic:
            old_pic = os.path.join(settings.MEDIA_ROOT,
                                   'posts/pics', old_pic)
            if os.path.isfile(old_pic):
                os.remove(old_pic)

        return instance

    def save_image(self, image):
        unique_name = str(uuid.uuid4())

        _, file_extension = os.path.splitext(image.name)
        new_filename = f"{unique_name}{file_extension}"

        img = Image.open(image)
        img.thumbnail((400, 400))

        img.save(os.path.join(settings.MEDIA_ROOT, 'posts/pics/', new_filename))

        return new_filename


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('post_id', 'picture', 'caption')

    def __init__(self, *args, **kwargs):
        super(PostUpdateSerializer, self).__init__(*args, **kwargs)

        self.fields['picture'].required = False

    def update(self, instance, validated_data):
        old_pic = str(instance.picture) if instance.picture else None
        new_pic = validated_data.pop('picture', None)
        instance = super(PostUpdateSerializer, self).update(
            instance, validated_data)
        if new_pic:
            new_filename = self.save_image(new_pic)
            instance.picture = new_filename
            instance.save()

        if new_pic and old_pic:
            old_pic = os.path.join(settings.MEDIA_ROOT,
                                   'posts/pics', old_pic)
            if os.path.isfile(old_pic):
                os.remove(old_pic)

        return instance

    def save_image(self, image):
        unique_name = str(uuid.uuid4())

        _, file_extension = os.path.splitext(image.name)
        new_filename = f"{unique_name}{file_extension}"

        img = Image.open(image)
        img.thumbnail((400, 400))

        img.save(os.path.join(settings.MEDIA_ROOT, 'posts/pics/', new_filename))

        return new_filename


class PostWithAuthorSerializer(serializers.ModelSerializer):
    author = UserFeedSerializer()

    class Meta:
        model = Post
        fields = ('post_id', 'caption', 'author', 'picture', 'created')
