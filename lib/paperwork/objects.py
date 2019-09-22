def _quote_str(string):
    return '"%s"' % string if string is not None else "None"


class Bookmark:

    def __init__(self, bookmark_id=None, description=None, time=None, title=None, url=None):  # pylint: disable=too-many-arguments
        self.id = bookmark_id  # pylint: disable=invalid-name
        self.description = description
        self.time = time
        self.title = title
        self.url = url

    def __repr__(self):
        return "Bookmark[id=%s, title=%s, url=%s]" % (
            self.id,
            _quote_str(self.title),
            _quote_str(self.url),
        )

    @staticmethod
    def from_json(json):
        return Bookmark(
            bookmark_id=json["bookmark_id"],
            description=json["description"],
            time=json["time"],
            title=json["title"],
            url=json["url"],
        )


class Folder:

    def __init__(self, folder_id=None, title=None, slug=None):
        self.id = folder_id  # pylint: disable=invalid-name
        self.title = title
        self.slug = slug

    def __repr__(self):
        return "Folder[id=%s, title=%s]" % (
            self.id,
            _quote_str(self.title),
        )

    @staticmethod
    def from_json(json):
        return Folder(
            folder_id=json["folder_id"],
            title=json["title"],
            slug=json["slug"]
        )


UNREAD_FOLDER = Folder(folder_id=0, title="unread")

ARCHIVE_FOLDER = Folder(folder_id="archive", title="archive")
