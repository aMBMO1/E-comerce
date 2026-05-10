terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "3.0.2"
    }
  }
}

provider "docker" {}

resource "docker_image" "node_alpine" {
  name = "node:18-alpine"
}

resource "docker_container" "mern_backend" {
  name  = "mern-backend"
  image = docker_image.node_alpine.name

  ports {
    internal = 3000
    external = 3000
  }

  working_dir = "/app"
  command     = ["sh", "-c", "npm install && npm start"]
}