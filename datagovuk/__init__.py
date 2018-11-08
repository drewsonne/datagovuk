from ckanapi import RemoteCKAN

from datagovuk.cache import DataCache
from datagovuk.calls.organisations import FetchAllOrganisationsCall, FetchOrganisationStructureCall


class Api(RemoteCKAN):
    ENDPOINT = 'https://data.gov.uk/'

    DEFAULT = None

    def __init__(self):
        super().__init__(
            address=self.ENDPOINT
        )
        if Api.DEFAULT is None:
            Api.DEFAULT = self

    def session_wrapper(self, func):
        def default_session_handler(session=None, *args, **kwargs):
            if session is None:
                session = self.DEFAULT
            return func(*args, session=session, **kwargs)

        return default_session_handler


client = Api()

organisation_structure = client.session_wrapper(FetchOrganisationStructureCall())
organisations = client.session_wrapper(FetchAllOrganisationsCall())

# try:
#     __IPYTHON__
#     IPY = True
# except NameError:
#     IPY = False
