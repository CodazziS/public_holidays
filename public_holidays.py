from openerp.osv import fields, osv
from datetime import date, timedelta
import datetime
from work_calendar import calendars_factory
from workalendar.europe import France, FranceAlsaceMoselle


class public_holidays_holidays(osv.osv):
    _name = 'public.holidays.holidays'
    _description = 'Get days'

    def get_range(self, cr, uid, date_start, date_end, user=None, country='FR'):

        calendars = calendars_factory.get_instance()
        calendars.register(France, 'France', 'FR')
        calendars.register(FranceAlsaceMoselle, 'France Alsace/Moselle', 'FA')

        current_year = date_start.year
        last_year = date_end.year
        days = None

        while current_year <= last_year:
            current_days = calendars[country].holidays_set(current_year)

            print "DAYS = " + str(days)
            if days is None:
                days = current_days
            else:
                days = days.union(current_days)
            current_year += 1

        print "FINAL DAYS = " + str(days)

        fixed_days = self.pool.get('public.holidays.days')\
            .search(cr, uid,
                    [('date', '>', date_start), ('date', '<', date_end)])
        # @TODO : Concat fixed days with regulars days

        """
        print "START LOOP"

        for day in days:
            print day
            if day is datetime.date(2014, 7, 14):
                print "DAY HERE"


        print "END LOOP"
        print "DAYS"
        print days

        print "FIXED DAYS"
        print fixed_days
        """
        return days

    def is_holiday(self, cr, uid, date):
        days = self.get_range(cr, uid, date, date)

        if date in days:
            return True
        return False


class holidays_days(osv.osv):
    _name = 'public.holidays.days'
    _description = 'Store holidays days'

    #cr.execute()
    #self.pool.get('nom_De_Classe').search(cr, uid, [('date_start', '>', 'XXX'), ('date_end', '<', 'XXX')])

    _columns = {
        'date': fields.date('Date'),
        'holiday': fields.boolean('Holiday'),
        'company_id': fields.many2one(
            'res.company',
            'holidays_days',
            'company',
            required="true"),
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
        'holidays_days': fields.one2many(
            'public.holidays.days',
            'company_id',
            'Holidays days',
            required="true"),
    }