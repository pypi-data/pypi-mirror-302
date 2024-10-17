from .sentry_tool import manage_exception
import math

def random_id(lenght=10, is_str=True, is_uuid=False):
    import random, string

    if is_uuid:
        import uuid
        return str(uuid.uuid4())

    alphabet = string.digits  # string.ascii_lowercase

    if is_str:
        alphabet += string.ascii_lowercase

    identifier = ''.join(random.choices(alphabet, k=lenght))

    return identifier if is_str else int(identifier)


def update_item(item, updatable_fields=None, **items):
    non_updatable_fields = ["id", "speaker_id", "owner_id", "creation_date"]
    response = {}
    table = item.__class__
    warnings = {}
    for k, v in items.items():
        if k in non_updatable_fields:
            warnings[k] = f"it's not updatable, it's been skipped"
            print(warnings[k])
            continue

        if updatable_fields and k not in updatable_fields:
            warnings[k] = f"it's not updatable, it's been skipped"
            print(warnings[k])
            continue

        if k not in table.get_attributes():
            warnings[k] = f"it's not part of the {table.__name__} model, it's been skipped"
            print(warnings[k])
            continue

        print(f"Updating {k} from {getattr(item, k)} to {v}")
        setattr(item, k, v)

    try:
        item.save()
    except Exception as e:
        response["error"] = manage_exception(e)
    else:
        response = item.to_dict()
        if warnings:
            response["warnings"] = warnings

    return response

def sigmoid(x):
    return 1 / (1 + math.exp(-x))