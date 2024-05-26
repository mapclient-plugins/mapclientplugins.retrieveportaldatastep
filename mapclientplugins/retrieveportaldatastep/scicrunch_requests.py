from urllib.parse import quote_plus


def _get_facet_type_map():
    return {
        'species': ['organisms.primary.species.name.aggregate', 'organisms.sample.species.name.aggregate', 'organisms.scaffold.species.name.aggregate'],
        'gender': ['attributes.subject.sex.value'],
        'sex': ['attributes.subject.sex.value'],
        'genotype': ['anatomy.organ.name.aggregate'],
        'anatomical structure': ['anatomy.organ.name.aggregate'],
        'organ': ['anatomy.organ.name.aggregate'],
        'experimental approach': ['item.modalities.keyword'],
        'age categories': ['attributes.subject.ageCategory.value']
    }


def _facet_query_string(query, facets, type_map):
    # We will create AND OR structure. OR within facets and AND between them
    # Example Output:
    #
    # "heart AND attributes.subject.sex.value:((male) OR (female))"

    # Add search query if it exists
    qt = ""
    if query != "":
        qt = f'{query}'

    for k in facets:
        if qt and len(facets[k]) > 0:
            qt += " AND "
            break

    # Add the brackets for OR and AND parameters
    remove_last_and = False
    for k, values in facets.items():

        k = k.lower()
        if k == "datasets":
            needParentheses = (qt or len(facets) > 1) and (len(values) > 1)
            if needParentheses:
                qt += "("
            for entry in values:
                if entry == "scaffolds":
                    qt += "objects.additional_mimetype.name:(application%2fx.vnd.abi.scaffold.meta%2Bjson)"
                if entry is not values[-1]:
                    qt += " OR "  # 'OR' if more terms in this facet are coming
            if needParentheses:
                qt += ")"
        else:
            if len(values):
                qt += "("
                for m in type_map[k]:
                    qt += m + ":("  # facet term path and opening bracket
                    for entry in values:
                        qt += f"({entry})"  # bracket around terms incase there are spaces
                        if entry is not values[-1]:
                            qt += " OR "  # 'OR' if more terms in this facet are coming
                        else:
                            qt += ")"
                    if m is not type_map[k][-1]:
                        qt += " OR "
                qt += ")"

                remove_last_and = True
                qt += " AND "

    if remove_last_and:
        qt = qt.removesuffix(" AND ")

    return qt


def create_filter_request(query, facets, size, start, fields=None):
    if size is None:
        size = 10
    if start is None:
        start = 0

    if not query and not facets:
        return {"size": size, "from": start}

    query = quote_plus(query)

    # Data structure of a sci-crunch search
    data = {
        "size": size,
        "from": start,
        "query": {
            "query_string": {
                "query": ""
            }
        }
    }
    if fields:
        data["query"]["query_string"]["fields"] = fields

    qs = _facet_query_string(query, facets, _get_facet_type_map())
    data["query"]["query_string"]["query"] = qs
    return data


def form_scicrunch_match_request(match_field, match_value, source_fields):
    return {
        "size": 20,
        "from": 0,
        "query": {
            "match": {
                "item.curie": "DOI:10.26275/d52i-yves"
            }
        },
        "_source": source_fields
    }
