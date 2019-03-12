
# Copyright 2017-present Open Networking Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import jinja2
import json
import yaml
from synchronizers.new_base.modelaccessor import *
from synchronizers.new_base.policy import Policy

from xosconfig import Config
from multistructlog import create_logger

log = create_logger(Config().get('logging'))

class NextEPCWebUIInstancePolicy(Policy):
    model_name = "NextEPCWebUIInstance"

    def handle_create(self, service_instance):
        log.info("handle_create NextEPCWebUIInstance")
        return self.handle_update(service_instance)


    def handle_update(self, service_instance):
        log.info("handle_update NextEPCWebUIInstance")
        owner = KubernetesService.objects.first()

        yaml_file = ["nextepc-webui-deployment.yaml", "nextepc-webui-service.yaml"]
        for file in yaml_file:
            input_file=os.path.join(os.path.abspath(os.path.dirname(os.path.realpath(__file__))), file)
            with open(input_file, 'r') as stream:
                try:
                    resource_definition=json.dumps(yaml.load(stream), sort_keys=True, indent=2)
                    stream.close()
                except yaml.YAMLError as exc:
                    resource_definition="{}"
                    print(exc)

            name="nextepcwebui-%s" % service_instance.id
            instance = KubernetesResourceInstance(name=name, owner=owner, resource_definition=resource_definition, no_sync=False)

            instance.save()

    def handle_delete(self, service_instance):
        log.info("handle_delete NextEPCWebUIInstance")
        service_instance.compute_instance.delete()
        service_instance.compute_instance = None
        service_instance.save(update_fields=["compute_instance"])
