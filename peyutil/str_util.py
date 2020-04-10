#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python 2 to 3 dealing with unicode....
import sys
import re

# noinspection PyUnresolvedReferences
if sys.version_info.major == 2: # pragma: no cover
    # noinspection PyCompatibility,PyUnresolvedReferences
    from cStringIO import StringIO
    import codecs
    import urllib

    # noinspection PyUnresolvedReferences
    # primitive_string_types and UNICODE useful for isinstance checks
    primitive_string_types = (str, unicode)
    UNICODE = unicode
    urlencode = urllib.urlencode

    # noinspection PyUnresolvedReferences
    def is_str_type(x):
        # noinspection PyCompatibility
        return isinstance(x, basestring)


    def is_int_type(x):
        # noinspection PyUnresolvedReferences
        return isinstance(x, int) or isinstance(x, long)


    def get_utf_8_string_io_writer():
        string_io = StringIO()
        wrapper = codecs.getwriter("utf8")(string_io)
        return string_io, wrapper


    def flush_utf_8_writer(wrapper):
        wrapper.reset()


    def reverse_dict(d):
        # noinspection PyCompatibility
        return {v: k for k, v in d.iteritems()}


else:
    from io import StringIO  # pylint: disable=E0611,W0403
    import urllib.parse
    urlencode = urllib.parse.urlencode
    UNICODE = str
    primitive_string_types = (str,)


    def is_str_type(x):
        return isinstance(x, str)


    def is_int_type(x):
        return isinstance(x, int)


    def get_utf_8_string_io_writer():
        """Returns a (strio, wrapper) tuple. Backward compat. layer for 2.7

        1. wrapper.write(...) operations support adding content
        2. When write's are done: call flush_utf_8_writer(wrapper)
        3. the string can be recovered using strio.getvalue()
            * (you'll need to call strio.getvalue().decode('utf-8')
               if you are in Python 2.7)
        """
        string_io = StringIO()
        return string_io, string_io


    # noinspection PyUnusedLocal
    def flush_utf_8_writer(wrapper):
        """You must call this on wrapper instance from
         get_utf_8_string_io_writer when done writing.

         NO-Op in python 3.
         """
        pass


    def reverse_dict(d):
        return {v: k for k, v in d.items()}


def slugify(s):
    """Convert any string to a "slug", a simplified form suitable for filename and URL part.
     EXAMPLE: "Trees about bees" => 'trees-about-bees'
     EXAMPLE: "My favorites!" => 'my-favorites'
    N.B. that its behavior should match this client-side slugify function, so
    we can accurately "preview" slugs in the browser:
     https://github.com/OpenTreeOfLife/opentree/blob/553546942388d78545cc8dcc4f84db78a2dd79ac/curator/static/js/curation-helpers.js#L391-L397
    TODO: Should we also trim leading and trailing spaces (or dashes in the final slug)?
    """
    slug = s.lower()  # force to lower case
    slug = re.sub('[^a-z0-9 -]', '', slug)  # remove invalid chars
    slug = re.sub(r'\s+', '-', slug)  # collapse whitespace and replace by -
    slug = re.sub('-+', '-', slug)  # collapse dashes
    if not slug:
        slug = 'untitled'
    return slug


def increment_slug(s):
    """Generate next slug for a series.

       Some docstore types will use slugs (see above) as document ids. To
       support unique ids, we'll serialize them as follows:
         TestUserA/my-test
         TestUserA/my-test-2
         TestUserA/my-test-3
         ...
    """
    slug_parts = s.split('-')
    # advance (or add) the serial counter on the end of this slug
    # noinspection PyBroadException
    try:
        # if it's an integer, increment it
        slug_parts[-1] = str(1 + int(slug_parts[-1]))
    except:
        # there's no counter! add one now
        slug_parts.append('2')
    return '-'.join(slug_parts)


def underscored2camel_case(v):
    """converts ott_id to ottId."""
    vlist = v.split('_')
    c = []
    for n, el in enumerate(vlist):
        if el:
            if n == 0:
                c.append(el)
            else:
                c.extend([el[0].upper(), el[1:]])
    return ''.join(c)
