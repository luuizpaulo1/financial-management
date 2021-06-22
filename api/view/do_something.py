from flask.views import View
from flask import request, render_template


class DoSomethingView(View):
    methods = ['GET']

    def dispatch_request(self):
        if request.method == 'GET':
            return render_template('do_something.html')
