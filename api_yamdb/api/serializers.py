from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username"]


class UserRetrieveUpdateSerializer(UserBasicSerializer):
    role = serializers.ReadOnlyField()


class CustomTokenObtainPairSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)

    def validate(self, attrs):
        confirmation_code = attrs.get("confirmation_code")
        username = attrs.get("username")
        user = get_object_or_404(User, username=username)
        if user.confirmation_code != confirmation_code:
            raise ValidationError
        attrs["user"] = user
        return attrs


class GenreCategorySerializer(serializers.ModelSerializer):
    lookup_field = "slug"

    class Meta:
        fields = (
            "name",
            "slug",
        )


class CategorySerializer(GenreCategorySerializer):
    class Meta(GenreCategorySerializer.Meta):
        model = Category


class GenreSerializer(GenreCategorySerializer):
    class Meta(GenreCategorySerializer.Meta):
        model = Genre


class TitleSerializerGet(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source="reviews__score__avg", read_only=True
    )
    category = CategorySerializer()
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        fields = [
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        ]
        model = Title


class TitleSerializer(TitleSerializerGet):
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True, slug_field="slug", queryset=Genre.objects.all()
    )
    rating = serializers.IntegerField(read_only=True)

    def to_representation(self, value):
        return TitleSerializerGet(value, context=self.context).data


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = [
            "id",
            "text",
            "author",
            "score",
            "pub_date",
        ]
        model = Review

    def validate(self, data):
        if self.context["request"].method == "PATCH":
            return data
        title = self.context["view"].kwargs["title_id"]
        author = self.context["request"].user
        if Review.objects.filter(author=author, title__id=title).exists():
            raise serializers.ValidationError(
                "Нельзя оставлять более одного ревью!"
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )

    class Meta:
        fields = [
            "id",
            "text",
            "author",
            "pub_date",
        ]
        model = Comment
