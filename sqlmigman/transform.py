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
            regex = r'\$\((.*?)%%%s%%(.*?)\)' % name
            for m in re.finditer(regex, templ):
                old = ''.join(['$(', m.group(1),
                               '%', name, '%',
                               m.group(2), ')'])
                new = ''.join([m.group(1), value, m.group(2)])
                templ = templ.replace(old, new)
            templ = templ.replace(''.join(['%', name, '%']), str(value))

    # Cleaning undefined $( -flag %param%) and %param%
    templ = re.sub(r'\$\(.*?\)', '', templ)
    templ = templ = re.sub(r'%\w+%', '', templ)
    return templ
