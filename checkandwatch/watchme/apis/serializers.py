from django.forms import ValidationError
from rest_framework import serializers

from watchme.models import  Review, Watch_List, StreamPlatform, Review

# <Using Serializers. serializer start>
# def name_length(value): #It is validator validation
#     if len(value) < 2:
#         raise serializers.ValidationError('Name is too short!')

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators = [name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return Movies.objects.create(**validated_data) #validated_data= New data


#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)  #Instance means the old value in database
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance #Instance because instance hold all the contains
        
   #<serializer.serializer END>

# Validation in serializer fields
#Object leve Validation which used to validate more than one fields
    # def validate(self, data):
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError('Name and description should be different')
    #     else:
    #         return data
        
#First we use field level validation which is used for only one field of an object. For exp-

    # def validate_name(self, value):
    #     if len(value) < 2:
    #         raise serializers.ValidationError('Name is too short!')
    #     else:
    #         return value


# <start Model.Serializer>
class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        exclude = ('watchlist',)
       # fields = '__all__'


class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True) #For creating relationship between Review and Watchlist 
    #len_name = serializers.SerializerMethodField()      #It used when we want to add extra field. It is not inside an model field or in views but we inside an serializer to show the extra field on a page.
    class Meta:
        model = Watch_List
        fields = '__all__'

    #def get_len_name(self, object):   #It is a custom method which is mostly used to need the calculation, time duration or give ratings to features.
     #   length = len(object.name)
      #  return length


class StreamPlatformSerializer(serializers.ModelSerializer):
    #watchlist = serializers.StringRelatedField(many=True) #SiringRelatedField is used when we want to show only 1 field istead of all fields.
    #watchlist = serializers.PrimaryKeyRelatedField(read_only=True, many=True) #PrimaryKeyRelatedField may be used to represent target the of relationship
   # watchlist = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='moviedetail') #Hyperlinked creates a link to access the fields.
    watchlist = WatchListSerializer(many=True, read_only=True)
    class Meta:
        model = StreamPlatform
        fields = '__all__'


# class StreamPlatFormSerializer(serializers.HyperlinkedModelSerializer):
#     watchlist = WatchListSerializer(many=True, read_only=True)
#     class Meta: HyperlinkedModelserializer is used when we want to access through the url of every fields
#         model = StreamPlatform
#         fields = '__all__'
