from paperwork import Bookmark, Folder


class TestObjects:

    def test_create_bookmark(self):

        bookmark = Bookmark(
            bookmark_id="ID",
            description="DESCRIPTION",
            time="TIME",
            title="TITLE",
            url="URL",
        )

        assert bookmark.id == "ID"
        assert bookmark.description == "DESCRIPTION"
        assert bookmark.time == "TIME"
        assert bookmark.title == "TITLE"
        assert bookmark.url == "URL"

    def test_bookmark_from_json(self):

        json = {
            "bookmark_id": "ID",
            "description": "DESCRIPTION",
            "time": "TIME",
            "title": "TITLE",
            "url": "URL",
        }

        bookmark = Bookmark.from_json(json)

        assert bookmark.id == "ID"
        assert bookmark.description == "DESCRIPTION"
        assert bookmark.time == "TIME"
        assert bookmark.title == "TITLE"
        assert bookmark.url == "URL"

    def test_create_folder(self):

        folder = Folder(
            folder_id="ID",
            title="TITLE",
            slug="SLUG",
        )

        assert folder.id == "ID"
        assert folder.title == "TITLE"
        assert folder.slug == "SLUG"

    def test_folder_from_json(self):

        json = {
            "folder_id": "ID",
            "title": "TITLE",
            "slug": "SLUG",
        }

        folder = Folder.from_json(json)

        assert folder.id == "ID"
        assert folder.title == "TITLE"
        assert folder.slug == "SLUG"
