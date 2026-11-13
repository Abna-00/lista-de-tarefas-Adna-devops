# Sistema de Lista de Tarefas — DevOps, CI e IaC

API REST (Flask) com pipeline de CI no GitHub Actions e infraestrutura AWS descrita em Terraform.

## Estrutura

```
app/                      API Flask
tests/                    Testes automatizados (pytest)
Dockerfile                Empacotamento da aplicação
.github/workflows/ci.yml  Pipeline de CI
terraform/                Scripts de IaC (VPC, EC2, ECR, Security Group)
```

## Executar localmente

```bash
pip install -r requirements-dev.txt
flake8 .
pytest --cov=app --cov-fail-under=80
python -m app.main        # http://localhost:5000
```

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| GET | /health | Saúde da API |
| POST | /tasks | Criar tarefa |
| GET | /tasks?done=true\|false | Listar (com filtro) |
| GET | /tasks/{id} | Consultar |
| PUT | /tasks/{id} | Atualizar |
| POST | /tasks/{id}/complete | Concluir |
| DELETE | /tasks/{id} | Remover |

## Infraestrutura (Terraform)

```bash
cd terraform
terraform init
terraform plan -var="ssh_allowed_cidr=SEU.IP/32"
terraform apply -var="ssh_allowed_cidr=SEU.IP/32"
terraform destroy   # ao final, para evitar custos
```

Requer credenciais AWS configuradas (`aws configure`). Nunca versione `.tfstate` ou `.tfvars`.

## CI

A cada push e Pull Request: lint → testes com cobertura ≥ 80% → build Docker → validação do Terraform.
