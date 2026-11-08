from typing import Optional, Literal
from datetime import datetime


class CustomerAccount:
    """Read model for customer profile - non-sensitive details."""
    
    def __init__(
        self,
        customer_id: int,
        name: str,
        email: str,
        preferences: Optional[dict] = None
    ):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.preferences = preferences or {}


class OrderHistoryItem:
    """Single order from order history response."""
    
    def __init__(
        self,
        order_id: int,
        order_date: datetime,
        status: str,
        total_amount: float,
        items_count: int
    ):
        self.order_id = order_id
        self.order_date = order_date
        self.status = status
        self.total_amount = total_amount
        self.items_count = items_count


class DeliveryStatus:
    """Real-time package tracking information."""
    
    def __init__(
        self,
        tracking_number: str,
        carrier: str,
        current_status: Literal["In Transit", "Out for Delivery", "Delivered", "Exception"],
        estimated_delivery: Optional[datetime] = None,
        last_update: Optional[datetime] = None
    ):
        self.tracking_number = tracking_number
        self.carrier = carrier
        self.current_status = current_status
        self.estimated_delivery = estimated_delivery
        self.last_update = last_update


class BillingTransaction:
    """PCI-DSS compliant masked billing transaction."""
    
    def __init__(
        self,
        transaction_id: str,
        amount: float,
        transaction_type: Literal["Charge", "Refund", "Credit"],
        payment_method_masked: str,  # e.g., "Visa ending in 4242"
        timestamp: datetime,
        status: Literal["Pending", "Completed", "Failed"] = "Completed"
    ):
        self.transaction_id = transaction_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.payment_method_masked = payment_method_masked
        self.timestamp = timestamp
        self.status = status


class RefundEligibilityResult:
    """Deterministic refund eligibility evaluation."""
    
    def __init__(
        self,
        eligible: bool,
        reason: Optional[str] = None,
        return_window_days: Optional[int] = None,
        conditions: Optional[list] = None
    ):
        self.eligible = eligible
        self.reason = reason
        self.return_window_days = return_window_days
        self.conditions = conditions or []


class ReturnRequest:
    """Initiated return with idempotency key."""
    
    def __init__(
        self,
        request_id: str,
        order_item_id: int,
        quantity: int,
        reason: str,
        status: Literal["Pending", "Approved", "Rejected", "Completed"] = "Pending",
        idempotency_key: Optional[str] = None,
        created_at: Optional[datetime] = None
    ):
        self.request_id = request_id
        self.order_item_id = order_item_id
        self.quantity = quantity
        self.reason = reason
        self.status = status
        self.idempotency_key = idempotency_key or request_id
        self.created_at = created_at or datetime.utcnow()


class RefundOperation:
    """Financial operation - requires elevated permissions and audit logging."""
    
    def __init__(
        self,
        operation_id: str,
        amount: float,
        transaction_type: Literal["Charge", "Refund", "Credit"],
        customer_id: int,
        payment_method_masked: str,
        status: Literal["Pending", "Processed", "Failed"] = "Pending",
        audit_trace: Optional[list] = None,
        processed_at: Optional[datetime] = None
    ):
        self.operation_id = operation_id
        self.amount = amount
        self.transaction_type = transaction_type
        self.customer_id = customer_id
        self.payment_method_masked = payment_method_masked
        self.status = status
        self.audit_trace = audit_trace or []
        self.processed_at = processed_at