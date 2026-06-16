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
}

variable "container_version" {
  description = "Container image tag, usually a Git SHA or release version."
  type        = string
}

variable "container_port" {
  description = "Application container port."
  type        = number
}

variable "desired_count" {
  description = "Number of ECS tasks to run."
  type        = number
  default     = 2
}

variable "cpu" {
  description = "Fargate task CPU units."
  type        = number
  default     = 512
}

variable "memory" {
  description = "Fargate task memory in MiB."
  type        = number
  default     = 1024
}

variable "subnet_ids" {
  description = "Private subnet IDs used by the ECS service."
  type        = list(string)
}

variable "security_group_ids" {
  description = "Security groups attached to the ECS service."
  type        = list(string)
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
