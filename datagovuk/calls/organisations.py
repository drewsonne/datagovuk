from functools import reduce

import pandas as pd

from datagovuk.cache import cache


class OrganisationStructureCall(object):
    def __call__(self, session):
        def _process_org_entry(orgs, org):
            if 'children' in org:
                orgs = reduce(
                    lambda orgs_n, org_n: _process_org_entry(
                        orgs_n,
                        {**org_n, **{'parent': org['id']}}
                    ),
                    org['children'],
                    orgs
                )
                del org['children']
            else:
                org['parent'] = None
            orgs.append(org)
            return orgs

        @cache('organisation_structure')
        def get_organisation_structure():
            orgs = reduce(
                _process_org_entry,
                session.action.group_tree(type='organization'),
                []
            )
            ids = list(set([o['id'] for o in orgs]))
            return pd.DataFrame(orgs, index=ids)

        orgDf = get_organisation_structure(). \
            set_index('id')
        orgDf['highlighted'] = orgDf['highlighted'].astype('bool')
        return orgDf
