import json
from time import mktime
import urllib
from datetime import datetime

from flask import render_template, request, redirect, url_for

import requests
from lxml import html

from cwr.app import app, db
from cwr.models import Extension, ExtensionQuery, LOCALES, COUNTRIES


def _new_queries(eid, search_term, category):
    now = datetime.utcnow()

    for gl in COUNTRIES:
        for hl in LOCALES:
            # new query
            query = ExtensionQuery()
            query.extension_id = eid
            query.search_term = search_term
            query.category = category
            query.hl = hl
            query.gl = gl

            query.updated_datetime = now
            query.created_datetime = now
            db.session.add(query)
    db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def index():
    eid = request.args.get('eid', request.form.get('eid'))
    search_term = request.args.get('search_term', request.form.get('search_term'))
    category = request.args.get('category', request.form.get('category'))
    created = request.args.get('created', 0)
        

    if request.method == 'POST':
        if eid and search_term and category:
            now = datetime.utcnow()

            # new extension
            ext = Extension.query.get(eid)
            if not ext:
                ext = Extension()
                ext.id = eid
                ext.created_datetime = now
                db.session.add(ext)

                _new_queries(eid, search_term, category)
                created = 1
            else:  # existing extension
                query = ExtensionQuery.query. \
                    filter_by(extension_id=eid). \
                    filter_by(search_term=search_term). \
                    filter_by(category=category).first()

                # no such query - create one
                if not query:
                    _new_queries(eid, search_term, category)
                    created = 1

            return redirect(url_for('index') + "?" + urllib.urlencode({
                'eid': eid,
                'search_term': search_term,
                'category': category,
                'created': created
            }))
        else:
            return render_template('index.html', error="All terms are required", data={})


    # get the extension icon and name,
    # by scraping the extension page.
    # TODO should be probably done better,
    # caching the title and icon path in the db.
    
    extTitle = ''
    extIconUrl = ''
        
    if eid:
        
        cwrUrl = 'https://chrome.google.com/webstore/detail/'
        page = requests.get(cwrUrl + eid);
        
        tree = html.fromstring(page.text)
        extTitle = tree.xpath('//h1[@class="g-f-x"]/text()')[0]
        extIconUrl = tree.xpath('//img[@class="g-f-t"]/@src')[0]
        

    ext = None
    data = []
    if eid:

        ext = Extension.query.get(eid)
        if ext:
            for query in ext.queries:
                qdata = {
                    'key': json.dumps({
                        'hl': query.hl,
                        'gl': query.gl,
                        'search_term': query.search_term,
                        'category': query.category,
                    }),
                    'values': []
                }

                for rank in query.ranks:
                    qdata['values'].append(
                        [rank.created_datetime.strftime('%Y-%m-%dT%H:%M:%S'), rank.position]
                    )
                data.append(qdata)

    return render_template('index.html', data={
        'eid': eid or '',
        'search_term': search_term or '',
        'category': category or '',
        'chart_data': json.dumps(data),
        'title': extTitle,
        'icon': extIconUrl
    })