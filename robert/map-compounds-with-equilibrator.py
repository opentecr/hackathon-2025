import equilibrator_api
cc = equilibrator_api.ComponentContribution
cpd = cc.search_compound("norpyridoxal")
cc.search_compound_by_inchi_key("YBAZINRZQSAIAY-UHFFFAOYSA-N")
cpd.get_common_name()
cpd.identifiers

