import os
import ast
import time
from typing import Literal, Optional, Union, Any, Dict
import streamlit as st
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _st_session_browser_storage = components.declare_component(

        "st_session_browser_storage",

        url="http://localhost:3001",
    )
else:

    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _st_session_browser_storage = components.declare_component(
        "st_session_browser_storage", path=build_dir)


class SessionStorage:
    """
    Component to help manager sessionBrowser storage for streamlit apps
    """

    def __init__(self, key="storage_init", pause=1.5):

        self.storedKey = key
        if key not in st.session_state:
            self.storedItems: Dict[str, Any] = _st_session_browser_storage(
                method="getAll", key=key, default={})
        else:
            self.storedItems: Dict[str, Any] = st.session_state[key]

            st.session_state[key] = self.storedItems
        if pause != None:
            time.sleep(pause)

    def setItem(self, itemKey: str = None, itemValue: Union[str, int, float, bool] = None, key: str = "set", default=None):
        """
        Set individual items to sessionBrowser storage with a given name (itemKey) and value (itemValue)

        Args:
            itemKey: Name of the item to set
            itemValue: The value to save. Can be string, int, float, bool, dict, json but will be stored as a string
        """

        if (itemKey is None or itemKey == "") or (itemValue is None or itemValue == ""):
            return

        _st_session_browser_storage(method="setItem", itemKey=itemKey,
                                    itemValue=itemValue, key=key, default=default)

        self.storedItems[itemKey] = itemValue

    def deleteItem(self, itemKey: str, key: str = "delete", default=None):
        """
        Delete individual item from sessionBrowser storage

        Args:
            itemKey: item key to delete from sessionBrowser storage
            key: unique identifier for the function/method in case you wish to execute it again somewhere else in the app.
        """

        if itemKey is None or itemKey == "":
            return

        _st_session_browser_storage(method="deleteItem", itemKey=itemKey, key=key, default=default)
        
        if isinstance(self.storedItems, dict):
            if itemKey not in self.storedItems:
                return
            else:
                self.storedItems.pop(itemKey)

    def eraseItem(self, itemKey: str, key: str = "eraseItem", default=None):
        """
        Erase item from sessionBrowser storage. deleteItem does not remove it from storage, merely changes its default value. This will do so.

        Args:
            itemKey: item key to remove from sessionBrowser storage 
            key: unique identifier for the function/method in case you wish to execute it again somewhere else in the app.
        """
        if itemKey is None or itemKey == "":
            return

        _st_session_browser_storage(method="eraseItem", itemKey=itemKey, key=key, default=default)

    def getItem(self, itemKey: str = None):
        """
        Get individual items stored in sessionBrowser storage.

        Args:
            itemKey: name of item to get from sessionBrowser storage
        """

        if itemKey not in self.storedItems:
            return
        return self.storedItems.get(itemKey)

    def getAll(self):
        """
        Get all items saved on sessionBrowser storage.

        Args:
            key: unique identifier for the function/method in case you wish to execute it again somewhere else in the app.
        """

        return self.storedItems

    def deleteAll(self, key: str = "delete_all"):
        """
        Delete all items you saved on sessionBrowser storage

        Args:
            key: unique identifier for the function/method in case you wish to execute it again somewhere else in the app.
        """

        _st_session_browser_storage(method="deleteAll", key=key)
        if (isinstance(self.storedItems, dict)):
            self.storedItems.clear()
