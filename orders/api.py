from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import Province ,City
from .serializers import ProvinceSerializer, CitySerializer


class ListProvinceAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        provinces = Province.objects.all()
        provinces_serialized = ProvinceSerializer(provinces, many=True)
        return Response(provinces_serialized.data)


class ListCityAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        cities = City.objects.all()
        cities_serialized = CitySerializer(cities, many=True)
        return Response(cities_serialized.data)

