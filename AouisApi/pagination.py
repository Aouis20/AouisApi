from rest_framework import pagination
from rest_framework.response import Response

from Products.models import Product


class ProductPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, products):
        # Condition counter
        conditions = {condition: 0 for condition in Product.ConditionStatus}

        # Payment type counter
        payment_types = {type: 0 for type in Product.PaymentTypeEnum}

        for product in products:
            condition = product["condition"]
            payment_type = product["payment_type"]
            conditions[condition] += 1
            payment_types[payment_type] += 1

        return Response(
            {
                "items": len(products),
                "total_items": self.page.paginator.count,
                "page": self.page.number,
                "total_pages": self.page.paginator.num_pages,
                "conditions": conditions,
                "payment_types": payment_types,
                "results": products,
            }
        )
