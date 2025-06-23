import stripe

from config.settings import STRIPE_SECRET_KEY, PAYMENT_SUCCESS_URL, PAYMENT_CANCEL_URL

stripe.api_key = STRIPE_SECRET_KEY


class StripeService:
    """Сервис для работы со Stripe"""

    @staticmethod
    def create_product(name):
        product = stripe.Product.create(name=name)
        return product.id

    @staticmethod
    def create_price(amount, product_id):
        price = stripe.Price.create(
            unit_amount=int(amount * 100),
            currency="rub",
            product=product_id,
        )
        return price.id

    @staticmethod
    def create_checkout_session(price_id: str) -> dict:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": price_id,
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=PAYMENT_SUCCESS_URL,
            cancel_url=PAYMENT_CANCEL_URL,
        )
        return {"session_id": session.id, "payment_link": session.url}
