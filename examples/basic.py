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


ds = dgu.datasets()



dgu.dataset()
