from rest_framework import serializers
from django.contrib.auth.models import User
from tag.models import Tag 
from .models import Recipe
from authors.validators import AuthorRecipeValidator




class TagSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Tag
        fields = ['id', 'name', 'slug'] #outra forma de adicionar os campos
    # id = serializers.IntegerField()
    # name = serializers.CharField(max_length=65)
    # slug = serializers.SlugField(max_length=65)


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'author',
                  'category', 'tags', 'public', 'preparation',
                  'tags_name', 'tag_links', 'preparation_time', 
                  'preparation_time_unit', 'servings','servings_unit',
                  'preparation_steps', 'cover']

   
    public = serializers.BooleanField(source='is_published', read_only=True)#para caso queira trocar o nome do campo que está em models
    preparation = serializers.SerializerMethodField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    tags_name = TagSerializer(many=True, source='tags', read_only=True)

    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        read_only=True,
        view_name='recipes:recipes_api_v2_tag'
    )

    def get_preparation(self,recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'
    
    def validate(self, attrs):
        if self.instance is not None and attrs.get('servings') is None:
            attrs['servings'] = self.instance.servings

        if self.instance is not None and attrs.get('preparation_time') is None:
            attrs['preparation_time'] = self.instance.preparation_time

        super_validate = super().validate(attrs)
        AuthorRecipeValidator(
            data=attrs,
            ErrorClass=serializers.ValidationError,
        )

        return super_validate
    
    def save(self, **kwargs):
        return super().save(**kwargs)

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
