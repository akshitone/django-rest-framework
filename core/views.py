from django.http.response import HttpResponseNotAllowed
from rest_framework.response import Response
from core.serializers import CustomerSerializer
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Customer, DataSheet, Document, Profession
from .serializers import CustomerSerializer, ProfessionSerializer, DataSheetSerializer, DocumentSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    # queryset = Customer.objects.filter(active=True)
    serializer_class = CustomerSerializer

    def get_queryset(self):
        active_customers = Customer.objects.filter(active=True)
        return active_customers

    def list(self, request, *args, **kwargs):
        customers = Customer.objects.filter(id=3)
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        # obj = self.get_object()
        # serializer = CustomerSerializer(obj)
        # return Response(serializer.data)
        return HttpResponseNotAllowed('Not allowed')


class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer


class DataSheetViewSet(viewsets.ModelViewSet):
    queryset = DataSheet.objects.all()
    serializer_class = DataSheetSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
