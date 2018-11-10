import datagovuk as dgu

rsc = dgu.resources()

exts = rsc[rsc['format'].str.lower() == 'geojson']['format'].unique().tolist()
geo_resources = rsc[rsc['format'].isin(exts)].iloc[0]

geo = dgu.resource(geo_resources)

if geo is not None:
    print(geo.head())
