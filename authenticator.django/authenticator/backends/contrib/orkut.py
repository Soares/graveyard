"""
Orkut OAuth support.

This contribution adds support for Orkut OAuth service. The scope is
limited to http://orkut.gmodules.com/social/ by default, but can be
extended with ORKUT_EXTRA_SCOPE on project settings. Also name, display
name and emails are the default requested user data, but extra values
can be specified by defining ORKUT_EXTRA_DATA setting.

OAuth settings ORKUT_CONSUMER_KEY and ORKUT_CONSUMER_SECRET are needed
to enable this service support.
"""
import urllib

from django.conf import settings
from django.utils import simplejson

from authenticator.backends import OAuthBackend
from authenticator.backends.google import BaseGoogleOAuth


# Orkut configuration
# default scope, specify extra scope in settings as in:
# ORKUT_EXTRA_SCOPE = ['...']
ORKUT_SCOPE = ['http://orkut.gmodules.com/social/']
ORKUT_REST_ENDPOINT = 'http://www.orkut.com/social/rpc'
ORKUT_DEFAULT_DATA = 'name,displayName,emails'


class OrkutBackend(OAuthBackend):
    """Orkut OAuth authentication backend"""
    name = 'orkut'

    def get_user_details(self, response):
        """Return user details from Orkut account"""
        return {'email': response['emails'][0]['value'],
                'fullname': response['displayName'],
                'nickname': response['displayName'],
                'first_name': response['name']['givenName'],
                'last_name': response['name']['familyName']}


class OrkutAuth(BaseGoogleOAuth):
    """Orkut OAuth authentication mechanism"""
    AUTH_BACKEND = OrkutBackend
    SETTINGS_KEY_NAME = 'ORKUT_CONSUMER_KEY'
    SETTINGS_SECRET_NAME = 'ORKUT_CONSUMER_SECRET'

    def user_data(self, access_token):
        """Loads user data from Orkut service"""
        fields = ORKUT_DEFAULT_DATA
        if hasattr(settings, 'ORKUT_EXTRA_DATA'):
            fields += ',' + settings.ORKUT_EXTRA_DATA
        scope = ORKUT_SCOPE + getattr(settings, 'ORKUT_EXTRA_SCOPE', [])
        params = {'method': 'people.get',
                  'id': 'myself',
                  'userId': '@me',
                  'groupId': '@self',
                  'fields': fields,
                  'scope': ' '.join(scope)}
        request = self.oauth_request(access_token, ORKUT_REST_ENDPOINT, params)
        response = urllib.urlopen(request.to_url()).read()
        try:
            return simplejson.loads(response)['data']
        except (ValueError, KeyError):
            return None


# Backend definition
BACKENDS = {
    'orkut': OrkutAuth,
}
