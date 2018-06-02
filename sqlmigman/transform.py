"""sqlmigman cmd template transformer"""
import re


def transform(template, *args):
    templ = template
    for arg in args:
        for name, value in arg.items():
            # TODO: This is a hack to ignore unset values.
            # Find a way to not passe None values
            if value is None:
                continue
            regex = '\$\((.*?)%%%s%%(.*?)\)' % name
            for m in re.finditer(regex, templ):
                old = ''.join(['$(', m.group(1),
                               '%', name, '%',
                               m.group(2), ')'])
                new = ''.join([m.group(1), value, m.group(2)])
                templ = templ.replace(old, new)
            templ = templ.replace(''.join(['%', name, '%']), str(value))

    # Cleaning undefined $( -flag %param%) and %param%
    templ = re.sub('\$\(.*?\)', '', templ)
    templ = templ = re.sub('%\w+%', '', templ)
    return templ
