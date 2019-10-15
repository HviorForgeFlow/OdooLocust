# OdooLocust

An Odoo load testing solution, using odoorpc and Locust

## Links

* OdooRPC: <a href="https://github.com/OCA/odoorpc">odoorpc</a>
* Locust: <a href="http://locust.io">locust.io</a>
* Odoo: <a href="https://odoo.com">odoo.com</a>

## HowTo

To load test Odoo, you create tasks sets like you'll have done it with Locust:

```python
from locust import task
from OdooLocust.OdooRPCTaskSet import OdooRPCTaskSet

class SellerTaskSet(OdooRPCTaskSet):

    @task(20)
    def create_so(self):
        prod_model = self.env['product.product']
        cust_model = self.env['res.partner']
        so_model = self.env['sale.order']

        cust_id = cust_model.search([('name', 'ilike', 'fletch')])[0]
        prod_ids = prod_model.search([('name', 'ilike', 'ipad')])

        order_id = so_model.create({
            'partner_id': cust_id,
            'order_line': [(0,0,{'product_id': prod_ids[0], 
                                 'product_uom_qty':1}),
                           (0,0,{'product_id': prod_ids[1], 
                                 'product_uom_qty':2}),
                          ],

        })
        so_model.action_button_confirm([order_id,])
```

then you create a profile, based on your taskset, which use OdooLocust instead of Locust:

```python
from OdooLocust import OdooLocust
from SellerTaskSet import SellerTaskSet

class Seller(OdooLocust.OdooLocust):
    host = "127.0.0.1"
    database = "test_db"
    min_wait = 100
    max_wait = 1000
    weight = 3

    task_set = SellerTaskSet
```

and you finally run your locust tests the usual way:

```bash
locust -f my_file.py Seller
```

## Generic test

This version is shipped with a generic TaskSet task, OdooTaskSet, and a TaskSet which randomly click on menu items, 
OdooGenericTaskSet.  To use this version, create this simple test file:

```python
from OdooLocust import OdooLocust
from OdooLocust import OdooRPCTaskSet


class Generic(OdooLocust.OdooLocust):
    host = "127.0.0.1"
    database = "testdb"
    min_wait = 100
    max_wait = 1000
    weight = 3

    task_set = OdooRPCTaskSet.OdooRPCTaskSet
```

and you finally run your locust tests the usual way:

```bash
locust -f my_file.py Generic
```
