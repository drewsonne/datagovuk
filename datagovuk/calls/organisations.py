from functools import reduce

import numpy as np

from datagovuk.calls.base import BaseCall


class FetchOrganisationStructureCall(BaseCall):
    indices = ['id']
    column_types = {
        'highlighted': 'bool',
        'parent': 'category'
    }
    cache_identifier = 'organisation_structure'
    columns = ['name', 'title', 'highlighted', 'parent']

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


class FetchAllOrganisationsCall(BaseCall):
    cache_identifier = 'all_organisations'

    def _fetch(self):
        call = FetchOrganisationStructureCall()
        orgs = call(self.session)
        ids = orgs.index.tolist()
        return ids
