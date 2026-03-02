terraform {
  required_providers {
    docker = {
      source = "kreuzwerker/docker"
    }
  }
}

provider "docker" {}

resource "docker_image" "postgres" {
  name = "postgres:15"
}

resource "docker_container" "postgres" {
  name  = "mlops_postgres"
  image = docker_image.postgres.image_id

  ports {
    internal = 5432
    external = 5432
  }

  env = [
    "POSTGRES_USER=postgres",
    "POSTGRES_PASSWORD=1234",
    "POSTGRES_DB=mlopsdb"
  ]
}
