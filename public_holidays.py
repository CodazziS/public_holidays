from openerp.osv import fields, osv
from datetime import date, timedelta
import datetime
from work_calendar import calendars_factory
from workalendar.europe import France, FranceAlsaceMoselle


class public_holidays_holidays(osv.osv):
    _name = 'public.holidays.holidays'
    _description = 'Get days'

    def get_range(self, cr, uid, date_start, date_end, country='FA'):

        #INITIALSATION
        calendars = calendars_factory.get_instance()
        calendars.register(France, 'France', 'FR')
        calendars.register(FranceAlsaceMoselle, 'France Alsace/Moselle', 'FA')

        days_off = None
        # get all dayoffs
        current_year = date_start.year
        last_year = date_end.year
        while current_year <= last_year:
            current_days = calendars[country].holidays_set(current_year)
            if days_off is None:
                days_off = current_days
            else:
                days_off = days_off.union(current_days)
            current_year += 1

        days_off = list(days_off)

        #convert in list
        days_off_list = list()
        for d in days_off:
            days_off_list.append(str(d))

        # if calendar, get all forced_days of this calendar
        fdays = self.pool.get('public.holidays.days')\
            .search(cr, uid,
                    [('date', '>=', date_start), ('date', '<', date_end)])

        for d in self.pool.get('public.holidays.days').browse(cr, uid, fdays):
            if d.holiday is True:
                if not str(d.date) in days_off_list:
                    days_off_list.append(str(d.date))
            else:
                if d.date in days_off_list:
                    days_off_list.remove(str(d.date))

        # return result
        return days_off_list

    def is_holiday(self, cr, uid, date):
        days = self.pool.get('public.holidays')\
            .search(cr, uid, [('date', '=', str(date))])
        if days:
            return True
        return False


class public_holidays(osv.osv):
    _name = 'public.holidays'
    _description = 'Store holidays'

    def cron_restore_holidays(self, cr, uid, context=None):
        # Remove all values
        ids = self.search(cr, uid, [], context=context)
        self.unlink(cr, uid, ids, context=context)

        date_today = datetime.date.today()
        year_begin = datetime.datetime(date_today.year, 1, 1, 0, 0)
        year_end = datetime.datetime((date_today.year + 1), 1, 1, 0, 0)
        days = self.pool.get('public.holidays.holidays')\
            .get_range(cr, uid, year_begin, year_end)
        for day in days:
            vals = {
                'date': day,
            }
            self.create(cr, uid, vals, context=context)
        return None

    _columns = {
        'date': fields.date('Date'),
    }

    _order = "date asc"


class holidays_days(osv.osv):
    _name = 'public.holidays.days'
    _description = 'Store holidays days'

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





