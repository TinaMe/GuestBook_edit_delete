#!/usr/bin/env python
import os
import jinja2
import webapp2

from models import GuestBook

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True) #da ne mores kr nekaj vpisat v okvircek


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("domov.html")


class RezultatHandler(BaseHandler):
    def post(self):
        ime = self.request.get("input_ime")
        email = self.request.get("input_email")
        besedilo = self.request.get("input_sporocilo")

        if not ime:
            ime = "Uporabnik zeli ostati neimenovan."

        uporabnik = GuestBook(imepriimek=ime, enaslov=email, sporocilo=besedilo)
        uporabnik.put()

        params={"imegosta": ime, "emailgosta": email, "sporocilogosta": besedilo}

        return self.render_template("rezultat.html", params)


class GuestBookHandler(BaseHandler):
    def get(self):
        seznam = GuestBook.query(GuestBook.izbrisano == False).fetch()
        params = {"seznam": seznam}
        return self.render_template("guestbook.html", params=params)


class PosameznoSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = GuestBook.get_by_id(int(sporocilo_id))
        params = {"posamezno_sporocilo": sporocilo}
        return self.render_template("posamezno_sporocilo.html", params=params)


class UrediHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = GuestBook.get_by_id(int(sporocilo_id))
        params = {"posamezno_sporocilo": sporocilo}
        return self.render_template("uredi_sporocilo.html", params=params)

    def post(self, sporocilo_id):
        sporocilo = GuestBook.get_by_id(int(sporocilo_id))
        sporocilo.sporocilo = self.request.get("nov_tekst")
        sporocilo.put()
        self.redirect_to("seznam_sporocil")


class IzbrisiHandler(BaseHandler):
    def get(self, sporocilo_id):
            sporocilo = GuestBook.get_by_id(int(sporocilo_id))
            params = {"posamezno_sporocilo": sporocilo}
            return self.render_template("izbrisi_sporocilo.html", params=params)

    def post(self, sporocilo_id):
            sporocilo = GuestBook.get_by_id(int(sporocilo_id))
            sporocilo.izbrisano = True
            sporocilo.put()
            self.redirect_to("seznam_sporocil")



app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/rezultat', RezultatHandler),
    webapp2.Route('/seznam', GuestBookHandler, name="seznam_sporocil"),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>', PosameznoSporociloHandler),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>/edit', UrediHandler),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>/delete', IzbrisiHandler),
], debug=True)

