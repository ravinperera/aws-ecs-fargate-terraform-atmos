variable "tenant" {
  description = "Tenant or organisation identifier."
  type        = string
}

variable "environment" {
  description = "Deployment environment, for example dev, staging, or prod."
  type        = string
}

variable "stage" {
  description = "Deployment stage or stack grouping."
  type        = string
}

variable "region" {
  description = "AWS region."
  type        = string
}

variable "name" {
  description = "Service and container name."
  type        = string
}

variable "cluster_arn" {
  description = "ECS cluster ARN."
  type        = string
}

variable "task_execution_role_arn" {
  description = "IAM role used by ECS to pull images and read secrets."
  type        = string
}

variable "task_role_arn" {
  description = "IAM role assumed by the running application container."
  type        = string
}

variable "container_image" {
  description = "ECR image URI without tag."
  type        = string

  validation {
    condition     = length(trimspace(var.container_image)) > 0
    error_message = "container_image must be a non-empty image repository URI."
  }
}

variable "container_version" {
  description = "Immutable container image tag, usually a Git SHA or release version."
  type        = string

  validation {
    condition = (
      length(trimspace(var.container_version)) > 0 &&
      lower(trimspace(var.container_version)) != "latest"
    )
    error_message = "container_version must be a non-empty immutable tag; the mutable 'latest' tag is not allowed."
  }
}

variable "container_port" {
  description = "Application container port."
  type        = number

  validation {
    condition     = var.container_port >= 1 && var.container_port <= 65535
    error_message = "container_port must be between 1 and 65535."
  }
}

variable "desired_count" {
  description = "Number of ECS tasks to run."
  type        = number
  default     = 2

  validation {
    condition     = var.desired_count >= 0 && floor(var.desired_count) == var.desired_count
    error_message = "desired_count must be a non-negative whole number."
  }
}

variable "cpu" {
  description = "Fargate task CPU units."
  type        = number
  default     = 512

  validation {
    condition     = contains([256, 512, 1024, 2048, 4096, 8192, 16384], var.cpu)
    error_message = "cpu must be a supported Fargate CPU value."
  }
}

variable "memory" {
  description = "Fargate task memory in MiB."
  type        = number
  default     = 1024

  validation {
    condition     = var.memory >= 512 && floor(var.memory) == var.memory
    error_message = "memory must be a whole number of at least 512 MiB."
  }
}

variable "subnet_ids" {
  description = "Private subnet IDs used by the ECS service."
  type        = list(string)

  validation {
    condition     = length(var.subnet_ids) > 0 && alltrue([for id in var.subnet_ids : length(trimspace(id)) > 0])
    error_message = "subnet_ids must contain at least one non-empty subnet ID."
  }
}

variable "security_group_ids" {
  description = "Security groups attached to the ECS service."
  type        = list(string)

  validation {
    condition     = length(var.security_group_ids) > 0 && alltrue([for id in var.security_group_ids : length(trimspace(id)) > 0])
    error_message = "security_group_ids must contain at least one non-empty security group ID."
  }
}

variable "target_group_arn" {
  description = "ALB target group ARN."
  type        = string
}

variable "log_group_name" {
  description = "CloudWatch log group name."
  type        = string
}

variable "log_retention_days" {
  description = "CloudWatch log retention in days."
  type        = number
  default     = 30

  validation {
    condition = contains([
      1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545,
      731, 1096, 1827, 2192, 2557, 2922, 3288, 3653
    ], var.log_retention_days)
    error_message = "log_retention_days must be a retention period supported by CloudWatch Logs."
  }
}

variable "environment_variables" {
  description = "Plain non-sensitive container environment variables."
  type        = map(string)
  default     = {}
}

variable "secrets" {
  description = "Sensitive environment variables mapped to Secrets Manager ARNs."
  type        = map(string)
  default     = {}
}

variable "health_check_command" {
  description = "Container health check command."
  type        = string
  default     = "curl -f http://localhost:8000/health || exit 1"

  validation {
    condition     = length(trimspace(var.health_check_command)) > 0
    error_message = "health_check_command must not be empty."
  }
}

variable "enable_execute_command" {
  description = "Enable ECS Exec for controlled operational access."
  type        = bool
  default     = true
}

variable "tags" {
  description = "Tags applied to supported resources."
  type        = map(string)
  default     = {}
}
