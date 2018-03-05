from google.appengine.ext import ndb

class GuestBook(ndb.Model):         #ne pozabi importirati v main.py!
    imepriimek = ndb.StringProperty()
    enaslov = ndb.StringProperty()
    sporocilo = ndb.StringProperty()
    nastanek = ndb.DateTimeProperty(auto_now_add=True)
    izbrisano = ndb.BooleanProperty(default=False)

