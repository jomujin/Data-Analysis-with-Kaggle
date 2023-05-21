import re
import json
import datetime
import requests
import pandas as pd
import numpy as np
import warnings
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import (
    List
)
warnings.filterwarnings('ignore')


class RequestsTimeOutError(Exception):
    pass

class RequestsConnectionError(Exception):
    pass

class RequestsHTTPError(Exception):
    pass

class RequestsExcptionError(Exception):
    pass

class RequestsNotExistedError(Exception):
    pass

class SoupNotExistedError(Exception):
    pass

class ResultByTagsNotExistedError(Exception):
    pass


@dataclass
class Nba:
    def __init__(
        self,
        idx
    ):
        self.idx: int = idx

    def _get_url(
        self,
        page_typ: str
    ):
        self.url = f"https://www.espn.com/nba/{page_typ}/_/gameId/{self.idx}"

    def _get_req(self):
        try:
            self.req = requests.get(self.game_url)

        except requests.exceptions.Timeout as errd:
            RequestsTimeOutError("Timeout Error : ", errd)

        except requests.exceptions.ConnectionError as errc:
            RequestsConnectionError("Error Connecting : ", errc)
            
        except requests.exceptions.HTTPError as errb:
            RequestsHTTPError("Http Error : ", errb)

        # Any Error except upper exception
        except requests.exceptions.RequestException as erra:
            RequestsExcptionError("AnyException : ", erra)

    def _get_html(self):
        if self.req:
            html = self.req.text
            self.soup = BeautifulSoup(html, 'html.parser')
        else:
            RequestsNotExistedError("Not Existed Requests")

    def _get_find_by_tag(
        self,
        tag: str,
        type_var: str
    ):
        if not tag:
            raise ValueError("Missing tag")

        if not isinstance(tag, str):
            raise TypeError("Tag should be a string")

        if not type_var:
            raise ValueError("Missing type")

        if not isinstance(type_var, str):
            raise TypeError("Type should be a string")

        if not self.soup:
            SoupNotExistedError("Not Existed Requests")

        self.script_tags = self.soup.find_all(
            tag=tag,
            type=type_var
        )

    def _get_json_by_compile(
        self,
        compile: str,
        flags: str = re.DOTALL
    ):
        if not compile:
            raise ValueError("Missing Compile")

        if not isinstance(compile, str):
            raise TypeError("Compile should be a string")

        if not flags:
            raise ValueError("Missing Flags")

        if not isinstance(flags, str):
            raise TypeError("Flags should be a string")

        if not self.script_tags:
            ResultByTagsNotExistedError("Not Existed Result By Tags")

        self.jsons: List[str] = []
        pattern = re.compile(
            compile, 
            flags
        )
        
        for script_tag in self.script_tags:
            if script_tag.string:
                script_content = script_tag.string
                match = pattern.search(script_content)

                if match:
                    json_str = match.group(1)
                    json_data = json.loads(json_str)
                    self.jsons.append(json_data)


class NbaBoxScore(Nba):
    def __init__(
        self,
        idx
    ):
        super().__init__(self, idx)

    def _get_url(self, page_typ: str):
        return super()._get_url(page_typ)

    def _get_req(self):
        return super()._get_req()

    def _get_html(self):
        return super()._get_html()

    def _get_find_by_tag(self, tag: str, type_var: str):
        return super()._get_find_by_tag(tag, type_var)

    def _get_json_by_compile(self, compile: str, flags: str = re.DOTALL):
        return super()._get_json_by_compile(compile, flags)

    self._get_url(
        page_typ='boxscore'
    )
    self._get_find_by_tag(
        tag='script',
        type_var='text/javascript'
    )