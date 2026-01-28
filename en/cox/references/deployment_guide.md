# Observability System Deployment Guide

## Table of Contents
- [Environment Preparation](#environment-preparation)
- [Simple Solution Deployment](#simple-solution-deployment)
- [Intermediate Solution Deployment](#intermediate-solution-deployment)
- [Comprehensive Solution Deployment](#comprehensive-solution-deployment)
- [Solution Migration](#solution-migration)
- [Common Questions](#common-questions)

## Environment Preparation

### Basic Environment Requirements
- Python 3.7+
- pip package manager

### Simple Solution Environment
No additional dependencies needed, Python standard library sufficient

### Intermediate Solution Environment
Install Flask dependency:
```bash
pip install flask>=2.0.0
```

### Comprehensive Solution Environment
- Docker 20.10+
- Docker Compose 2.0+
- At least 2GB available memory

## Simple Solution Deployment

### Deployment Steps

1. **Prepare Data Files**
   Create three JSON files according to data format specifications:
   - `project_data.json`
   - `app_status.json`
   - `test_metrics.json`

2. **Generate Observability Log**
   ```bash
   python scripts/generate_observability_log.py \
     --project project_data.json \
     --app app_status.json \
     --test test_metrics.json
   ```

3. **View Log Output**
   Script outputs formatted observability information to terminal, also generates log file `observability.log`

4. **Analyze Logs**
   ```bash
   # View complete log
   cat observability.log

   # Filter specific dimensions
   grep "PROJECT:" observability.log
   grep "APP:" observability.log
   grep "TEST:" observability.log

   # View anomaly information
   grep "ANOMALY:" observability.log
   ```

### Parameter Descriptions
- `--project`: Project data file path (required)
- `--app`: Application status file path (required)
- `--test`: Test metrics file path (required)
- `--output`: Output log file path (optional, default: observability.log)

### Advantages
- Zero configuration, ready to use
- No network service needed, suitable for local development
- Can combine with grep, awk and other tools for customized analysis

### Limitations
- No visualization interface
- No multi-user access
- No historical data comparison

## Intermediate Solution Deployment

### Deployment Steps

1. **Prepare Data Files**
   Same as simple solution, create three JSON data files

2. **Install Dependencies**
   ```bash
   pip install flask>=2.0.0
   ```

3. **Launch Web Service**
   ```bash
   python scripts/run_web_observability.py \
     --project project_data.json \
     --app app_status.json \
     --test test_metrics.json \
     --port 5000
   ```

4. **Access Web Interface**
   Open `http://localhost:5000` in browser

5. **Auto Refresh**
   Web interface supports auto-refresh (default every 30 seconds), no need to manually reload page

### Parameter Descriptions
- `--project`: Project data file path (required)
- `--app`: Application status file path (required)
- `--test`: Test metrics file path (required)
- `--port`: Web service port (optional, default: 5000)
- `--refresh-interval`: Auto-refresh interval in seconds (optional, default: 30)

### Web Interface Functions
1. **Project Overview**: Display iteration list, task statistics, hypothesis status
2. **Application Status**: Display module list, completion rates, status distribution
3. **Test Monitoring**: Display test suite results, instrumentation point status, anomaly list
4. **Real-time Refresh**: Automatically detect data file changes and refresh interface
5. **Filter & Search**: Support filtering by status, priority and other conditions

### Advanced Configuration
Modify service listening address:
```bash
python scripts/run_web_observability.py \
  --project project_data.json \
  --app app_status.json \
  --test test_metrics.json \
  --host 0.0.0.0 \
  --port 5000
```

This allows other devices to access via `http://<serverIP>:5000`

### Advantages
- Visualization interface, intuitive and easy to understand
- Supports multi-user access
- Real-time data refresh
- Simple deployment, low maintenance cost

### Limitations
- No historical data storage
- No alerting mechanism
- Limited scalability

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

4. **Launch Services**
   ```bash
   cd assets/docker_compose
   docker-compose up -d
   ```

5. **Access Services**
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3000 (default account: admin/admin)

6. **Configure Grafana**
   - After logging into Grafana, add Prometheus data source
   - Import pre-configured dashboards (located in `assets/docker_compose/grafana/dashboards/`)
   - Start monitoring observability data

### Data Conversion Script
Convert JSON data to Prometheus metric format:

```bash
python scripts/collect_data.py export-prometheus \
  --project project_data.json \
  --app app_status.json \
  --test test_metrics.json \
  --output metrics.prom
```

Then let Prometheus collect this metric file.

### Docker Compose Services Description

| Service Name | Port | Description |
|--------------|------|-------------|
| prometheus | 9090 | Metric collection and storage |
| grafana | 3000 | Visualization dashboard |
| pushgateway | 9091 | Temporary metric push (optional) |

### Advantages
- Professional monitoring capabilities
- Supports historical data storage and query
- Rich alerting rules
- Scalable to production environment
- Standard technology stack, mature community

### Limitations
- Higher deployment complexity
- Requires more system resources
- Steeper learning curve

## Solution Migration

### Simple -> Intermediate
Migration steps:
1. Data files universal, no modification needed
2. Install Flask dependencies
3. Launch Web service
4. Access Web interface to verify

### Intermediate -> Comprehensive
Migration steps:
1. Prepare Docker environment
2. Use data conversion script to generate Prometheus metrics
3. Configure Prometheus and Grafana
4. Verify data correctness
5. Gradually switch to new system

### Comprehensive -> Intermediate/Simple
If downgrade needed:
1. Keep original JSON data files
2. Directly use intermediate or simple solution scripts
3. Clean up Docker containers and images

## Common Questions

### Simple Solution Related Questions

**Q: Log file too large, how to handle?**
A: Can periodically clean or use log rotation tools, such as `logrotate`.

**Q: How to filter data for specific iteration?**
A: Use `grep` to filter: `grep "ITERATION-ID" observability.log`

### Intermediate Solution Related Questions

**Q: Web interface inaccessible?**
A: Check if port is occupied, try modifying `--port` parameter; check firewall settings.

**Q: Interface not refreshing after data update?**
A: Confirm data file saved successfully, wait for auto-refresh cycle (default 30 seconds), or manually refresh browser page.

**Q: How to let other team members access?**
A: Use `--host 0.0.0.0` parameter, and ensure network accessibility.

### Comprehensive Solution Related Questions

**Q: Docker container fails to start?**
A: Check port occupation, Docker resource limits, view container logs: `docker-compose logs <service_name>`

**Q: Grafana cannot connect to Prometheus?**
A: Check if URL in data source configuration is correct (usually `http://prometheus:9090`)

**Q: How to customize Grafana dashboard?**
A: Create new dashboard in Grafana interface, or edit pre-configured dashboard to meet specific needs.

### Data Related Questions

**Q: Data format validation failed?**
A: Use `scripts/collect_data.py validate` command to check specific error messages, refer to data format specifications to correct.

**Q: How to import data from existing system?**
A: Write conversion script to convert existing system data to compliant JSON format.

**Q: How to version control data files?**
A: Recommend including data files in Git version control, facilitating tracking historical changes.

## Best Practices

1. **Choose Appropriate Solution**: Select deployment solution based on team size and requirements
2. **Regularly Update Data**: Establish data update mechanism to keep observability data fresh
3. **Continuous Optimization**: Continuously adjust monitoring metrics and interface display based on usage feedback
4. **Document Maintenance**: Timely update data files and configuration documents, keep information synchronized
5. **Backup Important Data**: Periodically backup JSON data files, prevent accidental loss
6. **Security Considerations**: For production environment use, pay attention to setting access control and data encryption
