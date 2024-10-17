import sentry_sdk
from werkzeug.exceptions import NotFound, MethodNotAllowed

is_debugging = None


def manage_exception(exception, object_id="unknown", output_bucket=None, extra=None):
    from sentry_sdk import capture_exception
    import io, traceback, sys, boto3, json

    # if is_debugging:
    #     raise exception

    print("Exception caught for object", object_id)

    # Get the exception class name
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print(exc_type.__name__)

    # Get the exception message
    print("Exception:", exception)

    # Get the traceback
    traceback_str = io.StringIO()
    traceback.print_tb(exc_tb, file=traceback_str)
    print("Traceback:\n", traceback_str.getvalue())

    if not is_debugging:
        with sentry_sdk.push_scope() as scope:
            scope.set_tag("object_id", object_id)
            if extra:
                scope.set_extra("extras", extra)
            capture_exception(exception if not exception.__cause__ else exception.__cause__)

    output = {
        "type": exc_type.__name__,
        "message": str(exception),
        "traceback": traceback_str.getvalue()
    }

    if output_bucket:
        path = f"/tmp/{object_id}.json"

        with open(path, "wt") as f:
            f.write(json.dumps(output))

        print("uploading to s3")
        s3 = boto3.resource("s3")
        s3.Bucket(output_bucket).upload_file(path, f"errors/{object_id}.json")

    return output


def send_debug_sentry(message, object_id="unknown", extra=None):
    from sentry_sdk import capture_message

    print("DEBUG:", message)

    if is_debugging:
        print("Not running on a lambda. Skipping sentry")
        return

    with sentry_sdk.push_scope() as scope:
        scope.set_tag("object_id", object_id)
        if extra:
            scope.set_extra("extras", extra)
        capture_message(message)


def before_send(event, hint):
    # Check if the error is a 404 Not Found error
    if 'exc_info' in hint:
        exc_type, exc_value, exc_traceback = hint['exc_info']
        if (exc_type == NotFound and exc_value.code == 404) or (exc_type == MethodNotAllowed and exc_value.code == 405):
            # Optionally, log the event locally or handle it in another way
            return None  # Returning None will prevent the event from being sent to Sentry

    # Otherwise, send the event to Sentry
    return event


def init_sentry(dsn, is_debug=False):
    global is_debugging

    is_debugging = is_debug

    if is_debugging:
        print("Not running on a prod. Skipping sentry")
        return

    from sentry_sdk.integrations.flask import FlaskIntegration

    sentry_sdk.init(
        dsn=dsn,
        integrations=[
            FlaskIntegration(),
        ],
        traces_sample_rate=1.0,
        environment="dev" if is_debug else "prod",
        before_send=before_send
    )
