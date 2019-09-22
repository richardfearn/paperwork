def _quote_str(s):
    return '"%s"' % s if s is not None else "None"


class Bookmark:

    def __init__(self, id=None, description=None, time=None, title=None, url=None):
        self.id = id
        self.description = description
        self.time = time
        self.title = title
        self.url = url

    def __repr__(self):
        return "Bookmark[id=%s, title=%s, url=%s]" % (self.id, _quote_str(self.title), _quote_str(self.url))

    @staticmethod
    def from_json(json):
        return Bookmark(
            id=json["bookmark_id"],
            description=json["description"],
            time=json["time"],
            title=json["title"],
            url=json["url"],
        )


class Folder:

    def __init__(self, id=None, title=None, slug=None):
        self.id = id
        self.title = title
        self.slug = slug

    def __repr__(self):
        return "Folder[id=%s, title=%s]" % (self.id, _quote_str(self.title))

    @staticmethod
    def from_json(json):
        return Folder(
            id=json["folder_id"],
            title=json["title"],
            slug=json["slug"]
        )


UNREAD_FOLDER = Folder(id=0, title="unread")

ARCHIVE_FOLDER = Folder(id="archive", title="archive")
