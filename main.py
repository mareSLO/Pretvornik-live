#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        self.render_template("hello.html")


class PretvoriHandler(BaseHandler):
    def post(self):
        pretvori1 = self.request.get("enota1")
        pretvori2 = self.request.get("enota2")
        pretvori1 = pretvori1.replace(",", ".")
        pretvori2 = pretvori2.replace(",", ".")

        if pretvori1 != "":
            rezultat1 = float(pretvori1) * 0.74
            rezultat1 = pretvori1 + " konjev = " + str(rezultat1) + " kilovatov"
            rezultat1 = rezultat1.replace(".", ",")
        else:
            rezultat1 = ""

        if pretvori2 != "":
            rezultat2 = float(pretvori2) * 1.341
            rezultat2 = pretvori2 + " kilovatov = " + str(rezultat2) + " konjev"
            rezultat2 = rezultat2.replace(".", ",")
        else:
            rezultat2 = ""

        params = {"pretvori1": pretvori1, "pretvori2": pretvori2, "rezultat1": rezultat1, "rezultat2": rezultat2}
        self.render_template("pretvorienoto.html", params)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/pretvorienoto', PretvoriHandler)
], debug=True)
