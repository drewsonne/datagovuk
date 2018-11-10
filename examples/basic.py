import datagovuk as dgu

for call in [
    dgu.organisation_structure,
    dgu.organisations_groups,
    dgu.organisations_users,
    dgu.organisations,
    dgu.datasets,
    dgu.resources
]:
    print(call().info())
    print(call().head())
    print("\n\n")

rsc = dgu.resources()
organogram = rsc[
    (rsc.format == 'CSV') &
    (rsc.name == 'organogram-uk-statistics-authority')
    ].iloc[0]

dgu.resource(organogram).head()
