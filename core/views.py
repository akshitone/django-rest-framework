from django.http import request
from django.http.response import HttpResponseNotAllowed
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Customer, DataSheet, Document, Profession
from .serializers import CustomerSerializer, ProfessionSerializer, DataSheetSerializer, DocumentSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    # queryset = Customer.objects.filter(active=True)
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    # filterset_fields = ['name', 'address']
    search_fields = ['name', 'address', 'data_sheet__description']
    # search_fields = ['=name', '^address', 'data_sheet__description'] it search for exact name and starts with address
    ordering_fields = ['id', 'name', 'address']
    # ordering_fields = '__all__' now you can filter with any field
    ordering = ['id']  # for default
    lookup_field = 'id'  # you can look up for any field but it must be unique it's for url

    def get_queryset(self):
        # id = self.request.query_params.get('id', None)
        address = self.request.query_params.get('address', None)

        status = self.request.query_params.get('active', True)

        if address:
            # address__icontains IS USED TO CHECK SUB STRING IN STRING
            customers = Customer.objects.filter(
                address__icontains=address, active=status)
        else:
            customers = Customer.objects.filter(active=status)

        # customers = Customer.objects.filter(id=id)
        return customers

    # def list(self, request, *args, **kwargs):
    #     customers = self.get_queryset()
    #     serializer = CustomerSerializer(customers, many=True)
    #     return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = CustomerSerializer(obj)
        return Response(serializer.data)
        # return HttpResponseNotAllowed('Not allowed')

    def create(self, request, *args, **kwargs):
        data = request.data
        customer = Customer.objects.create(
            name=data['name'],
            address=data['address'],
            data_sheet_id=data['data_sheet'],
        )
        profession = Profession.objects.get(id=data['profession'])
        customer.professions.add(profession)
        customer.save()

        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        customer = self.get_object()
        data = request.data
        customer.name = data['name']
        customer.address = data['address']
        customer.data_sheet_id = data['data_sheet']

        profession = Profession.objects.get(id=data['profession'])

        for p in customer.professions.all():
            customer.professions.remove(p)

        customer.professions.add(profession)
        customer.save()

        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.name = request.data.get('name', customer.name)
        customer.address = request.data.get('address', customer.address)
        customer.data_sheet_id = request.data.get(
            'data_sheet', customer.data_sheet_id)
        customer.save()

        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    @action(detail=True)
    def deactivate(self, request, **kwargs):
        customer = self.get_object()
        customer.active = False
        customer.save()

        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    @action(detail=False)
    def deactivate_all(self, request, **kwargs):
        customers = self.get_queryset()
        customers.update(active=False)

        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def activate_all(self, request, **kwargs):
        customers = self.get_queryset()
        customers.update(active=True)

        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)


class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer


class DataSheetViewSet(viewsets.ModelViewSet):
    queryset = DataSheet.objects.all()
    serializer_class = DataSheetSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
