import pytest
from rest_framework.test import APIRequestFactory
from Products.models import Product
from Products.views import ProductViewSet

product_payload = {
    "category": 1,
    "title": "Test Product",
    "description": "This is a test product",
    "price": 100.0,
    "visibility": True,
    "is_service": False,
    "payment": "UNIQ",
    "status": "FOR_SALE",
    "condition": "GOOD",
    "images": [],
}

@pytest.mark.django_db
def test_create_product():
    factory = APIRequestFactory()
    request = factory.post(
        "/products/",
        product_payload,
        format="json",
    )

    view = ProductViewSet.as_view({"post": "create"})
    response = view(request)

    assert response.status_code == 200

    product = Product.objects.first()
    assert product.title == "Test Product"
    assert product.description == "This is a test product"
    assert product.price == 100.0
    assert product.visibility == True
    assert product.is_service == False
    assert product.payment_type == Product.PaymentTypeEnum.UNIQ
    assert product.status == Product.ProductStatusEnum.FOR_SALE
    assert product.condition == Product.ConditionStatus.GOOD
    assert product.category.title == "Others"
