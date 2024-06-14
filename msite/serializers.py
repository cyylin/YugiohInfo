from msite.models import Dailybind, Cardtyperef, Registercard
from rest_framework import serializers

class DailybindSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dailybind
        fields = '__all__'

class CardtyperefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cardtyperef
        fields = '__all__'

class RegistercardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registercard
        fields = '__all__'