from openerp.osv import fields, osv
from datetime import date, timedelta
import datetime
from work_calendar import calendars_factory
from workalendar.europe import France, FranceAlsaceMoselle


class public_holidays_holidays(osv.osv):
    _name = 'public.holidays.holidays'
    _description = 'Get days'

    def get_range(self, cr, uid, date_start, date_end, user=None, country='FR'):

        #INITIALSATION
        calendars = calendars_factory.get_instance()
        calendars.register(France, 'France', 'FR')
        calendars.register(FranceAlsaceMoselle, 'France Alsace/Moselle', 'FA')


        days_off = None
        # TASK 1 : get all dayoffs
        current_year = date_start.year
        last_year = date_end.year
        while current_year <= last_year:
            current_days = calendars[country].holidays_set(current_year)

            #print "DAYS = " + str(current_days)
            if days_off is None:
                days_off = current_days
            else:
                days_off = days_off.union(current_days)
            current_year += 1

        #print "FINAL DAYS = " + str(days_off)

        # TASK 2 : if calendar, get all forced_days of this calendar
        fixed_days = self.pool.get('public.holidays.days')\
            .search(cr, uid,
                    [('date', '>', date_start), ('date', '<', date_end)])
        # @TODO : Concat fixed days with regulars days

        # TASK 3 : (IF TASK 2) : sum of both arrays.

        # TASK 4 return result
        return days_off

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


class holidays_config_conpany(osv.osv):
    _inherit = 'res.company'

    def calendar_link(self, cr, uid, ids, context=None):
        action = self.pool.get('ir.actions.act_window').for_xml_id(
            cr,
            uid,
            'resource',
            'action_resource_calendar_form',
            context=context
        )
        return action





