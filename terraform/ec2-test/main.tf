terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "me-central-1"
}

resource "aws_instance" "app_server" {
  ami           = "ami-05d1e0e430e0bc2bb"
  instance_type = "t3.micro"

  tags = {
    Name = var.instance_name
  }
}
