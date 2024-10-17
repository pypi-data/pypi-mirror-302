from datetime import datetime

from pynamodb.attributes import (UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute, BooleanAttribute)
from pynamodb.models import Model
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from utils.utils import random_id


class SpeakerIdIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = 'speaker_id_index'
        billing_mode = 'PAY_PER_REQUEST'
        projection = AllProjection()

    speaker_id = NumberAttribute(hash_key=True)


class OwnerIdIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = 'owner_id_index'
        billing_mode = 'PAY_PER_REQUEST'
        projection = AllProjection()

    owner_id = UnicodeAttribute(hash_key=True)


class Speech(Model):
    class Meta:
        table_name = "SpeechTable"
        region = "ap-southeast-1"
        billing_mode = 'PAY_PER_REQUEST'

    id = UnicodeAttribute(hash_key=True, default=lambda: random_id(is_uuid=True))
    owner_id = UnicodeAttribute()
    speaker_id = NumberAttribute()
    text = UnicodeAttribute()
    price = NumberAttribute(default=50)
    bought = BooleanAttribute(default=False)
    created_at = UTCDateTimeAttribute(default=lambda: datetime.utcnow())
    # updated_at = UTCDateTimeAttribute(default=datetime.utcnow())

    speaker_id_index = SpeakerIdIndex()
    owner_id_index = OwnerIdIndex()

    def to_dict(self):
        rval = {}
        for key, _ in self.get_attributes().items():
            value = getattr(self, key)
            if isinstance(value, datetime):
                from pytz import timezone
                value = value.astimezone(timezone('Asia/Bangkok')).isoformat()

            rval[key] = value

        return rval


# class DubbingSpeakerIdIndex(GlobalSecondaryIndex):
#     class Meta:
#         index_name = 'dubbing_speaker_id_index'
#         billing_mode = 'PAY_PER_REQUEST'
#         projection = AllProjection()
#
#     speaker_id = NumberAttribute(hash_key=True)
#
#
# class DubbingOwnerIdIndex(GlobalSecondaryIndex):
#     class Meta:
#         index_name = 'dubbing_owner_id_index'
#         billing_mode = 'PAY_PER_REQUEST'
#         projection = AllProjection()
#
#     owner_id = UnicodeAttribute(hash_key=True)
#
#
# class Dubbing(Model):
#     class Meta:
#         table_name = "DubbingTable"
#         region = "ap-southeast-1"
#         billing_mode = 'PAY_PER_REQUEST'
#
#     id = UnicodeAttribute(hash_key=True, default=lambda: random_id(is_uuid=True))
#     owner_id = UnicodeAttribute()
#     speaker_id = NumberAttribute()
#     transcription_dict =
#     price = NumberAttribute(default=50)
#     bought = BooleanAttribute(default=False)
#     created_at = UTCDateTimeAttribute(default=lambda: datetime.utcnow())
#     # updated_at = UTCDateTimeAttribute(default=datetime.utcnow())
#
#     speaker_id_index = SpeakerIdIndex()
#     owner_id_index = OwnerIdIndex()
#
#     def to_dict(self):
#         rval = {}
#         for key, _ in self.get_attributes().items():
#             value = getattr(self, key)
#             if isinstance(value, datetime):
#                 from pytz import timezone
#                 value = value.astimezone(timezone('Asia/Bangkok')).isoformat()
#
#             rval[key] = value
#
#         return rval
# Create the table if it does not exist
# if not Speech.exists():
#     Speech.create_table(wait=True)
