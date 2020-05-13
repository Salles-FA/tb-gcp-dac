# python app writes to this file to determine what modules get executed and how many times

# example follows - this would be written by python app before terraform executed
module "solution_folder" {
  source = "./solution_folder"
  region = var.region
  region_zone = var.region_zone
  root_id = var.root_id
  solution_name = var.solution_name
  tb_discriminator = var.tb_discriminator
}

module "workspace_project" {
  source = "./workspace_project"
  region = var.region
  region_zone = var.region_zone
  folder_id = module.solution_folder.solution_id
  tb_discriminator = var.tb_discriminator
  business_unit = var.business_unit
  cost_centre = var.cost_centre
  random_element = var.random_element
  billing_account = var.billing_account
  vpc_host_project = var.vpc_host_project
  solution_name = var.solution_name

}

module "environment_projects" {
  source = "./environment_project"
  project_name = "${var.solution_name}-dev-env"
  region = var.region
  region_zone = var.region_zone
  folder_id = module.solution_folder.solution_id
  tb_discriminator = var.tb_discriminator
  business_unit = var.business_unit
  cost_centre = var.cost_centre
  random_element = var.random_element
  billing_account = var.billing_account
  environments = var.environments
  vpc_host_project = var.vpc_host_project
  solution_name = var.solution_name
}
