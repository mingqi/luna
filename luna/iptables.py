import iptc


def get_chain(table, chain):
    for c in iptc.Table(table).chains:
        if c.name == chain:
            return c
    return None


def create_chain(table, chain):
    if get_chain(table, chain):
        raise Exception('{} has exists in table {}'.format(chain, table))
    iptc.Table(table).create_chain(chain)
    return get_chain(table, chain)


def rule(**rule):
    legal_attr = ['src', 'dst', 'in_interface', 'out_interface',
                  'protocol']
    rule = iptc.Rule()
    for attr_name, attr_value in rule:
        if attr_name == 'match':
            for match_name, match_options in attr_value.items():
                match = rule.create_match(match_name)
                for match_opt_name, match_opt_value in match_options:
                    setattr(match, match_opt_name, match_opt_value)

        if attr_name == 'target':
            rule.create_target(attr_value)

        if attr_name not in legal_attr:
            raise Exception('%s is not llegal rule attrubute' % attr_name)
        setattr(rule, attr_name, attr_value)
    return rule
