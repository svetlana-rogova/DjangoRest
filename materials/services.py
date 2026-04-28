import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_product(course):
    """
    Создаём продукт в Stripe на основе курса.
    """
    return stripe.Product.create(
        name=course.title
    )


def create_price(product_id, amount):
    """
    Создаём цену для продукта в Stripe.
    """
    return stripe.Price.create(
        unit_amount=amount * 100,
        currency="usd",
        product=product_id
    )


def create_session(price_id):
    """
     Создаём checkout-сессию Stripe для оплаты.
    """
    return stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price": price_id,
            "quantity": 1,
        }],
        mode="payment",
        success_url="http://127.0.0.1:8000/success/",
        cancel_url="http://127.0.0.1:8000/cancel/",
    )
