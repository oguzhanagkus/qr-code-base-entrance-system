from rest_framework import serializers
from entrance_system.models import Personnel, Location, PersonnelActivity, HESActivity


class PersonnelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personnel
        fields = ["first_name", "last_name"]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "name"]


class PersonnelActivitySerializer(serializers.ModelSerializer):
    personnel = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = PersonnelActivity
        fields = ["personnel", "result"]


class HESActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = HESActivity
        fields = ["first_name", "last_name", "result"]
