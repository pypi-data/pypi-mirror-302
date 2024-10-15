# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         __init__.py.py
# Description:  
# Author:       xaoyaoo
# Date:         2023/10/14
# -------------------------------------------------------------------------------
__version__ = "3.1.36"

import os, json

try:
    WX_OFFS_PATH = os.path.join(os.path.dirname(__file__), "WX_OFFS.json")
    with open(WX_OFFS_PATH, "r", encoding="utf-8") as f:
        WX_OFFS = json.load(f)
except:
    WX_OFFS = {}
    WX_OFFS_PATH = None

from .wx_core import BiasAddr, get_wx_info, get_wx_db, batch_decrypt, decrypt, get_core_db
from .wx_core import merge_db, decrypt_merge, merge_real_time_db, all_merge_real_time_db


__all__ = ["BiasAddr", "get_wx_info", "get_wx_db", "batch_decrypt", "decrypt", "get_core_db",
           "merge_db", "decrypt_merge", "merge_real_time_db", "all_merge_real_time_db", "WX_OFFS", "WX_OFFS_PATH",
           "__version__"]
