from datetime import datetime
from enum import Enum

from pynamodb.attributes import UnicodeAttribute, NumberAttribute, BooleanAttribute, UTCDateTimeAttribute, ListAttribute
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.models import Model
from pynamodb_attributes import UnicodeEnumAttribute

from utils.utils import random_id


class UserStatus(Enum):
    PENDING_INVITATION = "pending_invitation"
    ACTIVE = "active"
    INACTIVE = "inactive"
    DELETED = "deleted"


# Define your User model
def generate_referral_code():
    return "Ikon-" + random_id(is_str=True, lenght=6)


class User(Model):
    class Meta:
        table_name = 'Users'
        region = 'ap-southeast-1'
        billing_mode = 'PAY_PER_REQUEST'

    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute(null=True)
    email = UnicodeAttribute(null=True)
    email_verified = BooleanAttribute(default=False)
    nickname = UnicodeAttribute(null=True)
    picture = UnicodeAttribute(null=True)
    updated_at = UTCDateTimeAttribute(null=True)
    fetched_at = UTCDateTimeAttribute(null=True)

    energy_amount = NumberAttribute(default=0)
    sparkle_amount = NumberAttribute(default=50)
    drink_amount = NumberAttribute(default=0)
    start_amount = NumberAttribute(default=0)
    subscription_transaction_id = UnicodeAttribute(null=True)
    subscription_package = UnicodeAttribute(null=True)
    status = UnicodeEnumAttribute(UserStatus)
    invitation_code = UnicodeAttribute(null=True)
    referred_by = UnicodeAttribute(null=True)
    referral_code = UnicodeAttribute(default=lambda: generate_referral_code())
    referred_users = ListAttribute(null=True, default=lambda: [])
    is_internal = BooleanAttribute(default=False)

    # has_premium_membership = BooleanAttribute(null=True, default=False)

    recent_speakers = ListAttribute(of=NumberAttribute, default=list)

    def to_dict(self):
        rval = {}
        for key, _ in self.get_attributes().items():
            value = getattr(self, key)
            if isinstance(value, datetime):
                from pytz import timezone
                value = value.astimezone(timezone('Asia/Bangkok')).isoformat()

            rval[key] = value

        rval.pop("referred_users", None)
        rval["referred_users_count"] = len(self.referred_users) if self.referred_users else 0
        # rval["status"] = self.status.value if self.status and not isinstance(self.status, str) else None
        if not isinstance(rval.get("status", ""), str):
            rval["status"] = self.status.value if self.status else None

        return rval


# Define the Global Secondary Index for the 'code' attribute
class CodeIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = 'CodeIndex'
        projection = AllProjection()
        billing_mode = 'PAY_PER_REQUEST'

    code = UnicodeAttribute(hash_key=True)


class RedemptionCodeType(Enum):
    INVITATION = "invitation"
    TOP_UP = "top_up"


class RedemptionCode(Model):
    class Meta:
        table_name = 'RedemptionCode'
        region = 'ap-southeast-1'
        billing_mode = 'PAY_PER_REQUEST'

    id = UnicodeAttribute(hash_key=True, default=lambda: random_id(is_uuid=True))
    code = UnicodeAttribute(default=lambda: random_id(is_str=True))
    code_index = CodeIndex()
    credit_amount = NumberAttribute()
    expiration_date = UTCDateTimeAttribute(null=True)
    is_available = BooleanAttribute(default=True)
    redeemed_by_user_ids = ListAttribute(null=True, default=lambda: [])
    redeemed_at = UTCDateTimeAttribute(null=True)
    created_at = UTCDateTimeAttribute(default=lambda: datetime.utcnow())
    created_by_user_id = UnicodeAttribute(null=True)
    usage_limit = NumberAttribute(null=True)
    code_type = UnicodeEnumAttribute(RedemptionCodeType)
    premium_access = BooleanAttribute(default=False)  # For premium access

    @property
    def is_over_limit(self):
        return self.usage_limit and len(self.redeemed_by_user_ids) >= self.usage_limit

    def is_valid(self, user_id):
        if user_id in self.redeemed_by_user_ids:
            return False, "This code has already been redeemed by you"
        if not self.is_available:
            return False, "This code is no longer available"
        if self.expiration_date and self.expiration_date.replace(tzinfo=None) < datetime.utcnow():
            return False, "This code has expired"
        if self.is_over_limit:
            return False, "This code has reached its usage limit"

        return True, None

    def to_dict(self):
        rval = {}
        for key, _ in self.get_attributes().items():
            value = getattr(self, key)
            if isinstance(value, datetime):
                from pytz import timezone
                value = value.astimezone(timezone('Asia/Bangkok')).isoformat()

            rval[key] = value

        return rval


if not RedemptionCode.exists():
    RedemptionCode.create_table(wait=True)

# Create the table if it does not exist
if not User.exists():
    User.create_table(wait=True)
