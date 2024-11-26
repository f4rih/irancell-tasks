import re

from rest_framework.exceptions import ValidationError
from rest_framework import serializers


ALLOWED_OPERATIONS = {"+", "-", "*", "/", ""}


class CalculateKpiSerializer(serializers.Serializer):
    layer = serializers.CharField(max_length=100)
    elements = serializers.ListField(child=serializers.CharField(max_length=100))
    kpi = serializers.CharField(max_length=255)

    def validate_kpi(self, value):
        """
        This function will help me to validate expression,
        Because expressions come from untrusted outsource it must be validated before evaluation.
        I've used sympy for safety evaluation, but it's a good practice to validate expressions in multi steps
        to ensure there is no security issue in the future.

        :param expression:
        :return:
        """
        # Allowed characters: KPI names, numbers, spaces, and math operators
        pattern = re.compile(r"^([\d\.\s\(\)\+\-\*/kpi_]+)$")
        if not pattern.match(value):
            raise ValidationError("Invalid expression. Only KPIs and math operators are allowed.")

        # Ensure only allowed operators are present, according to docs.
        tokens = re.split(r"[\s\(\)]+", value)
        for token in tokens:
            if token.startswith("kpi_"):
                continue
            if token not in ALLOWED_OPERATIONS and not token.replace('.', '', 1).isdigit():
                raise ValidationError(f"Invalid token in expression: {token}")
        return value