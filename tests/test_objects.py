"""
Tests for the paperwork.objects module
"""

# pylint: disable=missing-docstring

from paperwork import Bookmark, Folder


class TestBookmark:

    """Tests for the Bookmark class"""

    @staticmethod
    def test_create_bookmark():

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

    @staticmethod
    def test_bookmark_from_json():

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


class TestFolder:

    """Tests for the Folder class"""

    @staticmethod
    def test_create_folder():

        folder = Folder(
            folder_id="ID",
            title="TITLE",
            slug="SLUG",
        )

        assert folder.id == "ID"
        assert folder.title == "TITLE"
        assert folder.slug == "SLUG"

    @staticmethod
    def test_folder_from_json():

        json = {
            "folder_id": "ID",
            "title": "TITLE",
            "slug": "SLUG",
        }

        folder = Folder.from_json(json)

        assert folder.id == "ID"
        assert folder.title == "TITLE"
        assert folder.slug == "SLUG"
