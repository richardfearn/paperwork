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
logger = logging.getLogger("paperwork")
logger.setLevel(logging.INFO)


class Client:

    def __init__(self, config, username):

        self.config = config

        self.oauth = OAuth1(self.config.consumer_key(),
                            client_secret=self.config.consumer_secret(),
                            resource_owner_key=self.config.token(username),
                            resource_owner_secret=self.config.token_secret(username))

        self.request_timeout = 5
        self.max_retries = 10

    def list_folders(self):
        data = self.do_request(LIST_FOLDERS)
        data = [o for o in data if o["type"] == "folder"]
        data = list(map(Folder.from_json, data))
        return data

    def list_bookmarks(self, folder, limit=500):
        data = self.do_request(LIST_BOOKMARKS, {
            "folder_id": folder.id,
            "limit": limit,
        })
        data = [o for o in data if o["type"] == "bookmark"]
        data = list(map(Bookmark.from_json, data))
        return data

    def move_bookmark(self, bookmark, folder):

        data = self.do_request(MOVE_BOOKMARK, {
            "bookmark_id": bookmark.id,
            "folder_id": folder.id,
        })
        data = data[0]
        data = Bookmark.from_json(data)
        return data

    def delete_folder(self, folder):
        return self.do_request(DELETE_FOLDER, {
            "folder_id": folder.id,
        })

    def add_folder(self, folder):
        data = self.do_request(ADD_FOLDER, {
            "title": folder.title,
        })
        data = data[0]
        data = Folder.from_json(data)
        return data

    def add_bookmark(self, bookmark, folder=None):
        params = {
            "url": bookmark.url,
        }
        if bookmark.title is not None:
            params["title"] = bookmark.title
        if bookmark.description is not None:
            params["description"] = bookmark.description
        if folder is not None:
            params["folder_id"] = folder.id
        data = self.do_request(ADD_BOOKMARK, params)
        data = data[0]
        data = Bookmark.from_json(data)
        return data

    def delete_bookmark(self, bookmark):
        return self.do_request(DELETE_BOOKMARK, {
            "bookmark_id": bookmark.id,
        })

    def do_request(self, url, params=None):
        full_url = API_URL_PREFIX + url
        logger.debug("Request URL: %s", full_url)
        logger.debug("Request parameters: %s", params)
        data = None
        successful = False
        for attempt in range(1, self.max_retries+1):
            try:
                logger.debug("Attempt %d", attempt)
                logger.debug("Making request")

                response = requests.post(url=full_url, data=params, auth=self.oauth, timeout=self.request_timeout)
                logger.debug("Response: %s", response)
                logger.debug("Response status: %d" % response.status_code)
                data = response.text
                # print(data)
                if response.status_code == 200:
                    data = json.loads(data)
                    successful = True
                else:
                    logger.warning(ATTEMPT_FAILED_MARKER)
            except requests.exceptions.RequestException:
                logger.warning(ATTEMPT_FAILED_MARKER, exc_info=True)
            if successful:
                break
        logger.debug("Final result: %s", successful)
        if not successful:
            raise Exception("Failed after %d attempts" % self.max_retries)
        return data


ATTEMPT_FAILED_MARKER = "@@@ ATTEMPT FAILED @@@"
