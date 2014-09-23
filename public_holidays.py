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

class public_holidays(osv.Model):
    _name = 'public_holidays'
    _description = 'Gestion des jours fériés'
    _rec_name = 'pub_holiday_name'
    
    _columns = {
        'pub_holiday_id' : fields.integer('holiday id', required=True),
        'pub_holiday_name' : fields.char('Nom', required=True),
        'pub_holiday_type' : fields.selection([(0, 'Fixe'), (1, 'Variable')], string='Type', required=True),
        'pub_holiday_month' : fields.integer('Mois', required=False),e
        'pub_holiday_day' : fields.integer('Jour', required=False),
        'pub_holiday_regime' : fields.selection([(0, 'Général'), (1, 'Local')], string='Régime', required=True),
        'pub_holiday_expr' : fields.char('Expression', required=False),
    }

    _defaults = {
        'pub_holiday_regime' : 0,
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: