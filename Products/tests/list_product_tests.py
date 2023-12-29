import pytest
from django.urls import reverse
from Products.models import Product
from Categories.models import Category
from Accounts.models import User

@pytest.fixture
def user(db):
    return User.objects.create(email='test@example.com')

@pytest.fixture
def category(db):
    return Category.objects.create(title='Test Category')

@pytest.fixture
def api_client(user):
    from rest_framework.test import APIClient
    client = APIClient()
    client.force_authenticate(user=user)
    return client

def test_list_product(api_client, user, category):
    product1 = Product.objects.create(title='Product 1', price=33.44, owner=user, category=category)
    product2 = Product.objects.create(title='Product 2', price=78.10, owner=user, category=category)
    data = {'user_id': user.id, 'ids': [product1.id, product2.id]}
    response = api_client.post(reverse('list-product'), data)
    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]['title'] == 'Product 1'
    assert response.data[0]['price'] == 33.44
    assert response.data[1]['title'] == 'Product 2'
    assert response.data[1]['price'] == 78.10
