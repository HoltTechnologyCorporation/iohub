from pymongo import MongoClient

from project.settings import MONGODB


def connect_db():
    conn = MongoClient(**MONGODB['connection'])
    db = conn[MONGODB['database']]

    # ping
    db.ping.create_index([
        ('data.session_id', 1),
        ('_id', 1),
    ])
    db.ping.create_index([
        ('date', 1),
        ('data.session_id', 1),
    ])

    # session
    db.session.create_index([
            ('session_id', 1),
        ],
        unique=True
    )
    db.session.create_index([
        ('date', 1),
        ('session_id', 1),
    ])

    return db


db = connect_db()
