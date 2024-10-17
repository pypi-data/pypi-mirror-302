from datetime import datetime, timedelta
from pynamodb.attributes import (UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute, BooleanAttribute,
                                 ListAttribute, MapAttribute)
from pynamodb.indexes import GlobalSecondaryIndex, AllProjection
from pynamodb.models import Model

from utils.utils import random_id
from utils.embedding_utils import delete_item_from_index, create_update_item, \
    get_embedding_from_bedrock_cohere, speaker_to_text
from utils.utils import sigmoid

from IkonGlobals.settings import MINIMUM_SCORE, SPEAKER_INDEX


class SentenceLanguageIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = 'SentenceLanguageIndex'
        projection = AllProjection()
        billing_mode = 'PAY_PER_REQUEST'

    language_code = UnicodeAttribute(hash_key=True)


class LanguagePriorityIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index
    """

    class Meta:
        index_name = 'language-priority-index'
        billing_mode = 'PAY_PER_REQUEST'
        projection = AllProjection()

    language_code = UnicodeAttribute(hash_key=True)
    priority = NumberAttribute(range_key=True)


class TrainingSentence(Model):
    class Meta:
        table_name = "TrainingSentenceTable"
        region = "ap-southeast-1"
        billing_mode = 'PAY_PER_REQUEST'

    language_priority_index = LanguagePriorityIndex()

    id = NumberAttribute(hash_key=True, default=lambda: random_id(is_str=False))
    priority = NumberAttribute()
    text = UnicodeAttribute()
    language_code = UnicodeAttribute(default="en")
    created_at = UTCDateTimeAttribute(default=lambda: datetime.utcnow())

    def to_dict(self):
        rval = {}
        for key, _ in self.get_attributes().items():
            value = getattr(self, key)
            if isinstance(value, datetime):
                from pytz import timezone
                value = value.astimezone(timezone('Asia/Bangkok')).isoformat()

            rval[key] = value

        return rval


class SpeakerOwnerIndex(GlobalSecondaryIndex):
    class Meta:
        index_name = 'SpeakerOwnerIndex'
        projection = AllProjection()
        billing_mode = 'PAY_PER_REQUEST'

    owner_id = UnicodeAttribute(hash_key=True)


class SpeakerRenting(Model):
    class Meta:
        table_name = "SpeakerRenting"
        region = "ap-southeast-1"
        billing_mode = 'PAY_PER_REQUEST'

    renter_id = UnicodeAttribute(hash_key=True)
    speaker_id = NumberAttribute(range_key=True)
    rent_price = NumberAttribute(null=True)
    default_expiry = UTCDateTimeAttribute(default=lambda: datetime.utcnow() + timedelta(hours=48))

    def to_dict(self):
        rval = {}
        for key, _ in self.get_attributes().items():
            value = getattr(self, key)
            if isinstance(value, datetime):
                from pytz import timezone
                value = value.astimezone(timezone('Asia/Bangkok')).isoformat()

            rval[key] = value

        return rval


class SpeakerFavorite(Model):
    class Meta:
        table_name = "SpeakerFavorite"
        region = "ap-southeast-1"
        billing_mode = 'PAY_PER_REQUEST'

    user_id = UnicodeAttribute(hash_key=True)
    speaker_id = NumberAttribute(range_key=True)

    def to_dict(self):
        rval = {}
        for key, _ in self.get_attributes().items():
            value = getattr(self, key)
            if isinstance(value, datetime):
                from pytz import timezone
                value = value.astimezone(timezone('Asia/Bangkok')).isoformat()

            rval[key] = value

        return rval


from enum import Enum


class AgeStyle(Enum):
    YOUNG = "young"
    MIDDLE = "middle"
    OLD = "old"


class SpeakerRating(Model):
    class Meta:
        table_name = "SpeakerRating"
        region = "ap-southeast-1"
        billing_mode = 'PAY_PER_REQUEST'

    speaker_id = NumberAttribute(hash_key=True)
    user_id = UnicodeAttribute(range_key=True)
    rating = NumberAttribute(default=5)
    created_at = UTCDateTimeAttribute(default=lambda: datetime.utcnow())
    updated_at = UTCDateTimeAttribute(default=lambda: datetime.utcnow())

    def to_dict(self):
        rval = {}
        for key, _ in self.get_attributes().items():
            value = getattr(self, key)
            if isinstance(value, datetime):
                from pytz import timezone
                value = value.astimezone(timezone('Asia/Bangkok')).isoformat()

            rval[key] = value

        return rval

    # everytime it saves it updates update_at
    def save(self, conditional_operator=None, **expected_values):
        self.updated_at = datetime.utcnow()
        return super().save(conditional_operator, **expected_values)


class SocialMediaAccounts(MapAttribute):
    facebook = UnicodeAttribute(null=True)
    twitter = UnicodeAttribute(null=True)
    instagram = UnicodeAttribute(null=True)
    tiktok = UnicodeAttribute(null=True)

class SpeakerPopularityIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index for sorting by popularity amount
    """
    class Meta:
        index_name = 'speaker_popularity_index'
        projection = AllProjection()

    is_market = NumberAttribute(hash_key=True)
    popularity_amount = NumberAttribute(range_key=True)

class MarketScoreIndex(GlobalSecondaryIndex):
    """
    This class represents a global secondary index for sorting by market_sort_score
    """
    class Meta:
        index_name = 'market_score_index'
        projection = AllProjection()

    is_market = NumberAttribute(hash_key=True)
    market_sort_score = NumberAttribute(range_key=True)

class Speaker(Model):
    """
    A speaker model class for pynamodb
    """

    class Meta:
        table_name = "SpeakerTable"
        region = "ap-southeast-1"
        billing_mode = 'PAY_PER_REQUEST'

    speaker_id = NumberAttribute(hash_key=True, default=random_id(is_str=False))
    id = UnicodeAttribute(null=True, default=random_id(is_uuid=True))
    speaker_name = UnicodeAttribute(null=True)
    owner_id = UnicodeAttribute(null=True)
    owner_name = UnicodeAttribute(null=True, default='IkonVoiceLite')

    serial_number = UnicodeAttribute(null=True)
    labels = ListAttribute(default=None, null=True)
    country = UnicodeAttribute(null=True)
    city = UnicodeAttribute(null=True)
    # category string. Possible values: 'news', 'entertainment', 'education', 'other'
    category = UnicodeAttribute(null=True, default="")
    emotions = ListAttribute(default=None, null=True)
    description = UnicodeAttribute(default='', null=True)
    ai_description = UnicodeAttribute(default='', null=True)
    age_style = UnicodeAttribute(null=True)
    age = NumberAttribute(null=True, default=22)
    custom_tts_price = NumberAttribute(null=True)
    untrained_duration = NumberAttribute(default=0)

    platform = UnicodeAttribute(null=True)
    platform_id = UnicodeAttribute(null=True)

    base_platform = UnicodeAttribute(null=True)
    base_platform_id = UnicodeAttribute(null=True)

    is_custom = BooleanAttribute(default=False)

    for_sale = BooleanAttribute(default=False)
    sale_price = NumberAttribute(null=True)
    for_rent = BooleanAttribute(default=False)
    rent_price = NumberAttribute(null=True)
    level = NumberAttribute(default=1)

    score = NumberAttribute(null=True)
    creation_date = UTCDateTimeAttribute(default=datetime.utcnow)
    speaker_owner_index = SpeakerOwnerIndex()

    audio = UnicodeAttribute(default='https://celebai-celeb-images-public.s3.ap-southeast-1.amazonaws.com/audio_samples'
                                     '/el-GR-AthinaNeural_azure.wav')
    eng_name = UnicodeAttribute(default='Athina')
    real_name = UnicodeAttribute(null=True)
    face_image = UnicodeAttribute(default='https://celebai-celeb-images-public.s3.ap-southeast-1.amazonaws.com/1.png')
    gender = UnicodeAttribute(default='ผู้หญิง')
    gender_value = NumberAttribute(default=0)
    horizontal_face_image = UnicodeAttribute(default='')
    image = UnicodeAttribute(default='https://celebai-celeb-images-public.s3.ap-southeast-1.amazonaws.com/1.png')
    language = UnicodeAttribute(default='en-US')
    other_languages = ListAttribute(default=None, null=True)
    popularity = UnicodeAttribute(default="")
    popularity_amount = NumberAttribute(default=0)
    rating = NumberAttribute(default=0)
    rating_count = NumberAttribute(default=0)
    speech_style = ListAttribute(default=None, null=True)
    speed = UnicodeAttribute(default='')
    square_image = UnicodeAttribute(default='https://celebai-celeb-images-public.s3.ap-southeast-1.amazonaws.com/square'
                                            '_face/1.png')
    status = BooleanAttribute(default=True)
    thai_name = UnicodeAttribute(default='')
    type = NumberAttribute(default=0)
    voice_style = ListAttribute(default=None, null=True)
    relative_ids = ListAttribute(default=None, null=True)
    last_sampling_date = UTCDateTimeAttribute(null=True)
    tribe = UnicodeAttribute(null=True)
    times_used = NumberAttribute(default=0)
    is_premium = BooleanAttribute(default=False)
    is_partner = BooleanAttribute(default=False)
    is_featured = BooleanAttribute(default=False)
    attributes_string = UnicodeAttribute(null=True)
    attributes_hash = UnicodeAttribute(null=True)
    accents = ListAttribute(of=UnicodeAttribute, default=list)

    order_of_importance = NumberAttribute(default=0)
    social_media = SocialMediaAccounts(null=True)
    hash_id = UnicodeAttribute(null=True)

    is_market = NumberAttribute(default=0)
    market_sort_score = NumberAttribute(default=0)
    market_score_index = MarketScoreIndex()

    speaker_popularity_index = SpeakerPopularityIndex()

    @property
    def tts_price(self):
        return self.custom_tts_price or self.default_tts_price

    @property
    def default_tts_price(self):
        if self.popularity_amount < 500 and self.rating in [3, 4]:
            price = 1
        elif self.popularity_amount > 500 and self.rating in [3, 4]:
            price = 2
        elif self.popularity_amount < 500 and self.rating == 5:
            price = 2
        elif self.popularity_amount > 500 and self.rating == 5:
            price = 3
        else:
            price = 1

        return price

    def to_dict(self, reduced=False):
        rval = {}
        if reduced:
            attributes = ["speaker_id", "speaker_name", "category", "ai_description", "labels", "accents", "hash_id",
                          "age_style", "age", "is_custom", "audio", "popularity", "image", "language",
                          "gender_value", "tribe", "serial_number", "is_premium", "is_partner", "is_featured"]
        else:
            attributes = [key for key in self.get_attributes().keys()]

        for key in attributes:
            value = getattr(self, key)
            if isinstance(value, datetime):
                from pytz import timezone
                value = value.astimezone(timezone('Asia/Bangkok')).isoformat()
            elif isinstance(value, SocialMediaAccounts):
                value = value.as_dict()

            rval[key] = value

        rval["tts_price"] = self.tts_price
        rval["default_tts_price"] = self.tts_price

        # rval.pop("custom_tts_price", None)

        return rval

    def save(self, conditional_operator=None, **expected_values):
        try:
            speaker_text = speaker_to_text(self)
            speaker_hash = speaker_text + str(self.is_market)
            self.market_sort_score = self.calculate_market_sort_score()
            self.is_market = 1 if self.for_rent or self.for_sale else 0

            if self.attributes_hash is not None and self.attributes_hash == speaker_hash:
                super().save()
                return

            self.attributes_string = speaker_text
            self.attributes_hash = speaker_hash

            if not self.hash_id:
                from hashlib import sha256
                self.hash_id = sha256(self.id.encode()).hexdigest()

            super().save()
            if not self.is_market:
                try:
                    delete_item_from_index(self.speaker_id, "id", SPEAKER_INDEX)
                except Exception as e:
                    print(f"Error deleting speaker from index: {e}")
                return

            speaker_embedding = get_embedding_from_bedrock_cohere(speaker_text)
            query = {
                "query": {
                    "match": {
                        "id": str(self.speaker_id)
                    }
                }
            }
            doc = {
                "id": str(self.speaker_id),
                "speaker-vector": speaker_embedding
            }
            create_update_item(query=query, document=doc, index_name=SPEAKER_INDEX)
        except Exception as e:
            print(f"Error saving speaker to index: {e}")

    def delete(self, conditional_operator=None, **expected_values):
        super().delete()

        try:
            delete_item_from_index(self.speaker_id, "id.keyword", SPEAKER_INDEX)
        except Exception as e:
            print(f"Error deleting speaker from index: {e}")

    def calculate_market_sort_score(self):
        score = 0
        score += 100_000 * int(self.is_partner)
        score += 50_000 * int(self.is_featured)
        score += (sigmoid(self.order_of_importance/100) - 0.5) * 10_000 if self.order_of_importance else 0
        score += 10 if self.language.startswith("en") else 0

        score += self.rating if self.rating else 0
        return score


from enum import Enum


class TrainingStatus(Enum):
    NOT_TRAINED = 0
    TRAINED = 1
    FAILED_TO_TRAINED = -1
    UNTRAINABLE = -2


class SpeakerTraining(Model):
    """
    A case model class for pynamodb
    """

    class Meta:
        table_name = "SpeakerTraining"
        region = "ap-southeast-1"
        billing_mode = 'PAY_PER_REQUEST'

    speaker_id = NumberAttribute(hash_key=True)
    sentence_id = NumberAttribute(range_key=True)
    score = NumberAttribute(null=True)
    transcript = UnicodeAttribute(null=True)
    duration = NumberAttribute(null=True)
    creation_date = UTCDateTimeAttribute(default=datetime.utcnow)
    training_state = NumberAttribute(default=TrainingStatus.NOT_TRAINED.value)

    def to_dict(self):
        rval = {}
        for key, _ in self.get_attributes().items():
            value = getattr(self, key)
            if isinstance(value, datetime):
                from pytz import timezone
                value = value.astimezone(timezone('Asia/Bangkok')).isoformat()

            rval[key] = value

        return rval


# Function to count the number of items with trained=False for a given speaker_id
def get_untrained_items(speaker_id):
    items = []

    # Execute the query for each speaker_id and sentence_id combination
    for item in SpeakerTraining.query(speaker_id):
        if item.training_state == TrainingStatus.NOT_TRAINED.value and item.score >= MINIMUM_SCORE:
            items.append(item)

    return items

# Create the table if it does not exist
# if not Speaker.exists():
#     Speaker.create_table(wait=True)
#
# Create the table if it does not exist
# if not SpeakerTraining.exists():
#     SpeakerTraining.create_table(wait=True)
#
# Create the table if it does not exist
# if not SpeakerRenting.exists():
#     SpeakerRenting.create_table(wait=True)


# Create the table if it does not exist
# if not SpeakerFavorite.exists():
#     SpeakerFavorite.create_table(wait=True)

# Create the table if it does not exist
# if not TrainingSentence.exists():
#     TrainingSentence.create_table(wait=True)


# Create the table if it does not exist
# if not SpeakerRating.exists():
#     SpeakerRating.create_table(wait=True)

# Create the table if it does not exist
# if not SpeakerRecents.exists():
#     SpeakerRecents.create_table(wait=True)
