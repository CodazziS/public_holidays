# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 TeMPO Consulting
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv, fields

from datetime import date
from datetime import timedelta

class easter_day(date):

    def __new__(cls, year = 0):
        
        if year == 0:
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


class public_holidays(osv.Model):
    _name = 'public_holidays'
    _description = 'Public holidays management'
    _rec_name = 'pub_holiday_name'
    
    _columns = {
        'pub_holiday_id' : fields.integer('Holiday id', required=True),
        'pub_holiday_name' : fields.char('Name', required=True),
        'pub_holiday_type' : fields.selection([(0, 'Fixed'), (1, 'Variable')], string='Type', required=True),
        'pub_holiday_month' : fields.integer('Month', required=False),
        'pub_holiday_day' : fields.integer('Day', required=False),
        'pub_holiday_regime' : fields.selection([(0, 'General'), (1, 'Local')], string='Régime', required=True),
        'pub_holiday_expr' : fields.char('Expression', required=False),
    }

    _defaults = {
        'pub_holiday_regime' : 0,
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: