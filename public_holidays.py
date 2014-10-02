from openerp.osv import fields, osv
from datetime import date, timedelta


class easter_day(date):
    def __new__(cls, year=None):
        
        if year is None:
            year = date.today().year

        a = year // 100
        b = year % 100
        c = (3 * (a + 25)) // 4
        d = (3 * (a + 25)) % 4
        e = (8 * (a + 11)) // 25
        f = (5 * a + b) % 19
        g = (19 * f + c - e) % 30
        h = (f + 11 * g) // 319
        j = (60 * (5 - d) + b) // 4
        k = (60 * (5 - d) + b) % 4
        m = (2 * j - k - g + h) % 7
        n = (g - h + m + 114) // 31
        p = (g - h + m + 114) % 31

        return super(easter_day, cls).__new__(cls, year, n, p + 1)

    def __add__(self, other):
        if type(other) is int:
            return self + timedelta(other)
        else:
            return super(easter_day, self).__add__(other)
     
    def __sub__(self, other):
        if type(other) is int:
            return self - timedelta(other)
        else:
            return super(easter_day, self).__sub__(other)


class french_holidays(object):

    def __init__(self, year=None, country=None):

        if year is None:
            year = date.today().year

        self._holidays = [

            date(year, 1, 1),       # Jour de l'an
            easter_day(year) - 2,   # Vendredi Saint (Alsace-Moselle)
            easter_day(year),       # Dimanche de P?ques
            easter_day(year) + 1,   # Lundi de P?ques
            date(year, 5, 1),       # F?te du travail
            date(year, 5, 8),       # Victoire 1945
            easter_day(year) + 39,  # Jeudi de l'Ascension
            easter_day(year) + 49,  # Dimanche de Pentecote
            easter_day(year) + 50,  # Lundi de Pentecote
            date(year, 7, 14),      # F?te Nationale
            date(year, 8, 15),      # Assomption
            date(year, 11, 1),      # Toussaint
            date(year, 11, 11),     # Armistice de 1918
            date(year, 12, 25),     # No?l
            date(year, 12, 26),     # Saint Etienne (Alsace-Moselle)

        ]

    def to_list(self):
        return self._holidays


class public_holidays_holidays(osv.osv):
    _name = 'public.holidays.holidays'
    _description = 'Get days'

    def get_range(self, date_start, date_stop):
        res = {}
        # @TODO when french_holidays get all params 
        x = french_holidays(year=date_start.year)
        return x.to_list()


class holidays_days(osv.osv):
    _name = 'public_holidays.holidays_days'
    _description = 'Store holidays days'

    _columns = {
        'date': fields.date('Date'),
        'holiday': fields.boolean('Holiday'),
        #m2o user_id ...
    }


class holidays_config_user(osv.osv):
    _inherit = 'res.users'

    _columns = {
        'monday': fields.boolean('Monday'),
        'tuesday': fields.boolean('Tuesday'),
        'wednesday': fields.boolean('Wednesday'),
        'thuesday': fields.boolean('thuesday'),
        'friday': fields.boolean('Friday'),
        'saturday': fields.boolean('Saturday'),
        'sunday': fields.boolean('Sunday'),
        'country': fields.char('Country'),
    }


class holidays_config_conpany(osv.osv):
    _inherit = 'res.company'

    _columns = {
        'monday': fields.boolean('Monday'),
        'tuesday': fields.boolean('Tuesday'),
        'wednesday': fields.boolean('Wednesday'),
        'thuesday': fields.boolean('thuesday'),
        'friday': fields.boolean('Friday'),
        'saturday': fields.boolean('Saturday'),
        'sunday': fields.boolean('Sunday'),
        'country': fields.char('Country'),
    }