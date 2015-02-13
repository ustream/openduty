from settings import *

DEBUG = True
TEMPLATE_DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'database.sql',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': ''
    }
}

BASE_URL = "http://localhost:8000"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'devsecret'

PAGINATION_DEFAULT_PAGINATION = 3



#LDAP RELATED
AUTH_LDAP_SERVER_URI = "ldap://fqdn:389"
AUTH_LDAP_BIND_DN = ""
AUTH_LDAP_BIND_PASSWORD = ""
AUTH_LDAP_START_TLS = False
AUTH_LDAP_MIRROR_GROUPS = True #Mirror LDAP Groups as Django Groups, and populate them as well.
AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=Group,dc=domain,dc=com",
    ldap.SCOPE_SUBTREE, "(&(objectClass=posixGroup)(cn=openduty*))"
)
AUTH_LDAP_GROUP_TYPE = PosixGroupType()

AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=People,dc=domain,dc=com",
ldap.SCOPE_SUBTREE, "(uid=%(user)s)")

AUTH_LDAP_USER_ATTR_MAP = {
"first_name": "uid",
"last_name": "sn",
"email": "mail"
}

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
    'openduty.middleware.basicauthmiddleware',
)

