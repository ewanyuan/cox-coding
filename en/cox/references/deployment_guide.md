# Observability System Deployment Guide

## Table of Contents
- [Environment Preparation](#environment-preparation)
- [Static Web Solution Deployment](#static-web-solution-deployment)
- [Interactive Web Solution Deployment](#interactive-web-solution-deployment)
- [Comprehensive Solution Deployment](#comprehensive-solution-deployment)
- [Solution Migration](#solution-migration)
- [Common Issues](#common-issues)

## Environment Preparation

### Basic Environment Requirements
- Python 3.7+
- pip package manager

### Static Web Solution Environment
No additional dependencies required, Python standard library sufficient

### Interactive Web Solution Environment
Install Flask dependencies:
```bash
pip install flask>=2.0.0
```

### Comprehensive Solution Environment
- Docker 20.10+
- Docker Compose 2.0+
- At least 2GB available memory

## Static Web Solution Deployment

### Deployment Steps

1. **Prepare Data Files**
   Create three JSON files according to data format specification:
   - `project_data.json`
   - `app_status.json`
   - `test_metrics.json`

2. **Generate Static Webpage**
   ```bash
   python scripts/run_web_observability.py \
     --mode static \
     --project project_data.json \
     --app app_status.json \
     --test test_metrics.json \
     --output observability.html
   ```

3. **View Generated Webpage**
   Script generates `observability.html` file, can be opened directly in browser

4. **Refresh Data**
   Re-run above command to regenerate HTML file with latest data
   ```bash
   # Regenerate
   python scripts/run_web_observability.py --mode static --project project_data.json --app app_status.json --test test_metrics.json --output observability.html
   ```

### Parameter Description
- `--project`: Project data file path (required)
- `--app`: Application status file path (required)
- `--test`: Test metrics file path (required)
- `--mode`: Operation mode (required, static for static web mode)
- `--output`: Output HTML file path (optional, default: observability.html)

### Advantages
- Zero configuration, ready to use
- No network service required, suitable for local development
- Can be combined with grep, awk and other tools for customized analysis

### Limitations
- No visualization interface
- No multi-user access support
- No historical data comparison

## Interactive Web Solution Deployment

### Deployment Steps

1. **Prepare Data Files**
   Same as static web solution, create three JSON data files

2. **Install Dependencies**
   ```bash
   pip install flask>=2.0.0
   ```

3. **Start Web Service**
   ```bash
   python scripts/run_web_observability.py \
     --mode web \
     --project project_data.json \
     --app app_status.json \
     --test test_metrics.json \
     --port 5000
   ```

4. **Access Web Interface**
   Open `http://localhost:5000` in browser

5. **Auto Refresh**
   Web interface supports auto refresh (default every 30 seconds), no manual reload required

### Parameter Description
- `--project`: Project data file path (required)
- `--app`: Application status file path (required)
- `--test`: Test metrics file path (required)
- `--mode`: Operation mode (required, web for interactive web mode)
- `--port`: Web service port (optional, default: 5000)
- `--refresh-interval`: Auto refresh interval in seconds (optional, default: 30)

### Web Interface Functions
1. **Project Overview**: Shows iteration list, task statistics, assumption status
2. **Application Status**: Shows module list, completion rate, status distribution
3. **Test Monitoring**: Shows test suite results, tracing point status, anomaly list
4. **Real-time Refresh**: Automatically detects data file changes and refreshes interface
5. **Filtering**: Supports filtering by status, priority, etc.

### Advanced Configuration
Modify service listening address:
```bash
python scripts/run_web_observability.py \
  --mode web \
  --project project_data.json \
  --app app_status.json \
  --test test_metrics.json \
  --host 0.0.0.0 \
  --port 5000
```

Other devices can then access via `http://<server-IP>:5000`

### Advantages
- Visual interface, intuitive and easy to understand
- Multi-user access support
- Real-time data refresh
- Simple deployment, low maintenance cost

### Limitations
- No historical data storage
- No alert mechanism
- Limited extensibility

## Comprehensive Solution Deployment

### Deployment Steps

1. **Prepare Environment**
   ```bash
   # Check Docker version
   docker --version

   # Check Docker Compose version
   docker-compose --version
   ```

2. **Prepare Data Files**
   Same as other solutions, create three JSON data files

3. **Configure Prometheus**
   Edit `assets/docker_compose/prometheus.yml`, add data collection configuration:
   ```yaml
   scrape_configs:
     - job_name: 'observability'
       static_configs:
         - targets: ['localhost:8080']
       scrape_interval: 30s
   ```

4. **Start Services**
   ```bash
   cd assets/docker_compose
   docker-compose up -d
   ```

5. **Access Services**
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3000 (default account: admin/admin)

6. **Configure Grafana**
   - After logging into Grafana, add Prometheus data source
   - Import pre-configured dashboard (located at `assets/docker_compose/grafana/dashboards/`)
   - Start monitoring observability data

### Data Conversion Script
Convert JSON data to Prometheus metrics format:

```bash
python scripts/collect_data.py export-prometheus \
  --project project_data.json \
  --app app_status.json \
  --test test_metrics.json \
  --output metrics.prom
```

Then let Prometheus collect the metric file.

### Docker Compose Service Description

| Service Name | Port | Description |
|---------|------|------|
| prometheus | 9090 | Metric collection and storage |
| grafana | 3000 | Visualization dashboard |
| pushgateway | 9091 | Temporary metric push (optional) |

### Advantages
- Professional-grade monitoring capabilities
- Historical data storage and query support
- Rich alert rules
- Scalable to production environment
- Standard technology stack, mature community

### Limitations
- Higher deployment complexity
- Requires more system resources
- Steeper learning curve

## Solution Migration

### Simple -> Medium
Migration steps:
1. Data files universal, no modifications needed
2. Install Flask dependencies
3. Start web service
4. Access web interface for verification

### Medium -> Comprehensive
Migration steps:
1. Prepare Docker environment
2. Use data conversion script to generate Prometheus metrics
3. Configure Prometheus and Grafana
4. Verify data correctness
5. Gradually switch to new system

### Comprehensive -> Interactive Web/Static Web
To downgrade:
1. Retain original JSON data files
2. Directly use interactive web or static web solution scripts
3. Clean up Docker containers and images

## Common Issues

### Static Web Solution Related Issues

**Q: HTML file too large to handle?**
A: Regularly clean or regenerate, keep data files concise.

**Q: How to filter data for specific iteration?**
A: Regenerate static webpage with filter parameters (if supported) or manually find in page.

### Interactive Web Solution Related Issues

**Q: Web interface inaccessible?**
A: Check if port is occupied, try modifying `--port` parameter; check firewall settings.

**Q: Data updates but interface doesn't refresh?**
A: Confirm data file saved successfully, wait for auto-refresh cycle (default 30 seconds), or manually refresh browser page.

**Q: How to allow other team members access?**
A: Use `--host 0.0.0.0` parameter, and ensure network accessibility.

### Comprehensive Solution Related Issues

**Q: Docker container startup failure?**
A: Check port occupancy, Docker resource limits, view container logs: `docker-compose logs <service_name>`

**Q: Grafana cannot connect to Prometheus?**
A: Check URL in data source configuration (usually `http://prometheus:9090`)

**Q: How to customize Grafana dashboard?**
A: Create new dashboard in Grafana interface, or edit pre-configured dashboard to meet specific needs.

### Data Related Issues

**Q: Data format validation failure?**
A: Use `scripts/collect_data.py validate` command to check specific error information, reference data format specification to correct.

**Q: How to import data from existing system?**
A: Write conversion script to convert existing system data to JSON format compliant with specification.

**Q: How to version control data files?**
A: Recommend incorporating data files into Git version control for tracking historical changes.

## Best Practices

1. **Choose appropriate solution**: Select deployment solution based on team size and requirements
2. **Regular data updates**: Establish data update mechanism to maintain observability data freshness
3. **Continuous optimization**: Continuously adjust monitoring metrics and interface display based on usage feedback
4. **Documentation maintenance**: Update data files and configuration documentation timely, maintain information synchronization
5. **Backup important data**: Regularly backup JSON data files to prevent accidental loss
6. **Security considerations**: Pay attention to access control and data encryption when using in production environment