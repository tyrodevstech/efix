from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushServerError,
    PushTicketError,
)
from requests.exceptions import ConnectionError, HTTPError
from django.contrib.auth.models import User
# Basic arguments. You should extend this function with the push features you
# want to use, or simply pass in a `PushMessage` object.
def send_push_message(token, title='', message='', extra=None):
    try:
        response = PushClient().publish(
            PushMessage(to=token,
                        title=title,
                        body=message,
                        data=extra))
    except PushServerError as exc:
        extra_data={
                'token': token,
                'message': message,
                'extra': extra,
                'errors': exc.errors,
                'response_data': exc.response_data,
        }
        # Encountered some likely formatting/validation error.
        print(extra_data)
    except (ConnectionError, HTTPError) as exc:
        # Encountered some Connection or HTTP error - retry a few times in
        # case it is transient.
        extra_data={'token': token, 'message': message, 'extra': extra}
        print(extra_data)

    try:
        # We got a response back, but we don't know whether it's an error yet.
        # This call raises errors so we can handle them with normal exception
        # flows.
        response.validate_response()
    except PushTicketError as exc:
        # Encountered some other per-notification error.
        extra_data={
                'token': token,
                'message': message,
                'extra': extra,
                'push_response': exc.push_response._asdict(),
        }
        print(extra_data)


def notify_admins(title='',message=''):
    for admin in User.objects.filter(is_superuser=True):
        if hasattr(admin,'userdevicetoken') and message:
            if admin.userdevicetoken.device_token:
                send_push_message(admin.userdevicetoken.device_token,title,message)