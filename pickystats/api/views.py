from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from ..analyzer import PickyStats
from .serializers import FileUploadSerializer
from rest_framework.response import Response


class DataAnalyzerView(APIView):

    parser_classes = [MultiPartParser, ]

    def post(self, request):

        formatter = request.query_params.get('formatter', 'json')
        print('format is ', formatter)
        serializer = FileUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        textinput = serializer.validated_data['textfile'].read().decode()

        results = PickyStats(textfile=textinput)
        result = results.get_all_stats(format=formatter)

        return Response(result)
