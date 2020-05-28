from cli.helpers.ObjDict import ObjDict


def get_component_parser(available_components):
    """Return comma-separated component list parser."""

    def parse_components(value):
        parsed_items = set(
            item_stripped
            for item in value.split(',')
            for item_stripped in [item.strip()]
            if item_stripped
        )

        if len(parsed_items) == 1:
            if 'all' in parsed_items:
                return set(available_components)
            if 'none' in parsed_items:
                return set()

        difference = parsed_items - set(available_components)
        if difference:
            raise Exception('Error parsing components: invalid values present')

        return parsed_items

    return parse_components


def components_to_dict(parsed_components, available_components):
    """Return an ObjDict of component -> boolean value pairs (enabled/disabled)."""

    parsed_components = frozenset(parsed_components)
    available_components = frozenset(available_components)

    difference = parsed_components - available_components
    if difference:
        raise Exception('Error parsing components: invalid values present')

    return ObjDict(
        (component_name, component_name in parsed_components)
        for component_name in available_components
    )
