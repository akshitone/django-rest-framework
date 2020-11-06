from rest_framework import serializers
from .models import Customer, DataSheet, Document, Profession


class DataSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSheet
        fields = ['id', 'description', 'historical_data']


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ['id', 'description']


class CustomerSerializer(serializers.ModelSerializer):
    number_of_professions = serializers.SerializerMethodField()
    data_sheet = DataSheetSerializer(read_only=True)  # Nested Serializer
    # data_sheet = serializers.PrimaryKeyRelatedField(read_only=True)
    # data_sheet = serializers.SerializerMethodField()
    # data_sheet = serializers.StringRelatedField()
    professions = ProfessionSerializer(many=True)
    # professions = serializers.StringRelatedField(many=True)

    class Meta:
        model = Customer
        fields = ['id', 'name', 'address',
                  'professions', 'data_sheet', 'active', 'get_status_message', 'number_of_professions']

    def get_number_of_professions(self, obj):
        return obj.number_of_professions()

    def get_data_sheet(self, obj):
        return obj.data_sheet.description
        # return obj.data_sheet.historical_data


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'dtype', 'doc_number', 'customer']
