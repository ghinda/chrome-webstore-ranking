import json
from datetime import datetime
from celery.utils.log import get_task_logger

import requests

from cwr.app import db, celery
from cwr.models import Extension, ExtensionRank, STATUS_READY, STATUS_WIP, ExtensionQuery

logger = get_task_logger(__name__)

s = requests.Session()
s.headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Accept': '*/*',
    'Referer': 'https://chrome.google.com/',
    'Authority': 'chrome.google.com',
})

BASE_URL = 'https://chrome.google.com/webstore/'
LIST_URL = BASE_URL + "ajax/item"


@celery.task()
def search():
    """ Find a free query and fetch from CWS """

    cext = None
    q = None
    for ext in Extension.query.order_by(Extension.updated_datetime).all():
        if q:
            break

        # oldest first
        queries = ExtensionQuery.query.filter_by(extension_id=ext.id).order_by(ExtensionQuery.updated_datetime).all()

        for query in queries:
            if query.status == STATUS_READY:
                q = query
                cext = ext
                query.status = STATUS_WIP
                db.session.add(query)
                db.session.commit()
                break

    if not q:
        return 0

    params = {
        'hl': q.hl,
        'gl': q.gl,
        'pv': '20141016',
        'mce': 'rlb,svp,atf,c3d,ncr,ctm,ac,hot,euf,fcf',
        'count': 100,
        'category': q.category,
        'searchTerm': q.search_term,
        'sortBy': 0,
        'container': 'CHROME',
        '_reqid': 172075,
        'rt': 'j'
    }

    logger.info("Fetching for %s" % q.extension_id)

    r = s.post(LIST_URL, params=params)
    # remove the first few chars then try to decode
    content = r.content[5:]

    # some weird stuff with empty fields - replace them with zeros
    while ',,' in content:
        content = content.replace(',,', ',0 ,')

    data = json.loads(content)
    ext_list = data[0][1][1]
    now = datetime.utcnow()
    for i, e in enumerate(ext_list):
        ext_id = e[0]
        if ext_id == q.extension_id:
            rank = ExtensionRank()
            rank.extension_id = query.extension_id
            rank.extension_query_id = query.id
            rank.created_datetime = now
            rank.position = i
            db.session.add(rank)
            break

    query.status = STATUS_READY
    query.updated_datetime = now
    db.session.add(query)

    logger.info("Updating %s %s" % (cext.id, now))
    cext.updated_datetime = now
    db.session.add(cext)

    db.session.commit()

    return 1


if __name__ == '__main__':
    search()

