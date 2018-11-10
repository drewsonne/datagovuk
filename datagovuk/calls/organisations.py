import json
import zlib
from functools import reduce

import numpy as np
import requests

from datagovuk.calls.base import BaseCall


class FetchOrganisationStructureCall(BaseCall):
    cache_identifier = 'organisation_structure'
    indices = ['id']
    column_types = {
        'highlighted': 'bool',
        'parent': 'category'
    }
    columns = ['id', 'name', 'title', 'highlighted', 'parent']

    def _fetch(self):
        return reduce(
            self._process_org_entry,
            self.session.action.group_tree(type='organization'),
            []
        )

    def _process_org_entry(self, orgs, org):
        if 'children' in org:
            orgs = reduce(
                lambda orgs_n, org_n: self._process_org_entry(
                    orgs_n,
                    {**org_n, **{'parent': org['id']}}
                ),
                org['children'],
                orgs
            )
            del org['children']
        else:
            org['parent'] = np.NAN
        orgs.append(org)
        return orgs


class FetchAllOrganisationsBaseCall(BaseCall):
    metadata_file_format = 'https://data.gov.uk/data/dumps/' \
                           'data.gov.uk-ckan-meta-data-{date}.organizations.jsonl.gz'
    facet = None

    def _fetch(self):
        return self._fetch_all()[self.facet]

    def _fetch_all(self):
        url = self._build_latest_metadata_url()
        r = requests.get(url)
        data_raw = zlib.decompress(r.content, 16 + zlib.MAX_WBITS).decode()
        users = []
        groups = []
        orgs = []
        for line in data_raw.splitlines():
            org = json.loads(line)
            for user in org['users']:
                users.append({
                    **user,
                    **{'org': org['id']}
                })
            del org['users']
            for group in org['groups']:
                groups.append({
                    **group,
                    **{'org': org['id']}
                })
            del org['groups']
            orgs.append(org)
        return {
            'organisations': orgs,
            'users': users,
            'groups': groups
        }

    def _build_latest_metadata_url(self, date=None):
        date_str = 'latest' if (date is None) else date.strftime("%Y-%m-%d")
        return self.metadata_file_format.format(
            date=date_str
        )


class FetchAllOrganisationsCall(FetchAllOrganisationsBaseCall):
    cache_identifier = 'all_organisations'
    facet = 'organisations'
    indices = ['id']
    columns = ['abbreviation', 'approval_status', 'category', 'contact-email', 'contact-name', 'contact-phone',
               'description', 'extras', 'foi-email', 'foi-name', 'foi-phone', 'foi-web', 'id', 'image_display_url',
               'image_url', 'is_organization', 'name', 'replaced_by', 'tags', 'title', 'type']

class FetchOrganisationUsersCall(FetchAllOrganisationsBaseCall):
    cache_identifier = 'all_organisations_users'
    facet = 'users'
    indices = ['name', 'org']
    column_types = {
        'capacity': 'category'
    }
    columns = ['name', 'capacity', 'org']

class FetchOrganisationGroupsCall(FetchAllOrganisationsBaseCall):
    cache_identifier = 'all_organisations_groups'
    facet = 'groups'
    indices = ['name', 'org']
    column_types = {
        'capacity': 'category'
    }
    columns = ['name', 'capacity', 'org']
