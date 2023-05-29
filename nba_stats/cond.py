from typing import (
    List,
    Dict
)


BOX_SCORE_COLS: List[str] = [
    'g_id',
    't_id',
    'tm_abbrev',
    'is_total',
    'is_played',
    'is_starter',
    'p_id',
    'p_nm',
    'p_pos',
    'min',
    'fgr',
    'fgm',
    'fga',
    '3ptr',
    '3ptm',
    '3pta',
    'ftr',
    'ftm',
    'fta',
    'oreb',
    'dreb',
    'reb',
    'ast',
    'stl',
    'blk',
    'to',
    'pf',
    '+/-',
    'pts'
]

HEADER_COLS: List[str] = [
    'g_id',
    't_id',
    'tm_abbrev',
    'is_total',
    'is_played',
    'is_starter',
    'p_id',
    'p_nm',
    'p_pos'
]

PLAYED_STATS_RENAME_COLS: Dict[str, str] ={
    'MIN': 'min',
    'FG': 'fg',
    '3PT': '3pt',
    'FT': 'ft',
    'OREB': 'oreb',
    'DREB': 'dreb',
    'REB': 'reb',
    'AST': 'ast',
    'STL': 'stl',
    'BLK': 'blk',
    'TO': 'to',
    'PF': 'pf',
    # '+/-': ,
    'PTS': 'pts',
}
