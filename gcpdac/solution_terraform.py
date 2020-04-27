# Copyright 2019 The Tranquility Base Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import yaml
from flask import Flask
from flask_cors import CORS
from python_terraform import Terraform

from gcpdac.local_logging import get_logger
from gcpdac.utils import labellize

logger = get_logger()
logger.info("Logger initialised")

app = Flask(__name__)
app.logger = logger  # use our own logger for consistency vs flasks own
CORS(app)


def run_terraform(solutiondata, terraform_command):
    # builds and destroys solution
    # The configuration YAML file read by read_config_map() determines where this new infrastructure should sit
    # within a GCP project, as well as setting other properties like billing.
    # Accepts JSON content-type input.
    # returns return code and repsonse from terraform
    tf_data = dict()
    solution_id = solutiondata.get("id")
    tf_data['solution_id'] = solution_id
    logger.debug("solution_id is %s", solution_id)

    tf_data['solution_name'] = solutiondata.get("name", "NoneAsDelete")
    labellizedCostCentre = labellize(solutiondata.get("costCentre", "NoneAsDelete"))
    tf_data['cost_centre'] = labellizedCostCentre
    labellizedBusinessUnit = labellize(solutiondata.get("businessUnit", "NoneAsDelete"))
    tf_data['business_unit'] = labellizedBusinessUnit
    # TODO return the labellized versions of cost centre and business unit to the houston service (or billing service?)

    config = read_config_map()

    region = config['region']
    tf_data['region'] = region
    tf_data['activator_folder_id'] = config['activator_folder_id']
    tf_data['billing_account'] = config['billing_account']
    tf_data['shared_vpc_host_project'] = config['shared_vpc_host_project']
    tf_data['shared_network_name'] = config['shared_network_name']
    tf_data['shared_networking_id'] = config['shared_networking_id']
    tf_data['root_id'] = config['applications_folder_id']
    tb_discriminator = config['tb_discriminator']
    tf_data['tb_discriminator'] = tb_discriminator

    backend_prefix = str(solution_id) + '-' + tb_discriminator

    # TODO generate tfvars file from input - currently only region_zone in this file
    env_data = '/app/terraform/input.tfvars'
    # TODO pass region_zone in
    region_zone = region + "-b"
    tf_data['region_zone'] = region_zone

    terraform_source_path = '/app/terraform/'  # this should be the param to python script

    # TODO create 'modules.tf' file for solution. Will have correct number of environments
    # currently using a 'hard coded' modules.tf file that creates 3 environment projects

    tf: Terraform = Terraform(working_dir=terraform_source_path, variables=tf_data)
    return_code, stdout, stderr = tf.init(capture_output=False,
                                          backend_config={'bucket': config['terraform_state_bucket'],
                                                          'prefix': backend_prefix})
    logger.debug("Terraform init return code is {}".format(return_code))
    logger.debug("Terraform init stdout is {}".format(stdout))
    logger.debug("Terraform init stderr is {}".format(stderr))

    if terraform_command.lower() == 'destroy'.lower():
        return_code, stdout, stderr = tf.destroy(var_file=env_data, capture_output=False)
        logger.debug("Terraform destroy return code is {}".format(return_code))
        logger.debug("Terraform destroy stdout is {}".format(stdout))
        logger.debug("Terraform destroy stderr is {}".format(stderr))
    else:
        return_code, stdout, stderr = tf.apply(skip_plan=True, var_file=env_data, capture_output=False)
        logger.debug("Terraform apply return code is {}".format(return_code))
        logger.debug("Terraform apply stdout is {}".format(stdout))
        logger.debug("Terraform apply stderr is {}".format(stderr))

    return {"return_code": return_code, "stdout": stdout, "stderr": stdout}


def read_config_map():
    # Returns the EC configuration as a dictionary
    try:
        with open("/app/ec-config.yaml", 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                logger.exception("Failed to parse EC YAML after successfully opening - {}".format(exc))
                raise
    except Exception:
        logger.exception("Failed to load EC YAML file")
        raise


if __name__ == "__main__":
    print("TODO")