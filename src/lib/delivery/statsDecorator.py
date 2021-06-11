from datetime import datetime
from src.lib.db.db import Db

STATS_LIST = [
    Db.COLUMN_GYRO_X,
    Db.COLUMN_GYRO_Y,
    Db.COLUMN_GYRO_Z,
    Db.COLUMN_ACC_X,
    Db.COLUMN_ACC_Y,
    Db.COLUMN_ACC_Z,
    Db.COLUMN_LIGHT_LEVEL,
]


def decorate(stat_groups, stat_type):
    decorated_stats = []

    if not stat_groups:
        return None

    for stat_group in stat_groups:
        group = {
            'type': stat_type,
            'when': stat_group['created_at'] or datetime.now(),
            'id': stat_group['id'],
            'attributes': get_attributes(stat_group)
        }

        decorated_stats.append(group)

    return decorated_stats


def get_attributes(stats):
    attributes = {}

    for name, stat in stats.items():
        if name in STATS_LIST:
            attributes[name] = stat

    return attributes
