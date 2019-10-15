from locust import TaskSet


class OdooRPCTaskSet(TaskSet):

    def on_start(self):
        self.env = self.client.env
