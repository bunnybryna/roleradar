variable "project_id" {
  type        = string
  description = "GCP project ID"
}

variable "region" {
  type        = string
  description = "GCP region"
  default     = "us-east1"
}

variable "zone" {
  type        = string
  description = "GCP zone"
  default     = "us-east1-b"
}

variable "instance_name" {
  type        = string
  description = "Compute Engine instance name"
  default     = "roleradar"
}

variable "machine_type" {
  type        = string
  description = "Compute Engine machine type"
  default     = "e2-micro"
}

variable "data_disk_size_gb" {
  type        = number
  description = "Persistent disk size (GB)"
  default     = 20
}

variable "fqdn" {
  type        = string
  description = "Fully qualified domain name for the app"
}

variable "duckdns_subdomain" {
  type        = string
  description = "DuckDNS subdomain (without .duckdns.org)"
}

variable "duckdns_token" {
  type        = string
  description = "DuckDNS token"
  sensitive   = true
}

variable "ghcr_image" {
  type        = string
  description = "GHCR image to run"
  default     = "ghcr.io/bunnybryna/roleradar:latest"
}

variable "ghcr_username" {
  type        = string
  description = "Optional GHCR username (required for private images)"
  default     = ""
}

variable "ghcr_token" {
  type        = string
  description = "Optional GHCR token (required for private images)"
  default     = ""
  sensitive   = true
}
