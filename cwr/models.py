from cwr.app import db

STATUS_READY = 0
STATUS_WIP = 1

LOCALES = [
    'en-US',
    #'en-GB',
    #'ru-RU',
    'fr-FR',
    #'fr-CA',
    'de-DE',
    #'es-MX',
    'es-ES',
]

COUNTRIES = [
    'US'
]


class Extension(db.Model):
    id = db.Column(db.String(40), primary_key=True)
    avg_rank = db.Column(db.Float())

    created_datetime = db.Column(db.DateTime(), index=True)
    updated_datetime = db.Column(db.DateTime(), index=True)

    queries = db.relationship('ExtensionQuery', backref="extension_query")


class ExtensionQuery(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    extension_id = db.Column(db.String(40), db.ForeignKey("extension.id"))

    category = db.Column(db.String(100), index=True)
    search_term = db.Column(db.String(200), index=True)
    hl = db.Column(db.String(10), index=True)
    gl = db.Column(db.String(2), index=True)

    created_datetime = db.Column(db.DateTime(), index=True)
    updated_datetime = db.Column(db.DateTime(), index=True)

    status = db.Column(db.Integer(), default=0, index=True)  # use for locking

    ranks = db.relationship('ExtensionRank', backref="extension_Rank")


class ExtensionRank(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    extension_id = db.Column(db.String(40), db.ForeignKey("extension.id"))
    extension_query_id = db.Column(db.Integer(), db.ForeignKey("extension_query.id"))

    position = db.Column(db.Integer(), index=True)

    created_datetime = db.Column(db.DateTime(), index=True)

