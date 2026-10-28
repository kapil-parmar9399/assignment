from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse

from .models import Box, Order, OrderItem, Product
from .recommendations import recommend_box


class RecommendationTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(sku="P-1", name="Widget", length_cm=8, width_cm=5, height_cm=3, weight_kg="1.250")
        self.order = Order.objects.create()
        OrderItem.objects.create(order=self.order, product=self.product, quantity=1)

    def box(self, name="Box", length=10, width=8, height=5, max_weight="2", cost="2.00", is_available=True):
        return Box.objects.create(name=name, length_cm=length, width_cm=width, height_cm=height,
                                  max_weight_kg=max_weight, cost=cost, is_available=is_available)

    def test_recommends_box_that_fits_and_respects_rotation(self):
        box = self.box(length=3, width=8, height=5)
        self.assertEqual(recommend_box(self.order).box, box)

    def test_rejects_dimensions_that_do_not_fit_even_if_volume_is_larger(self):
        self.box(length=12, width=2, height=3)
        self.assertIsNone(recommend_box(self.order))

    def test_rejects_box_when_order_weight_exceeds_capacity(self):
        self.box(max_weight="1.249")
        self.assertIsNone(recommend_box(self.order))

    def test_uses_updated_database_weight_instead_of_cached_product_weight(self):
        cached_item = OrderItem.objects.select_related("product").get(order=self.order)
        self.assertEqual(cached_item.product.weight_kg, Decimal("1.250"))
        Product.objects.filter(pk=self.product.pk).update(weight_kg="6.000")
        too_light = self.box(name="Small Box", max_weight="5.000")

        self.assertIsNone(recommend_box([cached_item]))
        self.assertEqual(Product.objects.get(pk=self.product.pk).weight_kg, Decimal("6.000"))

    def test_recommends_box_with_capacity_for_updated_six_kg_product(self):
        Product.objects.filter(pk=self.product.pk).update(weight_kg="6.000")
        suitable = self.box(name="Six kg box", max_weight="6.000", cost="3.00")

        recommendation = recommend_box(self.order)

        self.assertEqual(recommendation.box, suitable)
        self.assertEqual(recommendation.total_weight_kg, Decimal("6.000"))

    def test_total_weight_includes_every_product_and_its_quantity(self):
        Product.objects.filter(pk=self.product.pk).update(weight_kg="3.000")
        second = Product.objects.create(sku="P-2", name="Second", length_cm=8, width_cm=5, height_cm=3, weight_kg="1.500")
        OrderItem.objects.filter(order=self.order, product=self.product).update(quantity=2)
        OrderItem.objects.create(order=self.order, product=second, quantity=1)
        self.box(max_weight="7.499")
        sufficient = self.box(name="Sufficient", length=24, width=5, height=3, max_weight="7.500", cost="3.00")

        recommendation = recommend_box(self.order)

        self.assertEqual(recommendation.box, sufficient)
        self.assertEqual(recommendation.total_weight_kg, Decimal("7.500"))

    def test_selects_lowest_cost_eligible_box(self):
        self.box(name="Large costly", length=20, width=20, height=20, cost="5.00")
        cheaper = self.box(name="Small economical", cost="1.25")
        self.assertEqual(recommend_box(self.order).box, cheaper)

    def test_returns_no_recommendation_when_no_box_is_available(self):
        self.box(is_available=False)
        self.assertIsNone(recommend_box(self.order))

    def test_packs_multiple_products_without_overlap(self):
        second = Product.objects.create(sku="P-2", name="Second", length_cm=8, width_cm=5, height_cm=3, weight_kg="0.5")
        OrderItem.objects.create(order=self.order, product=second)
        box = self.box(name="Two items", length=16, width=5, height=3)
        self.assertEqual(recommend_box(self.order).box, box)

    def test_order_with_no_items_has_no_recommendation(self):
        self.assertIsNone(recommend_box([]))


class ApplicationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(sku="P-1", name="Widget", length_cm=8, width_cm=5, height_cm=3, weight_kg="1")
        self.box = Box.objects.create(name="Small box", length_cm=10, width_cm=8, height_cm=5, max_weight_kg=2, cost=1)

    def test_home_page_loads(self):
        response = self.client.get(reverse("shipping:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Recommend a shipping box")

    def test_valid_request_creates_order_and_shows_recommendation(self):
        response = self.client.post(reverse("shipping:home"), {"products": [self.product.pk], "quantity": 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)
        self.assertContains(response, self.box.name)

    def test_updated_six_kg_product_is_not_assigned_to_five_kg_box(self):
        Product.objects.filter(pk=self.product.pk).update(weight_kg="6.000")
        self.box.max_weight_kg = Decimal("5.000")
        self.box.save(update_fields=["max_weight_kg"])

        response = self.client.post(reverse("shipping:home"), {"products": [self.product.pk], "quantity": 1})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No available box can safely fit this order")
        self.assertNotContains(response, "Recommended Small box")

    def test_updated_six_kg_product_can_use_box_with_six_kg_capacity(self):
        Product.objects.filter(pk=self.product.pk).update(weight_kg="6.000")
        self.box.max_weight_kg = Decimal("6.000")
        self.box.save(update_fields=["max_weight_kg"])

        response = self.client.post(reverse("shipping:home"), {"products": [self.product.pk], "quantity": 1})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Recommended Small box")

    def test_invalid_request_shows_validation_error(self):
        response = self.client.post(reverse("shipping:home"), {"products": [], "quantity": 0})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 0)
        self.assertContains(response, "Choose at least one product")
