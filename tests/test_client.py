"""
Tests for the paperwork.client module
"""

# pylint: disable=missing-docstring

import random
import pytest

import paperwork
from paperwork import Bookmark, Folder, UNREAD_FOLDER, ARCHIVE_FOLDER

USERNAME = "richardfearn@gmail.com"


class TestClient:

    """Tests for the Client class"""

    @staticmethod
    @pytest.fixture
    def client():
        config = paperwork.Config()
        client = paperwork.Client(config, USERNAME)
        return client

    @staticmethod
    def test_list_folders(client):

        folders = client.list_folders()
        print(folders)
        assert folders is not None

    @staticmethod
    def test_list_bookmarks_in_unread(client):

        bookmarks = client.list_bookmarks(UNREAD_FOLDER)
        print(bookmarks)
        assert bookmarks is not None

    @staticmethod
    def test_list_bookmarks_in_archive(client):

        bookmarks = client.list_bookmarks(ARCHIVE_FOLDER)
        print(bookmarks)
        assert bookmarks is not None

    @staticmethod
    def test_list_bookmarks_in_user_folder(client):

        # create new folder
        new_folder_name = TestClient.random_folder_name()
        folder_to_add = Folder(title=new_folder_name)
        added_folder = client.add_folder(folder_to_add)
        print(added_folder)

        bookmarks = client.list_bookmarks(added_folder)
        assert bookmarks is not None

        # delete folder
        client.delete_folder(added_folder)

    @staticmethod
    def test_delete_folder(client):

        # create new folder
        new_folder_name = TestClient.random_folder_name()
        folder_to_add = Folder(title=new_folder_name)
        added_folder = client.add_folder(folder_to_add)
        print(added_folder)

        folders_before = client.list_folders()
        assert new_folder_name in [f.title for f in folders_before]

        # delete folder
        client.delete_folder(added_folder)

        folders_after = client.list_folders()
        assert new_folder_name not in [f.title for f in folders_after]

    @staticmethod
    def test_add_folder(client):

        new_folder_name = TestClient.random_folder_name()

        folders_before = client.list_folders()
        assert new_folder_name not in [f.title for f in folders_before]

        # create new folder
        folder_to_add = Folder(title=new_folder_name)
        added_folder = client.add_folder(folder_to_add)
        print(added_folder)

        folders_after = client.list_folders()
        assert new_folder_name in [f.title for f in folders_after]

        # delete folder
        client.delete_folder(added_folder)

    @staticmethod
    def test_add_bookmark_to_unread(client):

        TestClient._test_add_bookmark_to_folder(client, UNREAD_FOLDER)

    @staticmethod
    def test_add_bookmark_to_user_folder(client):

        # create folder
        temp_folder_title = TestClient.random_folder_name()
        folder_to_add = Folder(title=temp_folder_title)
        temp_folder = client.add_folder(folder_to_add)

        TestClient._test_add_bookmark_to_folder(client, temp_folder)

        client.delete_folder(temp_folder)

    @staticmethod
    def _test_add_bookmark_to_folder(client, folder):

        bookmarks_before = client.list_bookmarks(folder)

        url = "https://www.bbc.co.uk/news/uk-politics-49651969"

        bookmark_to_add = Bookmark(url=url)
        new_bookmark = client.add_bookmark(bookmark_to_add, folder)
        print(new_bookmark)
        assert new_bookmark is not None
        assert new_bookmark.id not in [b.id for b in bookmarks_before]

        bookmarks_after = client.list_bookmarks(folder)
        assert new_bookmark.id in [b.id for b in bookmarks_after]

    @staticmethod
    def test_delete_bookmark(client):

        # create folder
        temp_folder_title = TestClient.random_folder_name()
        folder_to_add = Folder(title=temp_folder_title)
        temp_folder = client.add_folder(folder_to_add)

        url = "https://www.bbc.co.uk/news/uk-politics-49651969"

        bookmark_to_add = Bookmark(url=url)
        new_bookmark = client.add_bookmark(bookmark_to_add, temp_folder)
        print(new_bookmark)
        assert new_bookmark is not None

        bookmarks_before = client.list_bookmarks(temp_folder)
        assert new_bookmark.id in [b.id for b in bookmarks_before]

        client.delete_bookmark(new_bookmark)

        bookmarks_after = client.list_bookmarks(temp_folder)
        assert new_bookmark.id not in [b.id for b in bookmarks_after]

        client.delete_folder(temp_folder)

    @staticmethod
    def test_move_bookmark_from_unread_to_user_folder(client):

        # create folder
        temp_folder_title = TestClient.random_folder_name()
        folder_to_add = Folder(title=temp_folder_title)
        temp_folder = client.add_folder(folder_to_add)

        url = "https://www.bbc.co.uk/news/uk-politics-49651969"
        bookmark_to_add = Bookmark(url=url)
        new_bookmark = client.add_bookmark(bookmark_to_add)

        client.move_bookmark(new_bookmark, temp_folder)

        bookmarks = client.list_bookmarks(temp_folder)
        assert len(bookmarks) == 1
        assert bookmarks[0].id == new_bookmark.id

        client.delete_folder(temp_folder)

    @staticmethod
    def test_move_bookmark_from_user_folder_to_unread(client):

        # create folder
        temp_folder_title = TestClient.random_folder_name()
        folder_to_add = Folder(title=temp_folder_title)
        temp_folder = client.add_folder(folder_to_add)

        url = "https://www.bbc.co.uk/news/uk-politics-49651969"
        bookmark_to_add = Bookmark(url=url)
        new_bookmark = client.add_bookmark(bookmark_to_add, temp_folder)

        client.move_bookmark(new_bookmark, UNREAD_FOLDER)

        bookmarks = client.list_bookmarks(UNREAD_FOLDER)
        assert new_bookmark.id in [b.id for b in bookmarks]

        client.delete_bookmark(new_bookmark)
        client.delete_folder(temp_folder)

    @staticmethod
    def random_folder_name():
        return "temp-" + str(random.randrange(10000, 100000))
