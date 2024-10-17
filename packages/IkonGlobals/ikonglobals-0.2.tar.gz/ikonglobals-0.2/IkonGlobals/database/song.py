from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, ListAttribute
from utils.utils import random_id


class Song(Model):
    class Meta:
        table_name = 'Song'
        region = 'ap-southeast-1'
        billing_mode = 'PAY_PER_REQUEST'

    id = UnicodeAttribute(hash_key=True, default=lambda: random_id(is_uuid=True))
    key = UnicodeAttribute()
    key_preview = UnicodeAttribute(null=True)
    title = UnicodeAttribute()
    page_url = UnicodeAttribute()
    file_url = UnicodeAttribute()
    tags = ListAttribute(of=UnicodeAttribute)

    def to_dict(self):
        rval = {}
        for key, _ in self.get_attributes().items():
            rval[key] = getattr(self, key)

        return rval


if not Song.exists():
    Song.create_table(wait=True)
