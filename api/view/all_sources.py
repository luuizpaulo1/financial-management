from flask.views import View
from flask import request, render_template
from api.model.source import SourceModel


class AllSourcesView(View):
    methods = ['GET']

    def dispatch_request(self):
        if request.method == 'GET':
            sources = SourceModel.query.filter_by(
                is_deleted=False
            ).all()
            return render_template('all_sources.html', sources=sources)
