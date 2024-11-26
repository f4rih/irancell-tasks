import re
from decimal import Decimal

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from kpi.api.v1.serializers import CalculateKpiSerializer
from kpi.models import kpi_dynamic_model
from kpi.utils import evaluate_expression


class KPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CalculateKpiSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        expression = validated_data.get('kpi')
        elements = validated_data.get('elements')
        layer = validated_data.get('layer')
        kpi_list = re.findall(r"(kpi_\d+)", expression)
        _map = {layer: {} for layer in elements}
        for kpi in kpi_list:
            table_name = f'{kpi}_aggregations'
            model = kpi_dynamic_model(table_name=table_name)
            queryset = model.objects.filter(field_type=layer, field_name__in=elements).values('field_name', 'value')
            if queryset:
                for q in queryset:
                    _map[q['field_name']][kpi] = q['value']
            else:
                for e in elements:
                    _map[e][kpi] = Decimal(0)

        result = evaluate_expression(elements, expression, _map)
        return Response({'result': result}, status=status.HTTP_200_OK)

