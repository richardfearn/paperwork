"""
paperwork client module

This module includes Client, the main class for making requests to Instapaper.
"""

# https://www.instapaper.com/api
# https://2.python-requests.org/en/master/user/quickstart/
# https://requests-oauthlib.readthedocs.io/en/latest/oauth1_workflow.html

import json
import logging
import requests
from requests_oauthlib import OAuth1
from paperwork.objects import Bookmark, Folder

API_URL_PREFIX = "https://www.instapaper.com/api/1"

LIST_FOLDERS = "/folders/list"
ADD_FOLDER = "/folders/add"
DELETE_FOLDER = "/folders/delete"
LIST_BOOKMARKS = "/bookmarks/list"
DELETE_BOOKMARK = "/bookmarks/delete"
MOVE_BOOKMARK = "/bookmarks/move"
ADD_BOOKMARK = "/bookmarks/add"
OAUTH_ACCESS_TOKEN = "/oauth/access_token"

FORMAT = "%(asctime)-15s %(levelname)-8s %(name)s - %(message)s"
logging.basicConfig(format=FORMAT)
LOGGER = logging.getLogger("paperwork")
LOGGER.setLevel(logging.INFO)


class Client:

    """Main class for making requests to Instapaper."""

    def __init__(self, config, username):

        self.config = config

        self.oauth = OAuth1(self.config.consumer_key(),
                            client_secret=self.config.consumer_secret(),
                            resource_owner_key=self.config.token(username),
                            resource_owner_secret=self.config.token_secret(username))

        self.request_timeout = 5
        self.max_retries = 10

    def list_folders(self):

        """Lists the user's folders."""

        data = self._do_request(LIST_FOLDERS)

        data = [o for o in data if o["type"] == "folder"]
        data = list(map(Folder.from_json, data))
        return data

    def list_bookmarks(self, folder, limit=500):

        """Lists the user's bookmarks."""

        data = self._do_request(LIST_BOOKMARKS, {
            "folder_id": folder.id,
            "limit": limit,
        })

        data = [o for o in data if o["type"] == "bookmark"]
        data = list(map(Bookmark.from_json, data))
        return data

    def move_bookmark(self, bookmark, folder):

        """Moves the specified bookmark to the specified folder."""

        data = self._do_request(MOVE_BOOKMARK, {
            "bookmark_id": bookmark.id,
            "folder_id": folder.id,
        })

        data = data[0]
        data = Bookmark.from_json(data)
        return data

    def delete_folder(self, folder):

        """Deletes the specified folder."""

        return self._do_request(DELETE_FOLDER, {
            "folder_id": folder.id,
        })

    def add_folder(self, folder):

        """Creates a folder."""

        data = self._do_request(ADD_FOLDER, {
            "title": folder.title,
        })

        data = data[0]
        data = Folder.from_json(data)
        return data

    def add_bookmark(self, bookmark, folder=None):

        """Adds a new unread bookmark to the user's account."""

        params = {
            "url": bookmark.url,
        }

        if bookmark.title is not None:
            params["title"] = bookmark.title

        if bookmark.description is not None:
            params["description"] = bookmark.description

        if folder is not None:
            params["folder_id"] = folder.id

        data = self._do_request(ADD_BOOKMARK, params)

        data = data[0]
        data = Bookmark.from_json(data)
        return data

    def delete_bookmark(self, bookmark):

        """Permanently deletes the specified bookmark."""

        return self._do_request(DELETE_BOOKMARK, {
            "bookmark_id": bookmark.id,
        })

    def _do_request(self, url, params=None):

        full_url = API_URL_PREFIX + url
        LOGGER.debug("Request URL: %s", full_url)
        LOGGER.debug("Request parameters: %s", params)

        data = None
        successful = False

        for attempt in range(1, self.max_retries+1):

            try:
                LOGGER.debug("Attempt %d", attempt)
                LOGGER.debug("Making request")

                response = requests.post(
                    url=full_url,
                    data=params,
                    auth=self.oauth,
                    timeout=self.request_timeout,
                )

                LOGGER.debug("Response: %s", response)
                LOGGER.debug("Response status: %d", response.status_code)

                data = response.text
                # print(data)

                if response.status_code == 200:
                    data = json.loads(data)
                    successful = True

                else:
                    LOGGER.warning(ATTEMPT_FAILED_MARKER)

            except requests.exceptions.RequestException:
                LOGGER.warning(ATTEMPT_FAILED_MARKER, exc_info=True)

            if successful:
                break

        LOGGER.debug("Final result: %s", successful)

        if not successful:
            raise Exception("Failed after %d attempts" % self.max_retries)

        return data


ATTEMPT_FAILED_MARKER = "@@@ ATTEMPT FAILED @@@"
