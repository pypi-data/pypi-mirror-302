from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic import HttpUrl, conlist


from mercuryclient.types.common import NormalizedString


class NotesField(BaseModel):
    """
    Notes Field Details
    """

    purpose: Optional[NormalizedString] = Field(max_length=250)


class ItemField(BaseModel):
    """
    Item Field Details
    """

    name: NormalizedString = Field(max_length=80)
    amount: float = Field()
    currency: NormalizedString = Field(max_length=8)
    description: NormalizedString = Field(max_length=250)


class QRCodeDetails(BaseModel):
    """
    QR Code details
    """

    type: NormalizedString = Field(max_length=20)
    name: NormalizedString = Field(max_length=80)
    usage: NormalizedString = Field(max_length=25)
    fixed_amount: bool = Field()
    payment_amount: float = Field()
    description: NormalizedString = Field(max_length=250)
    notes: Optional[NotesField]


class CreatePlan(BaseModel):
    """
    Payment Plan Details
    """

    period: NormalizedString = Field(max_length=20)
    interval: int = Field()
    item: ItemField


class SubscriptionCreation(BaseModel):

    """
    Subscription Creation Details
    """

    plan_id: NormalizedString = Field(max_length=100)
    total_count: int = Field()
    quantity: int = Field()
    customer_notify: Optional[int] = Field()


class SubscriptionFetch(BaseModel):

    """
    Serializer for subscription fetch
    """

    subscription_id: NormalizedString = Field(max_length=100)


class Notify(BaseModel):

    """
    Notify Details
    """

    sms: bool = Field()
    email: bool = Field()


class CustomerDetails(BaseModel):

    """
    Customer Details
    """

    name: NormalizedString = Field(max_length=100)
    email: NormalizedString = Field(max_length=100)
    contact: NormalizedString = Field(max_length=15)


class PaymentGateway(BaseModel):
    """
    Payment Gateway Link Details
    """

    amount: float = Field()
    currency: NormalizedString = Field(max_length=10)
    accept_partial: bool = Field()
    description: NormalizedString = Field(max_length=250)
    notes: Optional[NotesField]
    customer: CustomerDetails
    notify: Optional[Notify]
    reminder_enable: bool = Field()
