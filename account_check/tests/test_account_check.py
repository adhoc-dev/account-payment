##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo.tests import common


class TestAccountCheck(common.TransactionCase):

    def setUp(self):
        super(TestAccountCheck, self).setUp()
        self.partner.id = self.env['res.partner'].search(
            [('customer', '=', True)], limit=1)
        self.company.id = self.env['res.company'].search([], limit=1)
        self.company_currency = self.company.currency_id
        self.another_currency = self.env['res.currency'].search([(
            'id', '!=', self.company_currency)], limit=1)
        self.third_check_journal.id = self.env['account.journal'].search([(
            'id', '!=', self.company_currency)], limit=1)
        self.payment_method_received = self.env.ref(
            'account_payment_method_received_third_check')

    def test_00_another_currency_check(self):
        # Generate a customer payment
        payment = self.env['account.payment'].create({
            'partner_id': self.partner.id,
            'company_id': self.company.id,
            'payment_type_copy': 'inbound',
            'amount': 500,
            'currency_id': self.usd,
            'journal_id': self.third_check_journal.id,
            'payment_method_id': self.payment_method_received.id,
            # 'check_number': , 'payment_date':, 'check_name':,
            # 'check_issue_date':, 'check_bank_id':, 'check_owner_vat':,
            # 'check_owner_name':
        })
        # Generate check
        payment.post()
        check = payment.check_ids
        self.assertTrue(check)
        # Review generate aml
        # deposit check / craate transfer
        # post
        # assert check generate amls
