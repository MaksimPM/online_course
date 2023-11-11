import stripe

from rest_framework import status
from rest_framework.response import Response

from config import settings
from courses.models import Payment

stripe.api_key = settings.STRIPE_API_KEY


def create_customer(user):
    customer = stripe.Customer.create(
        email=user.email,
    )
    return customer


def create_intent(request):
    intent = stripe.PaymentIntent.create(
        amount=request.data['payment_amount'],
        currency=request.data['currency'],
        customer=create_customer(request.user)
    )
    return Response(status=status.HTTP_200_OK, data={"intent": intent})


def get_intent(pk):
    try:
        payment_intent_id = Payment.objects.get(pk=pk).stripe_id
        payment_intent = stripe.PaymentIntent.retrieve(
            payment_intent_id
        )
        return Response(status=status.HTTP_200_OK, data=payment_intent)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})
