from django.contrib.auth.models import User
from blogApp.models import Post,AuthorProfile,CategoryList,TagName
from rest_framework import generics, status, exceptions
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from django.core.validators import RegexValidator
from django.db.models.fields import TextField


class UsernameField(serializers.CharField):
    default_error_messages = {
        "invalid": "Not a valid username.",
        "blank": "This Username may not be blank.",
        "max_length": "Ensure Username field has no more than {max_length} characters.",
        "min_length": "Ensure Username field has at least {min_length} characters.",
    }

class PasswordField(serializers.CharField):
    default_error_messages = {
        "invalid": "Not a valid username.",
        "blank": "Password Field may not be blank.",
        "max_length": "Ensure Password field has no more than {max_length} characters.",
        "min_length": "Ensure Password field has at least {min_length} characters.",
    }
    
class UsernameSerializer(serializers.Serializer):
    alphanumeric = RegexValidator(
        r"^[0-9a-zA-Z]*$", message=" Username must contain Alphabets and Numbers only"
    )
    username = serializers.CharField(
        max_length=16, min_length=3, allow_null=True, validators=[alphanumeric]
    )  # allows only alphanumeric values

    class Meta:
        model = User
        fields = "username"

    def validate(self, args):
        username = args.get("username", None)
        if username[:1].isnumeric():
            raise serializers.ValidationError(
                {"username": "first digit should not be a Number"}
            )  # check if the first digit in the username is number
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {"username": "username already exists"}
            )  # check if the username already exists
        return super().validate(args)

class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(validators = [UniqueValidator(queryset=User.objects.all(),message="Email Already Exist")])
    alphanumeric = RegexValidator(
        r"^[0-9a-zA-Z]*$", message="Username must contain Alphabets and Numbers only"
    )

    username = UsernameField( 
        max_length=16,
        min_length=3,
        allow_null=True,
        validators=[
            alphanumeric,
            UniqueValidator(
                queryset=User.objects.all(), message="Username already exists"
            ),
        ],
    )
    password = PasswordField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password",
        )

    def validate(self, args):
        email = args.get("email", None)
        username = args.get("username", None)

        if username[:1].isnumeric():
            raise serializers.ValidationError(
                {"username": "First digit should not be a Number"}
            )  # check if the first digit in the username is number
        return super().validate(args)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        pass

class ProfileSerializer(serializers.Serializer):
    user = RegistrationSerializer()

    class Meta:
        model = AuthorProfile
        fields = ("username",)

    def create(self, validated_data):
        return User.objects.create_author(**validated_data)

    def update(self, instance, validated_data):
        pass

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=16, min_length=3, allow_null=True)
    password = PasswordField(min_length=8, write_only=True)
    class Meta:
        model = User
        fields =("username","password")
        def validate(self,args):
            email = args.get("email", None)
            username = args.get("username", None)

            if not User.objects.filter(username=username).exists:
                raise serializers.ValidationError({"username":"Username Does not Exists"})
            return super().validate(args)

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ("email",)

    def validate(self, args):
        email = args.get("email", None)
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "email does not exists"})
        return super().validate(args)

class WritePostSerializer(serializers.Serializer):
    # title = serializers.CharField(max_length=80, min_length=60)
    # content=serializers.CharField(max_length=7500, min_length=6250)
    # author = serializers.CharField()
    # category = serializers.ChoiceField(choices=list(CategoryList.objects.all().values_list('category_name', flat=True)))

    class Meta:
        model = Post
        fields = ("title","content","author","category")

    def validate(self, args):
        title = args.get("title", None)
        if Post.objects.filter(title=title).exists():
            raise serializers.ValidationError({"title": "title already exists"})
        return super().validate(args)

class CategorySerializer(serializers.Serializer):
    category_name = serializers.CharField(max_length=20, min_length=3)

    class Meta:
        model = CategoryList
        fields = ("category_name")

    def validate(self, args):
        category_name = args.get("category_name", None)
        if CategoryList.objects.filter(category_name=category_name).exists():
            raise serializers.ValidationError({"category": "category already exists"})
        return super().validate(args)

    def create(self, validated_data):
        return CategoryList.objects.create(**validated_data)

class TagSerializer(serializers.Serializer):
    category_name = serializers.CharField(max_length=20, min_length=3)
    # content=serializers.CharField(max_length=7500, min_length=6250)
    # author = serializers.CharField()
    # category = serializers.ChoiceField(choices=list(CategoryList.objects.all().values_list('category_name', flat=True)))

    class Meta:
        model = TagName
        fields = ("tag_name","category_name")

    def validate(self, args):
        tag_name = args.get("tag_name", None)
        if TagName.objects.filter(tag_name=tag_name).exists():
            raise serializers.ValidationError({"tag": "tag already exists"})
        return super().validate(args)

    def create(self, validated_data):
        category_name = validated_data.get('category_name')
        valid_category_name = CategoryList.objects.filter(category_name=category_name).first()
        if valid_category_name:
            validated_data['category_name']=valid_category_name
            return TagName.objects.create(**validated_data)
        raise serializers.ValidationError({"category": "invalid category"})
