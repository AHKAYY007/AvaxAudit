# AvaxAudit Docker Setup Guide

This guide explains how to use Docker to run the AvaxAudit application on both Linux and Windows systems.

## Prerequisites

### For Linux
- Docker Engine
- Docker Compose

### For Windows
- Docker Desktop for Windows
- WSL 2 (Windows Subsystem for Linux) recommended

## Installation

### Installing Docker

#### On Linux
```bash
# Update package index
sudo apt update

# Install dependencies
sudo apt install apt-transport-https ca-certificates curl software-properties-common

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Add Docker repository
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Install Docker
sudo apt update
sudo apt install docker-ce docker-compose

# Add your user to the docker group (to run docker without sudo)
sudo usermod -aG docker $USER
# Log out and log back in for changes to take effect
```

#### On Windows
1. Download and install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
2. During installation, enable WSL 2 integration
3. Start Docker Desktop after installation

## Getting Started

### Clone the Repository
```bash
# Linux
git clone https://github.com/your-repo/AvaxAudit.git
cd AvaxAudit

# Windows (PowerShell)
git clone https://github.com/your-repo/AvaxAudit.git
cd AvaxAudit
```

### Configure Environment Variables
Create a `.env` file in the project root or set the environment variable for your Snowtrace API key:

```bash
# Linux
echo "SNOWTRACE_API_KEY=your_api_key_here" > .env

# Windows (PowerShell)
echo "SNOWTRACE_API_KEY=your_api_key_here" | Out-File -FilePath .env -Encoding utf8
```

## Running the Application

### Start the Containers
```bash
# Linux (use sudo only if you didn't add your user to the docker group)
docker-compose up

# Windows (PowerShell or Command Prompt)
docker-compose up
```

To run in detached mode (background):
```bash
docker-compose up -d
```

### Rebuild Containers After Changes
```bash
docker-compose up --build
```

### Stop the Containers
```bash
# Keep the volumes and networks
docker-compose down

# Remove volumes too
docker-compose down -v
```

## Resolving Port Conflicts

If you encounter port conflicts (especially with PostgreSQL on port 5432), modify the docker-compose.yml file:

```yaml
db:
  # ... other settings
  ports:
    - "5433:5432"  # Change 5432 to another port like 5433
```

This keeps PostgreSQL running on port 5432 inside the container but maps to port 5433 on your host.

## Container Structure

- **Backend Service**: FastAPI application running on port 8000
- **Database Service**: PostgreSQL database running on port 5432

## Common Commands

### View Running Containers
```bash
docker ps
```

### View Logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend
docker-compose logs db

# Follow logs
docker-compose logs -f
```

### Access PostgreSQL Container
```bash
docker exec -it avaxaudit-db-1 psql -U postgres -d avaxaudits
```

### Access Backend Container Shell
```bash
docker exec -it avaxaudit-backend-1 bash
```

## Accessing the Application

Once the containers are running:
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Platform-Specific Notes

### Linux Notes
- If you receive permission errors, use `sudo` or ensure your user is in the docker group
- Local PostgreSQL may conflict with Docker's PostgreSQL port

### Windows Notes
- Docker runs in a virtualized Linux environment
- File performance is better when files are within the WSL2 filesystem
- Windows path mappings may cause issues with file watching

## Troubleshooting

### Container Won't Start
Check logs for errors:
```bash
docker-compose logs
```

### PostgreSQL Port Already in Use
```bash
# Linux: Stop local PostgreSQL service
sudo systemctl stop postgresql

# Or modify docker-compose.yml to use different port mapping
```

### Changes Not Reflected in Container
Rebuild the containers:
```bash
docker-compose up --build
```

## Development Workflow

1. Make changes to your code
2. Docker will automatically detect changes thanks to the volume mapping
3. For dependency changes, rebuild the containers with `docker-compose up --build`

---
