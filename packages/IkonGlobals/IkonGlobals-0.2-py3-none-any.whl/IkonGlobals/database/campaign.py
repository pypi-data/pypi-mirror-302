from datetime import datetime

from pynamodb.attributes import UnicodeAttribute, MapAttribute, UTCDateTimeAttribute, ListAttribute, NumberAttribute
from pynamodb.models import Model
from pytz import timezone

from utils.utils import random_id


class Submission(MapAttribute):
    id = UnicodeAttribute()
    user_id = UnicodeAttribute(null=False)
    speaker_id = NumberAttribute(null=False)
    submitted_at = UTCDateTimeAttribute(default=lambda: datetime.utcnow())

    def to_dict(self):
        value = self.submitted_at.astimezone(timezone('Asia/Bangkok')).isoformat()

        return {
            "id": self.id,
            "user_id": self.user_id,
            "speaker_id": self.speaker_id,
            "submitted_at": value
        }


def get_submission(campaign_id, submission_id):
    campaign = Campaign.get(campaign_id)
    for submission in campaign.submissions:
        if submission.id == submission_id:  # Assuming `id` attribute in Submission class
            return submission

    raise Exception(f"Submission {submission_id} not found")


class Campaign(Model):
    class Meta:
        table_name = 'Campaigns'
        region = 'ap-southeast-1'
        billing_mode = 'PAY_PER_REQUEST'

    TAG_AWARDED = "TAG_AWARDED"
    LABEL_AWARDED = "LABEL_AWARDED"
    SPARKLES_AWARDED = "SPARKLES_AWARDED"

    id = UnicodeAttribute(hash_key=True, default=random_id())
    name = UnicodeAttribute(null=True)
    owner = UnicodeAttribute(null=True)
    prize = UnicodeAttribute(null=True)
    script = UnicodeAttribute(null=True)
    description = UnicodeAttribute(null=True)
    tags = ListAttribute(default=None, null=True)
    submissions = ListAttribute(of=Submission, default=None, null=True)
    updated_at = UTCDateTimeAttribute(default=lambda: datetime.utcnow())
    creation_at = UTCDateTimeAttribute(default=lambda: datetime.utcnow())
    price_type = UnicodeAttribute(default=TAG_AWARDED, null=False)

    def to_dict(self):
        rval = {}
        for key, _ in self.get_attributes().items():
            value = getattr(self, key)
            if isinstance(value, datetime):
                value = value.astimezone(timezone('Asia/Bangkok')).isoformat()
            elif key == "submissions":
                value = [submission.to_dict() for submission in value]

            rval[key] = value

        return rval


# Create the table if it does not exist
if not Campaign.exists():
    Campaign.create_table(wait=True)
