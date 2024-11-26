from rest_framework.exceptions import ValidationError
from sympy import sympify, zoo


def evaluate_expression(elements, expression, mapped_kpi):
    """
    This function will evaluate expression using mapped_pki which contains
    kpi for each layer.
    :param elements:
    :param expression:
    :param mapped_kpi:
    :return:
    """
    result = {}
    for element in elements:
        variables = mapped_kpi[element]
        sympy_expr = sympify(expression)
        res = sympy_expr.evalf(subs={var: float(value) for var, value in variables.items()})
        if res == zoo:
            raise ValidationError("Division by zero!")
        result[element] = str(res)

    return result