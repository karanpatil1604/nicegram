import os
import uuid
from PIL import Image
from rest_framework import serializers
from django.conf import settings


from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('post_id', 'picture', 'caption')
        # fix the issue for optional field of `picture` for update method
        extra_kwargs = {
            'picture': {'required': False, 'allow_null': True}
        }

    def create(self, validated_data):
        image = validated_data.pop('picture', None)

        new_post = super(PostSerializer, self).create(validated_data)

        if image:
            new_filename = self.save_image(image)
            new_post.picture = new_filename
            new_post.save()

        return new_post

    def save_image(self, image):
        unique_name = str(uuid.uuid4())

        _, file_extension = os.path.splitext(image.name)
        new_filename = f"{unique_name}{file_extension}"

        img = Image.open(image)
        img.thumbnail((400, 400))

        img.save(os.path.join(settings.MEDIA_ROOT, 'posts/pics/', new_filename))

        return new_filename
