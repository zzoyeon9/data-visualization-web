#-*- coding:utf-8 -*-

"""Metadata
"""

__all__ = [
    "Metadata",
]

#
# Imports Modules
#
import base64
import os
import json
import sqlite3
from filelock import (
    FileLock,
    Timeout as LockTimeout,
)
from pathlib import Path
from modules.exceptions import *
from modules.types import *

#
# Paths
#
__curpath__ = os.path.dirname(os.path.abspath(__file__))
__metadata__ = os.path.join(__curpath__, "metadata")
__metalock__ = os.path.join(__curpath__, "metadata.lock")

#
# Objects
#
class Metadata(Object):
    """Metadata Object
    """

    # Session Timeout
    __timeout__ = 60

    def select(self, section: String, key: String) -> DefaultDict:
        """Selects the metadata.

        Parameters
        ----------
        section: String: Section info

        key: String: Search key

        Returns
        -------
        :Dict :조회결과

        """

        try:
            lock = FileLock(metalock(), timeout=self.__timeout__)
        except OSError:
            message = "Unable to access metadata"
            raise MetadataAccessError(message)
        else:
            sqls = tuple([
"""
CREATE TABLE IF NOT EXISTS {TBLNAME} (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
""", # If table doesn't exists, creates
"""
SELECT 
    * 
FROM 
    {TBLNAME} 
WHERE key='{KEY}';
""", # Query Infomation
            ])
            try:
                lock.acquire()
                result = dict()
                with sqlite3.connect(metadata()) as conn:
                    cursor = conn.cursor()
                    for id, sql in enumerate(sqls):
                        if id == 0:
                            q = sql.format(TBLNAME=section)
                            cursor.execute(q)
                            conn.commit()
                        elif id == 1:
                            q = sql.format(TBLNAME=section, KEY=key)
                            cursor.execute(q)
                            raws = cursor.fetchall()
                            if len(raws):
                                json_object = decode(raws[0][1])
                                result.update(json_object)
                        else:
                            continue
            except LockTimeout:
                message = "Because of locktimeout, unable to access metadata."
                raise MetadataAccessError(message)
            finally:
                try:
                    lock.release()
                except:
                    pass
        return result 

    def update(self, section: String, key: String, value: String):
        """Updates the metadata.

        Parameters
        ----------
        section: String: Section info

        key: String: Search key

        value: String: Result value

        """

        try:
            lock = FileLock(metalock(), timeout=self.__timeout__)
        except OSError:
            message = "Unable to access metadata"
            raise MetadataAccessError(message)
        else:
            sqls = tuple([
"""
CREATE TABLE IF NOT EXISTS {TBLNAME} (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
""", # If table doesn't exists, creates
"""
SELECT 
    COUNT(*) 
FROM 
    {TBLNAME} 
WHERE key='{KEY}';
""", # Checks having key or not in the table.
"""
UPDATE {TBLNAME} 
SET VALUE='{VALUE}'
WHERE KEY='{KEY}';
""",
"""
INSERT INTO {TBLNAME}
VALUES(
    '{KEY}',
    '{VALUE}'
);
""",
            ])
            try:
                lock.acquire()
                with sqlite3.connect(metadata()) as conn:
                    has_key = False
                    cursor = conn.cursor()
                    for id, sql in enumerate(sqls):
                        if id == 0:
                            q = sql.format(TBLNAME=section)
                            cursor.execute(q)
                            conn.commit()
                        elif id == 1:
                            q = sql.format(TBLNAME=section, KEY=key)
                            cursor.execute(q)
                            raws = cursor.fetchall()
                            count = raws[0][0]
                            if count:
                                has_key = True
                        elif id == 2 and has_key:
                            # The key exists in the table.
                            q = sql.format(TBLNAME=section, KEY=key, VALUE=encode(value))
                            cursor.execute(q)
                            conn.commit()
                        elif id == 3 and (not has_key):
                            # The key doesn't exists in the table.
                            q = sql.format(TBLNAME=section, KEY=key, VALUE=encode(value))
                            cursor.execute(q)
                            conn.commit()
                        else:
                            continue
            except LockTimeout:
                message = "Because of locktimeout, unable to access metadata."
                raise MetadataAccessError(message)
            finally:
                try:
                    lock.release()
                except:
                    pass

    def delete(self, section: String, key: String):
        """Deletes the metadata.

        Parameters
        ----------
        section: String: Section info

        key: String: Search key

        """

        try:
            lock = FileLock(metalock(), timeout=self.__timeout__)
        except OSError:
            message = "Unable to access metadata"
            raise MetadataAccessError(message)
        else:
            sqls = tuple([
"""
CREATE TABLE IF NOT EXISTS {TBLNAME} (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
)
""".format(
    TBLNAME=section, 
), # If table doesn't exists, creates
"""
SELECT 
    COUNT(*) 
FROM 
    {TBLNAME} 
WHERE key='{KEY}';
""".format(
    TBLNAME=section,
    KEY=key, 
), # Checks having key or not in the table.
"""
DELETE FROM {TBLNAME}
WHERE key='{KEY}';
"""
            ])
            try:
                lock.acquire()
                with sqlite3.connect(metadata()) as conn:
                    has_key = False
                    for id, sql in enumerate(sqls):
                        cursor = conn.cursor()
                        cursor.execute(sql)
                        if id == 0:
                            q = sql.format(TBLNAME=section)
                            cursor.execute(q)
                            conn.commit()
                        elif id == 1:
                            q = sql.format(TBLNAME=section, KEY=key)
                            cursor.execute(q)
                            raws = cursor.fetchall()
                            count = raws[0][0]
                            if count:
                                has_key = True
                        elif id == 2 and (has_key):
                            # The key exists in the table.
                            q = sql.format(TBLNAME=section, KEY=key)
                            cursor.execute(q)
                            conn.commit()
                        else:
                            continue
            except LockTimeout:
                message = "Because of locktimeout, unable to access metadata."
                raise MetadataAccessError(message)
            finally:
                try:
                    lock.release()
                except:
                    pass

# Common Functions
def metadata() -> Path:
    """Returns fullpath of metadata.

    Returns
    -------
    :Path :Fullpath of metadata

    """

    return __metadata__

def metalock() -> Path:
    """Returns fullpath of the lock of the metadata.

    Returns
    -------
    :Path :Fullpath of the lock of the metadata

    """

    return __metalock__

def encode(json_object: DefaultDict) -> String:
    """Encodes the json object to the string.

    Parameters
    ----------
    json_object: Dict: JSON Object

    Returns
    -------
    :String :Encoded string

    """

    json_src = json.dumps(json_object)
    value = base64.b64encode(json_src.encode()).decode()
    return value

def decode(value: String) -> DefaultDict:
    """Decodes the string to the json object.

    Parameters
    ----------
    value: String: Encoded string

    Returns
    -------
    :Dict :Decoded JSON object

    """

    json_src = base64.b64decode(value.encode()).decode()
    json_object = json.loads(json_src)
    return json_object
