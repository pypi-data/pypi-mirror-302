import json

import boto3
import pycountry
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth

from database.song import Song
from utils.sentry_tool import manage_exception
from settings import DATABASE_HOST, REGION, SERVICE


class DeleteItemException(Exception):
    def __init__(self, message):
        self.message = message


def get_opensearch_client():
    credentials = boto3.Session().get_credentials()
    auth = AWSV4SignerAuth(credentials, REGION, SERVICE)

    client = OpenSearch(
        hosts=[{'host': DATABASE_HOST, 'port': 443}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        pool_maxsize=20
    )
    return client


def assume_role(role_arn, session_name):
    sts_client = boto3.client('sts')
    assumed_role_object = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName=session_name
    )
    return assumed_role_object['Credentials']


def get_client_assuming_role():
    role_arn = 'arn:aws:iam::360122305252:role/aws-elasticbeanstalk-ec2-role'  # Replace with your role ARN
    session_name = 'YourSessionName'  # Replace with your session name

    # Assume the role
    credentials = assume_role(role_arn, session_name)

    auth = AWSV4SignerAuth(
        boto3.Session(
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        ).get_credentials(), REGION, SERVICE
    )

    client = OpenSearch(
        hosts=[{'host': DATABASE_HOST, 'port': 443}],
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        pool_maxsize=20
    )
    return client


def get_country_and_accent(language_code):
    parts = language_code.split('-')
    language = pycountry.languages.get(alpha_2=parts[0])
    country = pycountry.countries.get(alpha_2=parts[1])

    if language and country:
        language_name = language.name
        country_name = country.name
        accent = f"{country_name} accent"
        return country_name, language_name, accent
    else:
        return None, None, None


def speaker_to_text(speaker):
    text = "Give me a short biography for a speaker with the following attributes\n"
    text += f"name: {speaker.speaker_name}\n"
    age = speaker.age
    age_description = "young" if age < 30 else "middle-aged" if age < 60 else "old"
    text += f"age: {age_description}\n"

    emotions = None
    labels = None
    speech_style = None

    if speaker.emotions:
        emotions = ', '.join(speaker.emotions) if len(speaker.emotions) > 0 else None
    if speaker.labels:
        labels = ', '.join(speaker.labels or []) if len(speaker.labels) > 0 else None
    if speaker.speech_style:
        speech_style = ', '.join(speaker.speech_style or []) if len(speaker.speech_style) > 0 else None

    country_name = None
    language_name = None
    accent = None

    if speaker.language:
        country_name, language_name, accent = get_country_and_accent(speaker.language)

    if country_name:
        text += f", country: {country_name}\n"
    if language_name:
        text += f", language: {language_name}\n"
    if accent:
        text += f", accent: {accent}\n"

    text += f", description: {speaker.description}\n"

    if emotions:
        text += f", emotions: {emotions}\n"
    if labels:
        text += f", lables: {labels}\n"
    if speech_style:
        text += f", speech style: {speech_style}\n"

    return text


def song_to_text(song: Song):
    # Extract relevant fields from the song object
    title = song.title
    tags = ', '.join(song.tags) if len(song.tags) > 0 else None

    string_to_embed = f"Give me a short description for a song with these attributes: title - {title}"

    # add extra details to the string if available
    if tags:
        string_to_embed = string_to_embed + ", " + f"tags - [{tags}]"

    return string_to_embed


def get_embedding_from_bedrock_titan(text: str, region_name: str = 'ap-southeast-1'):
    client = boto3.client('bedrock-runtime', region_name=region_name)
    model_id = "amazon.titan-embed-text-v2:0"
    native_request = {"inputText": text}
    request = json.dumps(native_request)
    response = client.invoke_model(modelId=model_id, body=request)
    model_response = json.loads(response["body"].read())
    embedding = model_response["embedding"]
    return embedding


def get_embedding_from_bedrock_cohere(text: str, input_type: str = "search_query", region_name: str = 'ap-southeast-1'):
    client = boto3.client('bedrock-runtime', region_name=region_name)
    model_id = "cohere.embed-english-v3"
    native_request = {"texts": [text], "input_type": input_type}
    request = json.dumps(native_request)
    response = client.invoke_model(modelId=model_id, body=request)
    model_response = json.loads(response["body"].read())
    embeddings = model_response["embeddings"][0]
    return embeddings


def id_search(item_id: str, index_name: str, num_results: int = 10):
    try:
        client = get_opensearch_client()
        k = num_results  # Number of nearest neighbors to find
        q = {
            "size": k,
            "query": {"match": {"id": str(item_id)}}
        }

        # Execute the search
        response = client.search(index=index_name, body=q)
        return response["hits"]["hits"]
    except Exception as e:
        print(f"unexpected error: {e}")
        return []


def invoke_lambda(function_name: str, body: dict, invocation_type: str):
    '''
    :param function_name: Name of the lambda function
    :param body: body to pass into the lambda function. Should be a dictionary
    :param invocation_type: either Event or RequestResponse. Event for async, RequestResponse for sync
    '''
    try:
        client = boto3.client("lambda", region_name=REGION)

        response = client.invoke(
            FunctionName=function_name,
            InvocationType=invocation_type,
            Payload=json.dumps({"body": json.dumps(body)})
        )
        return response
    except Exception as e:
        return manage_exception(e)


def _get_search_results(query: dict, index_name: str, oss_host: str, region: str, service: str):
    try:
        function_name = "semantic-search-master"
        body = {
            "query": query,
            "index_name": index_name,
            "oss_host": oss_host,
            "region": region,
            "service": service
        }

        response = invoke_lambda(function_name, body, "RequestResponse")
        payload = response['Payload'].read()
        payload_body = json.loads(payload.decode())['body']
        results = json.loads(payload_body)['results']
        return results
    except Exception as e:
        print("could not get search results: ", e)
        return []


def _create_knn_query(num_results, vector_name, embedding):
    query = {
        "knn": {
            vector_name: {
                "vector": embedding,
                "k": num_results
            }
        }
    }

    return query


def _create_query(num_results, page, vector_name, embedding, filters=None):
    """
    Creates a query for AWS OpenSearch with optional filters.

    Args:
    - num_results (int): Number of results to return.
    - page (int): The page number for pagination.
    - vector_name (str): Name of the vector field.
    - embedding (list): The query vector.
    - filters (dict): Dictionary of filters to apply. Example: {"premium": True, "field2": "value"}.

    Returns:
    - dict: The generated OpenSearch query.
    """

    if filters is not None and page != 0:
        raise ValueError("Pagination is not supported with filters")

    filters = filters if filters is not None else []

    query = {
        "size": num_results
    }

    if page != 0:
        query["from"] = page * num_results

    if filters == []:
        query["query"] = _create_knn_query(num_results, vector_name, embedding)
        print("normal query, no filters")
    else:
        query["query"] = {
            "bool": {
                "must": [_create_knn_query(num_results * 2, vector_name, embedding)],
                "filter": filters
            }
        }

    return query


def semantic_search(embedding, index_name: str, vector_name: str, num_results: int = 10, page=0, filters=None):
    try:

        query = _create_query(num_results, page, vector_name, embedding, filters)

        results = _get_search_results(query, index_name, DATABASE_HOST, REGION, SERVICE)
        return results
    except Exception as e:
        print("could not get search results: ", e)
        return []


def delete_item_from_index(item_id: int, field_name: str, index_name: str):
    function_name = "delete-from-index-master"
    body = {
        "item_id": item_id,
        "index_name": index_name,
        "oss_host": DATABASE_HOST,
        "region": REGION,
        "service": SERVICE,
        "field_name": field_name
    }

    response = invoke_lambda(function_name, body, "Event")

    return response


def create_update_item(query: dict, document: dict, index_name: str):
    try:
        function_name = "save-to-index-master"

        body = {
            "query": query,
            "document": document,
            "index_name": index_name,
            "oss_host": DATABASE_HOST,
            "region": REGION,
            "service": SERVICE
        }

        response = invoke_lambda(function_name, body, "Event")

        return response
    except Exception as e:
        print("could not add item to index: ", e)
        manage_exception(e)
