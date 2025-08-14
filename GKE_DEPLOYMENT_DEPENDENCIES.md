# 🔧 GKE Deployment Dependencies & Configuration

## 📋 **Overview**

This document outlines all the dependencies, tools, and configuration requirements needed to successfully deploy the Ghostbusters AI microservices to Google Kubernetes Engine (GKE).

---

## 🛠️ **Required Tools & Dependencies**

### **1. Google Cloud CLI (gcloud)**
- **Version:** 533.0.0 or later
- **Installation:** `curl https://sdk.cloud.google.com | bash`
- **Verification:** `gcloud version`

### **2. Kubectl (Kubernetes CLI)**
- **Version:** 1.32.4 or later
- **Installation:** `gcloud components install kubectl --quiet`
- **Verification:** `kubectl version --client`

### **3. Docker (for container builds)**
- **Version:** 20.10 or later
- **Installation:** `sudo apt-get install docker.io` (Ubuntu/Debian)
- **Verification:** `docker --version`

---

## ⚙️ **Configuration Requirements**

### **1. GCP Project Configuration**
```bash
# Set the active project
gcloud config set project ghostbusters-hackathon-2025

# Verify project configuration
gcloud config list
```

**Expected Output:**
```
[core]
account = your-email@domain.com
project = ghostbusters-hackathon-2025
```

### **2. GCP Authentication**
```bash
# Authenticate with Google Cloud
gcloud auth login

# Set default account
gcloud config set account your-email@domain.com

# Verify authentication
gcloud auth list
```

**Expected Output:**
```
ACTIVE  ACCOUNT
*       your-email@domain.com
```

### **3. Required APIs Enabled**
The following APIs must be enabled in the project:
- ✅ `container.googleapis.com` - GKE clusters
- ✅ `compute.googleapis.com` - VM instances, networking
- ✅ `monitoring.googleapis.com` - Metrics, alerts, dashboards
- ✅ `logging.googleapis.com` - Log aggregation
- ✅ `cloudresourcemanager.googleapis.com` - Project management
- ✅ `iam.googleapis.com` - Identity and access management

**Check API Status:**
```bash
gcloud services list --enabled --project=ghostbusters-hackathon-2025
```

---

## 🔐 **IAM Permissions Required**

### **Minimum Required Roles:**
- **Kubernetes Engine Admin** (`roles/container.admin`)
- **Compute Admin** (`roles/compute.admin`)
- **Service Account User** (`roles/iam.serviceAccountUser`)
- **Storage Admin** (`roles/storage.admin`) - for container registry

### **Verify Permissions:**
```bash
# Check current user permissions
gcloud projects get-iam-policy ghostbusters-hackathon-2025 \
  --flatten="bindings[].members" \
  --format="table(bindings.role)" \
  --filter="bindings.members:$(gcloud config get-value account)"
```

---

## 🚀 **Pre-Deployment Checklist**

### **Before Running Deployment:**
- [ ] **GCP Project Created** - `ghostbusters-hackathon-2025`
- [ ] **Billing Account Linked** - Connected to billing account
- [ ] **Required APIs Enabled** - All 6 APIs are active
- [ ] **gcloud CLI Installed** - Version 533.0.0+
- [ ] **kubectl Installed** - Version 1.32.4+
- [ ] **User Authenticated** - `gcloud auth login` completed
- [ ] **Project Set** - `gcloud config set project` completed
- [ ] **IAM Permissions** - User has required roles
- [ ] **Docker Available** - For container operations

---

## 📱 **Installation Commands**

### **Ubuntu/Debian:**
```bash
# Install Google Cloud CLI
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Install kubectl
gcloud components install kubectl --quiet

# Install Docker
sudo apt-get update
sudo apt-get install docker.io
sudo usermod -aG docker $USER
```

### **macOS:**
```bash
# Install Google Cloud CLI
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Install kubectl
gcloud components install kubectl --quiet

# Install Docker Desktop
# Download from https://www.docker.com/products/docker-desktop
```

### **Windows:**
```bash
# Install Google Cloud CLI
# Download from https://cloud.google.com/sdk/docs/install

# Install kubectl
gcloud components install kubectl --quiet

# Install Docker Desktop
# Download from https://www.docker.com/products/docker-desktop
```

---

## 🔍 **Verification Commands**

### **1. Verify gcloud Installation:**
```bash
gcloud version
```
**Expected Output:**
```
Google Cloud SDK 533.0.0
```

### **2. Verify kubectl Installation:**
```bash
kubectl version --client
```
**Expected Output:**
```
Client Version: v1.32.4-dispatcher
Kustomize Version: v5.5.0
```

### **3. Verify Docker Installation:**
```bash
docker --version
```
**Expected Output:**
```
Docker version 20.10.x, build xxxxxxx
```

### **4. Verify GCP Configuration:**
```bash
gcloud config list
```
**Expected Output:**
```
[core]
account = your-email@domain.com
project = ghostbusters-hackathon-2025
```

### **5. Verify Authentication:**
```bash
gcloud auth list
```
**Expected Output:**
```
ACTIVE  ACCOUNT
*       your-email@domain.com
```

### **6. Verify Project Access:**
```bash
gcloud projects describe ghostbusters-hackathon-2025
```
**Expected Output:**
```
projectId: ghostbusters-hackathon-2025
name: Ghostbusters AI Hackathon 2025
projectNumber: '123456789012'
lifecycleState: ACTIVE
```

---

## 🚨 **Common Issues & Solutions**

### **1. kubectl not found**
**Error:** `kubectl: command not found`
**Solution:** Install kubectl via gcloud components
```bash
gcloud components install kubectl --quiet
```

### **2. Authentication Required**
**Error:** `You do not currently have an active account selected.`
**Solution:** Authenticate with gcloud
```bash
gcloud auth login
```

### **3. Project Not Set**
**Error:** `Project [ghostbusters-hackathon-2025] not found.`
**Solution:** Set the correct project
```bash
gcloud config set project ghostbusters-hackathon-2025
```

### **4. Insufficient Permissions**
**Error:** `Permission denied on resource`
**Solution:** Request appropriate IAM roles from project admin

### **5. APIs Not Enabled**
**Error:** `API not enabled`
**Solution:** Enable required APIs
```bash
gcloud services enable container.googleapis.com
gcloud services enable compute.googleapis.com
# ... enable other required APIs
```

---

## 📚 **Additional Resources**

### **Official Documentation:**
- [Google Cloud CLI Installation](https://cloud.google.com/sdk/docs/install)
- [Kubectl Installation](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [GKE Quickstart](https://cloud.google.com/kubernetes-engine/docs/quickstart)
- [IAM Roles for GKE](https://cloud.google.com/kubernetes-engine/docs/how-to/iam)

### **Troubleshooting:**
- [GKE Troubleshooting Guide](https://cloud.google.com/kubernetes-engine/docs/troubleshooting)
- [Kubectl Troubleshooting](https://kubernetes.io/docs/tasks/debug-application-cluster/debug-cluster/)

---

## 🎯 **Next Steps After Configuration**

### **1. Run Pre-Deployment Checks:**
```bash
# Verify all dependencies are met
./scripts/verify-deployment-prerequisites.sh
```

### **2. Deploy GKE Cluster:**
```bash
# Execute the deployment script
./scripts/deploy-ghostbusters.sh
```

### **3. Verify Deployment:**
```bash
# Check cluster status
kubectl cluster-info
kubectl get nodes
```

---

## 🏁 **Summary**

**Before deploying to GKE, ensure you have:**

- ✅ **Google Cloud CLI** installed and configured
- ✅ **Kubectl** installed via gcloud components
- ✅ **Docker** available for container operations
- ✅ **GCP project** created and configured
- ✅ **Required APIs** enabled
- ✅ **IAM permissions** granted
- ✅ **Authentication** completed

**Once all dependencies are satisfied, you can proceed with the GKE deployment using the provided deployment script!** 🚀
