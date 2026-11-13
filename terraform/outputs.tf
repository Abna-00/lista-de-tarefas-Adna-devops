output "instance_public_ip" {
  description = "IP público da instância da aplicação"
  value       = aws_instance.app.public_ip
}

output "ecr_repository_url" {
  description = "URL do repositório ECR"
  value       = aws_ecr_repository.app.repository_url
}

output "vpc_id" {
  description = "ID da VPC"
  value       = aws_vpc.main.id
}
