# -*- coding: utf-8 -*-
# Copyright 2017 Coop IT Easy SCRLfs
#   - Robin Keunen <robin@coopiteasy.be>
#   - Houssine BAKKALI <houssine@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Pos Round Cash Payment Line",
    "version": "9.0.1.0.0",
    "author": "Coop IT Easy SCRLfs",
    "license": "AGPL-3",
    "category": "Point of Sale",
    "website": "www.coopiteasy.be",
    "description": """
        Rounds due amount to nearest 5 cents when adding a cash Payment line.
        An line is added on the invoice to record the rounding remainder.

        The product *Round Remainder Product* is added to your product list.
        You must set the Rounding Account through:
        - Round Remainder Product > Accounting
          - > Income Account
          - > Expense Account

    """,
    "depends": [
        'point_of_sale',
        'product',
    ],
    'data': [
        'views/pos_config.xml',
#        'views/account_journal_view.xml',
        'data/round_remainder_product.xml',
        'static/src/xml/templates.xml',
    ],
    'qweb': [
        'static/src/xml/pos_round_cash_payment_line.xml'
    ],
    'installable': True,
}
