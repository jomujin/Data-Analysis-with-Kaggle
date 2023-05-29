import re
import json
import datetime
import requests
import pandas as pd
import numpy as np
import warnings
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from dataclasses import dataclass
from typing import (
    Any,
    List
)
from cond import (
    BOX_SCORE_COLS,
    HEADER_COLS,
    PLAYED_STATS_RENAME_COLS
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
class ESPN_NBA:
    def __init__(
        self
    ):
        self.session = requests.Session()
        adapter = HTTPAdapter(pool_connections=100, pool_maxsize=100)
        self.session.keep_alive = True
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def get_url(
        self,
        idx: str,
        page_typ: str
    ):
        if not idx:
            raise ValueError("Missing idx")
        
        if not isinstance(idx, str):
            raise TypeError("Idx should be a string")

        if not page_typ:
            raise ValueError("Missing page_typ")

        if not isinstance(page_typ, str):
            raise TypeError("Tag should be a string")

        self.idx = idx
        self.url: str = f"https://www.espn.com/nba/{page_typ}/_/gameId/{self.idx}"

    def _get_req(self):
        try:
            self.req = self.session.get(self.url, timeout=5)

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

    def _get_find_by_name(
        self,
        name: str,
        type_var: str
    ):
        if not name:
            raise ValueError("Missing Name")

        if not isinstance(name, str):
            raise TypeError("Name should be a string")

        if not type_var:
            raise ValueError("Missing type")

        if not isinstance(type_var, str):
            raise TypeError("Type should be a string")

        if not self.soup:
            SoupNotExistedError("Not Existed Requests")

        self.scripts = self.soup.find_all(
            name=name,
            type=type_var
        )

    def _get_json_by_compile(
        self,
        compile,
        flags = re.DOTALL
    ):
        if not compile:
            raise ValueError("Missing Compile")

        if not flags:
            raise ValueError("Missing Flags")

        if not self.scripts:
            ResultByTagsNotExistedError("Not Existed Result By Tags")

        self.jsons: List[Any] = []
        pattern = re.compile(
            compile, 
            flags
        )
        
        for script in self.scripts:
            if script.string:
                script_content = script.string
                match = pattern.search(script_content)

                if match:
                    json_str = match.group(1)
                    json_data = json.loads(json_str)
                    self.jsons.append(json_data)

class ESPN_NBA_Box_Score(ESPN_NBA):
    def __init__(
        self
    ):
        super().__init__()

    def get_url(self, idx: str, page_typ: str):
        return super().get_url(idx, page_typ)

    def _get_req(self):
        return super()._get_req()

    def _get_html(self):
        return super()._get_html()

    def _get_find_by_tag(self, tag: str, type_var: str):
        return super()._get_find_by_name(tag, type_var)

    def _get_json_by_compile(self, compile: str, flags = re.DOTALL):
        return super()._get_json_by_compile(compile, flags)

    def _convert_to_dataframe(self):
        if not self.jsons:
            raise ValueError("Not Existed Jsons")

        if not isinstance(self.jsons, list):
            raise TypeError("Name should be a list")

        if not len(self.jsons):
            raise ValueError("리스트 개수가 모자르다")
        
        if 'page' not in self.jsons[0].keys():
            raise ValueError("page key가 없다")

        # team_df = pd.DataFrame(columns=tt_cols)
        # game_df = pd.DataFrame(columns=gt_cols)
        self.box_score_df: pd.DataFrame = pd.DataFrame(columns=BOX_SCORE_COLS)

        page = self.jsons[0]['page']
        gm_strp = page['content']['gamepackage']['gmStrp']
        g_id = gm_strp['gid']
        dt = gm_strp['dt']
        season_typ = gm_strp['seasonType']
        status_state = gm_strp['statusState']
        tms = gm_strp['tms']

        for tm in tms:
            if tm['isHome'] == True:
                home = tm['abbrev']
                score_home = int(tm['score'])
                score_home_q1 = int(tm['linescores'][0]['displayValue'])
                score_home_q2 = int(tm['linescores'][1]['displayValue'])
                score_home_q3 = int(tm['linescores'][2]['displayValue'])
                score_home_q4 = int(tm['linescores'][3]['displayValue'])
            else:
                away = tm['abbrev']
                score_away = int(tm['score'])
                score_away_q1 = int(tm['linescores'][0]['displayValue'])
                score_away_q2 = int(tm['linescores'][1]['displayValue'])
                score_away_q3 = int(tm['linescores'][2]['displayValue'])
                score_away_q4 = int(tm['linescores'][3]['displayValue'])
            if ('winner' in tm.keys()) \
            and (tm['winner'] == True):
                winner = tm['abbrev']

        gm_info = page['content']['gamepackage']['gmInfo']
        attnd = gm_info['attnd']
        cpcty = gm_info['cpcty']
        loc = gm_info['loc']
        loc_city = gm_info['locAddr']['city']
        loc_state = gm_info['locAddr']['state']
        refs = gm_info['refs']
        ref_1 = refs[0]['dspNm']
        ref_2 = refs[1]['dspNm']
        ref_3 = refs[2]['dspNm']

        # Table Stats
        for team in page['content']['gamepackage']['bxscr']:
            team_info = team['tm']
            t_id = team_info['id']
            t_abbrev = team_info['abbrev']
            starter_stats = team['stats'][0]
            bench_stats = team['stats'][1]
            team_stats = team['stats'][2]
            table_column = bench_stats['lbls']
            table_column_desc = bench_stats['keys']
            cols = HEADER_COLS + table_column

            # Player Table Stats
            for idx, player in enumerate(starter_stats['athlts'] + bench_stats['athlts']):
                played_stats_df: pd.DataFrame = pd.DataFrame(columns=cols)
                not_played_stats_df: pd.DataFrame = pd.DataFrame(columns=BOX_SCORE_COLS)
                stats = [None] * 20
                p_info = player['athlt']
                p_id = p_info['id']
                p_nm = p_info['shrtNm']
                p_pos = p_info['pos']
                is_play = False
                is_total = False
                is_starter = False
                if idx < 5:
                    is_starter = True
                if (player['stats']) and (player['stats'][0].isalnum()):
                    is_play = True
                    stats = player['stats']

                values = [
                    g_id,
                    t_id,
                    t_abbrev,
                    is_total,
                    is_play,
                    is_starter,
                    p_id,
                    p_nm,
                    p_pos
                ] + stats

                if is_play:
                    series = pd.Series(values, index = played_stats_df.columns)
                    played_stats_df = played_stats_df.append(series, ignore_index=True)
                    
                    played_stats_df = played_stats_df.rename(columns=PLAYED_STATS_RENAME_COLS)
                    played_stats_df['fgm'] = int(played_stats_df['fg'].map(lambda x: str(x).split('-')[0]))
                    played_stats_df['fga'] = int(played_stats_df['fg'].map(lambda x: str(x).split('-')[1]))
                    played_stats_df['3ptm'] = int(played_stats_df['3pt'].map(lambda x: str(x).split('-')[0]))
                    played_stats_df['3pta'] = int(played_stats_df['3pt'].map(lambda x: str(x).split('-')[1]))
                    played_stats_df['ftm'] = int(played_stats_df['ft'].map(lambda x: str(x).split('-')[0]))
                    played_stats_df['fta'] = int(played_stats_df['ft'].map(lambda x: str(x).split('-')[1]))
                    played_stats_df['fgr'] = round((played_stats_df['fgm'] / played_stats_df['fga']) * 100, 2)
                    played_stats_df['3ptr'] = round((played_stats_df['3ptm'] / played_stats_df['3pta']) * 100, 2)
                    played_stats_df['ftr'] = round((played_stats_df['ftm'] / played_stats_df['fta']) * 100, 2)
                    played_stats_df = played_stats_df.drop([
                        'fg',
                        '3pt',
                        'ft'
                    ], axis=1)
                    stats_df = played_stats_df[BOX_SCORE_COLS]
                    self.box_score_df = pd.concat([
                        self.box_score_df,
                        stats_df
                    ])
                else:
                    series = pd.Series(values, index = not_played_stats_df.columns)
                    not_played_stats_df = not_played_stats_df.append(series, ignore_index=True)

                    self.box_score_df = pd.concat([
                        self.box_score_df,
                        not_played_stats_df
                    ])

            team_stats_df = pd.DataFrame(columns=cols)
            team_values = [
                g_id,
                t_id,
                t_abbrev,
                True, # is_total,
                None, # is_play,
                None, # is_starter
                None, # p_id,
                None, # p_nm,
                None # p_pos
            ] + team_stats['ttls']
            series = pd.Series(team_values, index = team_stats_df.columns)
            team_stats_df = team_stats_df.append(series, ignore_index=True)
            team_stats_df = team_stats_df.rename(columns=PLAYED_STATS_RENAME_COLS)
            team_stats_df['fgm'] = int(team_stats_df['fg'].map(lambda x: str(x).split('-')[0]))
            team_stats_df['fga'] = int(team_stats_df['fg'].map(lambda x: str(x).split('-')[1]))
            team_stats_df['3ptm'] = int(team_stats_df['3pt'].map(lambda x: str(x).split('-')[0]))
            team_stats_df['3pta'] = int(team_stats_df['3pt'].map(lambda x: str(x).split('-')[1]))
            team_stats_df['ftm'] = int(team_stats_df['ft'].map(lambda x: str(x).split('-')[0]))
            team_stats_df['fta'] = int(team_stats_df['ft'].map(lambda x: str(x).split('-')[1]))
            team_stats_df['fgr'] = round((team_stats_df['fgm'] / team_stats_df['fga']) * 100, 2)
            team_stats_df['3ptr'] = round((team_stats_df['3ptm'] / team_stats_df['3pta']) * 100, 2)
            team_stats_df['ftr'] = round((team_stats_df['ftm'] / team_stats_df['fta']) * 100, 2)
            team_stats_df = team_stats_df.drop([
                'fg',
                '3pt',
                'ft'
            ], axis=1)
            stats_df = team_stats_df[BOX_SCORE_COLS]
            self.box_score_df = pd.concat([
                self.box_score_df,
                stats_df
            ])

    def crawl_box_score(self, idx):
        self.get_url(
            idx,
            page_typ='boxscore'
        )
        self._get_req()
        if not self.req.ok:
            pass
        else:
            self._get_html()
            self._get_find_by_name(
                name='script',
                type_var='text/javascript'
            )
            self._get_json_by_compile(
                compile=r'window\[\'__espnfitt__\'\]\s*=\s*(\{.*\});',
                flags=re.DOTALL
            )
            self._convert_to_dataframe()