import pulumi
import pytest


class MyMocks(pulumi.runtime.Mocks):
    def new_resource(self, type_, name, inputs, provider, id_):
        return [name + "_id", inputs]

    def call(self, token, args, provider):
        return {}


pulumi.runtime.set_mocks(MyMocks())

import app


@pulumi.runtime.test
def test_using_ga_deployment_api():
    def assertion(args):
        api_version = args[0]
        assert api_version == "apps/v1"

    return pulumi.Output.all(app.deployment.api_version).apply(assertion)
