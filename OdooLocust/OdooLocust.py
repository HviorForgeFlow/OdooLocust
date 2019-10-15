# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (C) Stephane Wirtel
# Copyright (C) 2011 Nicolas Vanhoren
# Copyright (C) 2011 OpenERP s.a. (<http://openerp.com>).
# Copyright (C) 2017 Nicolas Seinlet
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met: 
# 
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer. 
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution. 
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
##############################################################################
import odoorpc
import time
import sys

from locust import Locust, events


def json(self, url, params):
    if params.get('service', False) and params.get('method', False):
        if params['service'] == "object" and 'execute' in params['method']:
            call_name = ': '.join(params['args'][3:5])
        else:
            call_name = '%s : %s' % (params['service'], params['method'])
    else:
        call_name = ': '.join([param for param in params])
    start_time = time.time()
    try:
        data = self._connector.proxy_json(url, params)
    except Exception as e:
        total_time = int((time.time() - start_time) * 1000)
        events.request_failure.fire(request_type="OdooRPC", name=call_name, response_time=total_time, exception=e)
        raise e
    else:
        total_time = int((time.time() - start_time) * 1000)
        events.request_success.fire(request_type="OdooRPC", name=call_name, response_time=total_time, response_length=sys.getsizeof(data))
    return data


odoorpc.ODOO.json = json


class OdooLocust(Locust):
    port = 8069
    database = "demo"
    login = "admin"
    password = "admin"
    protocol = "jsonrpc"

    def __init__(self):
        super(OdooLocust, self).__init__()
        self._connect()

    def _connect(self):
        try:
            self.client = odoorpc.ODOO(self.host, port=self.port, protocol=self.protocol)
            self.client.login(self.database, self.login, self.password)
        except Exception as e:
            raise e
