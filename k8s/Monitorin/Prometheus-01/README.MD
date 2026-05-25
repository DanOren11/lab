# Prometheus Stack on Kubernetes

This project installs a full monitoring stack on Kubernetes using:

- Prometheus
- Grafana
- Alertmanager
- kube-state-metrics
- node-exporter

Using the official `kube-prometheus-stack` Helm chart.

---

# Prerequisites

Make sure you already have:

- Kubernetes cluster running
- kubectl installed
- Helm installed

---

# Install Prometheus Stack

## Add Helm Repository

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
```

This adds the official Prometheus Helm charts repository.

---

## Update Helm Repositories

```bash
helm repo update
```

Downloads the latest chart versions.

---

## Install kube-prometheus-stack

```bash
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

This installs:

- Prometheus
- Grafana
- Alertmanager
- Exporters
- Prometheus Operator

Inside the `monitoring` namespace.

---

# Verify Installation

```bash
kubectl get pods -n monitoring
```

You should see pods like:

```text
prometheus-0
grafana-xxxxx
alertmanager-0
node-exporter-xxxxx
```

Wait until all pods are in `Running` state.

---

# Access Grafana

## Port Forward Grafana Service

```bash
kubectl port-forward svc/monitoring-grafana 3033:80 -n monitoring
```

Open in browser:

```text
http://localhost:3033
```

---

# Get Grafana Admin Password

```bash
kubectl get secret monitoring-grafana \
  -n monitoring \
  -o jsonpath="{.data.admin-password}" | base64 --decode
```

Default username:

```text
admin
```

---

# Access Prometheus

## Port Forward Prometheus Service

```bash
kubectl port-forward svc/monitoring-kube-prometheus-prometheus 9090 -n monitoring
```

Open in browser:

```text
http://localhost:9090
```

---

# Useful Prometheus Queries

## CPU Usage

```promql
rate(container_cpu_usage_seconds_total[5m])
```

## Memory Usage

```promql
container_memory_usage_bytes
```

## Number of Pods

```promql
count(kube_pod_info)
```

---

# Useful Commands

## View Services

```bash
kubectl get svc -n monitoring
```

## View All Monitoring Resources

```bash
kubectl get all -n monitoring
```

## Delete Stack

```bash
helm uninstall monitoring -n monitoring
```

---

# Architecture

```text
Kubernetes Cluster
│
├── Prometheus
│     ├── Scrapes Metrics
│     ├── Stores Time Series Data
│     └── Evaluates Alerts
│
├── Grafana
│     └── Dashboards & Visualization
│
├── Alertmanager
│     └── Sends Notifications
│
├── node-exporter
│     └── Node Metrics
│
└── kube-state-metrics
      └── Kubernetes Object Metrics
```

---

# Learning Goals

This setup helps practice:

- Kubernetes Monitoring
- Prometheus Queries (PromQL)
- Grafana Dashboards
- Alerting
- Kubernetes Observability

---
