import html


def escape_html(unsafe: str):
    safe = html.escape(unsafe)

    return safe


# Manual replacement.
# Escape "&" with "&amp;" first because otherwise it'd replace the other replacements.
# ---
# html_key = {"<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&apos;"}

# def escape_html(unsafe: str):
#     for key in html_key.keys():
#         unsafe = unsafe.replace(key, html_key[key])

#     return unsafe
