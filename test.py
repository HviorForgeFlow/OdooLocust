from locust import task, TaskSet
from OdooLocust import OdooLocust
from datetime import datetime


class PurchaseTaskSet(TaskSet):
      
    @task(20)
    def create_purchase(self):
        product = self.client.env.ref('product.product_product_4')
        partner = self.client.env.ref('base.res_partner_1')
        date = datetime.today().strftime('%Y-%m-%d')
        quantity = 1.0
        rslt = self.client.env['purchase.order'].create({
            'partner_id': partner.id,
            'order_line': [
                (0, 0, {
                    'name': product.name,
                    'product_id': product.id,
                    'product_qty': quantity,
                    'product_uom': product.uom_po_id.id,
                    'price_unit': 100.0,
                    'date_planned': date,
                })],
            'date_order': date,
        })
        self.client.env['purchase.order'].browse(rslt).button_confirm()


class Purchaser(OdooLocust.OdooLocust):
    host = "127.0.0.1"
    database = "12.0-locust-purchase_tier_validation"
    port = 8069
    min_wait = 100
    max_wait = 1000
    weight = 3

    task_set = PurchaseTaskSet

