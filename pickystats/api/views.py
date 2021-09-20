from django.utils.decorators import method_decorator
from drf_yasg.openapi import Parameter
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

import logging

from ..analyzer import PickyStats
from .serializers import FileUploadSerializer

logger = logging.getLogger(__name__)

# quick fix to enable swagger
@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        request_body=FileUploadSerializer,
        manual_parameters=[
            Parameter(name='formatter', in_='json', default='json', type='string', enum=['json', 'csv'])
        ]
    )
)
class DataAnalyzerView(APIView):

    parser_classes = [MultiPartParser, ]
    def post(self, request, *args, **kwargs):

        logger.info('User uploaded a file to ba analyzed')

        formatter = request.query_params.get('formatter', 'json')
        serializer = FileUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        textinput = serializer.validated_data['textfile'].read().decode()

        results = PickyStats(textfile=textinput)
        result = results.get_all_stats(format=formatter)

        return Response(result)
