# A host project provides network resources to associated service projects.
//resource "google_compute_shared_vpc_host_project" "host" {
//  project = var.shared_vpc_host_project
//}

# A service project gains access to network resources provided by its
# associated host project.
//resource "google_compute_shared_vpc_service_project" "service" {
//  count = length(var.project_ids)
//  host_project    = google_compute_shared_vpc_host_project.host.project
//  service_project = var.project_ids[count.index]
//  depends_on = [google_compute_shared_vpc_host_project.host]
//}

