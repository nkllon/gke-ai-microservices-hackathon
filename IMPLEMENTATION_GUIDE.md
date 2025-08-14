# 🚀 Ghostbusters AI GKE Implementation Guide

**Project:** Ghostbusters AI Agent Microservices Platform on GKE  
**Objective:** Deploy AI agent microservices with cost control and monitoring  
**Timeline:** 1-month hackathon implementation  
**Status:** Ready for deployment  

---

## 📋 **Prerequisites**

### **Required Tools:**
- ✅ **gcloud CLI** - Google Cloud SDK
- ✅ **kubectl** - Kubernetes command-line tool
- ✅ **Docker** - Container runtime
- ✅ **Git** - Version control

### **GCP Requirements:**
- ✅ **Project:** `aardvark-linkedin-grepper`
- ✅ **Billing:** Enabled and configured
- ✅ **APIs:** Container Engine, Compute Engine, Monitoring APIs enabled
- ✅ **Permissions:** Owner or Editor role on project

---

## 🏗️ **Architecture Overview**

### **System Components:**
```
┌─────────────────────────────────────────────────────────────┐
│                    GKE Cluster                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              ghostbusters-ai                        │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │   │
│  │  │Orchestrator │ │Security    │ │Quality      │   │   │
│  │  │Service      │ │Agent       │ │Agent        │   │   │
│  │  └─────────────┘ └─────────────┘ └─────────────┘   │   │
│  │  ┌─────────────┐ ┌─────────────┐                   │   │
│  │  │Test Agent   │ │Performance  │                   │   │
│  │  │             │ │Agent        │                   │   │
│  │  └─────────────┘ └─────────────┘                   │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              ghostbusters-ingress                   │   │
│  │  ┌─────────────┐ ┌─────────────┐                   │   │
│  │  │Frontend     │ │Ingress      │                   │   │
│  │  │Service      │ │Controller   │                   │   │
│  │  └─────────────┘ └─────────────┘                   │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              ghostbusters-monitoring                │   │
│  │  ┌─────────────┐ ┌─────────────┐                   │   │
│  │  │Prometheus   │ │Grafana     │                   │   │
│  │  │Metrics      │ │Dashboards  │                   │   │
│  │  └─────────────┘ └─────────────┘                   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### **Cost Optimization Features:**
- **Machine Type:** e2-micro (smallest, cheapest)
- **Preemptible Instances:** 50% cost savings
- **Auto-scaling:** Conservative thresholds (80% CPU, 85% memory)
- **Resource Limits:** Minimal requests, reasonable limits
- **Node Limits:** 1-3 nodes maximum during development

---

## 🚀 **Quick Start Deployment**

### **1. Clone and Setup:**
```bash
# Clone the repository
git clone https://github.com/nkllon/gke-ai-microservices-hackathon.git
cd gke-ai-microservices-hackathon

# Make deployment script executable
chmod +x scripts/deploy-ghostbusters.sh
```

### **2. Run Deployment:**
```bash
# Execute the deployment script
./scripts/deploy-ghostbusters.sh
```

**The script will automatically:**
- ✅ Check prerequisites
- ✅ Authenticate with GCP
- ✅ Create cost-optimized GKE cluster
- ✅ Deploy all services and configurations
- ✅ Verify deployment status
- ✅ Show access information

---

## 🔧 **Manual Deployment Steps**

### **Step 1: Create GKE Cluster**
```bash
# Create cost-optimized cluster
gcloud container clusters create ghostbusters-hackathon \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --disk-size=20 \
  --disk-type=pd-standard \
  --preemptible \
  --enable-autoscaling \
  --min-nodes=1 \
  --max-nodes=3 \
  --enable-autorepair \
  --no-enable-autoupgrade \
  --enable-network-policy \
  --enable-ip-alias \
  --enable-stackdriver-kubernetes \
  --labels=cost-center=hackathon,environment=development,auto-shutdown=true
```

### **Step 2: Get Cluster Credentials**
```bash
# Get credentials for kubectl
gcloud container clusters get-credentials ghostbusters-hackathon --zone=us-central1-a
```

### **Step 3: Deploy Infrastructure**
```bash
# Create namespaces
kubectl apply -f k8s/namespaces/ghostbusters-namespace.yaml

# Deploy configuration
kubectl apply -f k8s/config/ghostbusters-config.yaml

# Deploy core services
kubectl apply -f k8s/services/orchestrator-service.yaml
kubectl apply -f k8s/services/ai-agents.yaml

# Deploy ingress and frontend
kubectl apply -f k8s/ingress/ghostbusters-ingress.yaml

# Deploy monitoring
kubectl apply -f k8s/monitoring/ghostbusters-monitoring.yaml
```

---

## 📊 **Verification and Testing**

### **Check Deployment Status:**
```bash
# Check namespaces
kubectl get namespaces | grep ghostbusters

# Check pods
kubectl get pods --all-namespaces | grep ghostbusters

# Check services
kubectl get services --all-namespaces | grep ghostbusters

# Check ingress
kubectl get ingress --all-namespaces
```

### **Test Services:**
```bash
# Test orchestrator health
kubectl exec -n ghostbusters-ai deployment/ghostbusters-orchestrator -- curl -s http://localhost:8080/health

# Test AI agent health
kubectl exec -n ghostbusters-ai deployment/ghostbusters-security-agent -- curl -s http://localhost:8080/health
```

### **Access Monitoring:**
```bash
# Port forward Prometheus
kubectl port-forward -n ghostbusters-monitoring service/prometheus 9090:9090

# Port forward Grafana
kubectl port-forward -n ghostbusters-monitoring service/grafana 3000:3000
```

---

## 💰 **Cost Monitoring and Control**

### **Daily Cost Checks:**
```bash
# Run existing GCP billing reporter
cd ..  # Go to OpenFlow-Playground root
python scripts/gcp_billing_daily_reporter.py
```

### **Real-time GKE Monitoring:**
```bash
# Check cluster costs
gcloud billing reports list --filter="service=container.googleapis.com"

# Check resource usage
kubectl top pods --all-namespaces
kubectl top nodes
```

### **Emergency Cost Control:**
```bash
# Scale down all deployments
kubectl scale deployment --all --replicas=1

# Disable auto-scaling
kubectl delete hpa --all

# Reduce cluster size
gcloud container clusters update ghostbusters-hackathon \
  --node-pool default-pool \
  --min-nodes 1 \
  --max-nodes 2
```

---

## 🔍 **Troubleshooting**

### **Common Issues:**

#### **1. Pods Not Starting:**
```bash
# Check pod events
kubectl describe pod <pod-name> -n <namespace>

# Check logs
kubectl logs <pod-name> -n <namespace>

# Check resource constraints
kubectl describe node <node-name>
```

#### **2. Services Not Accessible:**
```bash
# Check service endpoints
kubectl get endpoints --all-namespaces

# Check network policies
kubectl get networkpolicies --all-namespaces

# Test connectivity
kubectl run test-pod --image=busybox --rm -it --restart=Never -- nslookup <service-name>
```

#### **3. High Resource Usage:**
```bash
# Check resource usage
kubectl top pods --all-namespaces
kubectl top nodes

# Scale down if needed
kubectl scale deployment <deployment-name> --replicas=1
```

### **Debug Commands:**
```bash
# Get detailed cluster info
gcloud container clusters describe ghostbusters-hackathon --zone=us-central1-a

# Check cluster events
kubectl get events --all-namespaces --sort-by='.lastTimestamp'

# Check node status
kubectl get nodes -o wide
```

---

## 📈 **Scaling and Optimization**

### **Development Phase (Week 1):**
- **Target:** <$5/month
- **Configuration:** 1-2 nodes, minimal resources
- **Monitoring:** Daily cost tracking

### **Testing Phase (Week 2-3):**
- **Target:** <$15/month
- **Configuration:** 2-3 nodes, optimized resources
- **Monitoring:** Real-time cost alerts

### **Demo Phase (Week 4):**
- **Target:** <$25/month
- **Configuration:** 3-4 nodes, performance optimized
- **Monitoring:** Comprehensive cost control

---

## 🔗 **Integration Points**

### **1. TiDB Integration:**
```yaml
# Enable in ghostbusters-config.yaml
integrations:
  tidb:
    enabled: "true"
    connection_string: "your-tidb-connection-string"
    database_name: "ghostbusters"
```

### **2. Kiro Integration:**
```yaml
# Enable in ghostbusters-config.yaml
integrations:
  kiro:
    enabled: "true"
    plugin_path: "/.kiro/plugins/ghostbusters-ai"
    config_path: "/.kiro/config/ai-agents.yml"
```

### **3. External APIs:**
```yaml
# Add to configuration
external_apis:
  github:
    enabled: "true"
    token_env: "GITHUB_TOKEN"
  slack:
    enabled: "false"
    webhook_url: ""
```

---

## 📝 **Development Workflow**

### **1. Code Changes:**
```bash
# Make changes to Kubernetes manifests
vim k8s/services/ai-agents.yaml

# Apply changes
kubectl apply -f k8s/services/ai-agents.yaml

# Verify changes
kubectl get pods -n ghostbusters-ai
```

### **2. Configuration Updates:**
```bash
# Update configuration
vim k8s/config/ghostbusters-config.yaml

# Apply configuration
kubectl apply -f k8s/config/ghostbusters-config.yaml

# Restart services if needed
kubectl rollout restart deployment/ghostbusters-orchestrator -n ghostbusters-ai
```

### **3. Monitoring Updates:**
```bash
# Update monitoring configuration
vim k8s/monitoring/ghostbusters-monitoring.yaml

# Apply monitoring updates
kubectl apply -f k8s/monitoring/ghostbusters-monitoring.yaml
```

---

## 🎯 **Success Metrics**

### **Technical Metrics:**
- ✅ **Availability:** 99.9% uptime
- ✅ **Response Time:** <500ms average
- ✅ **Throughput:** 1000+ requests/second
- ✅ **Auto-scaling:** Responsive within 5 minutes

### **Cost Metrics:**
- ✅ **Development:** <$5/month
- ✅ **Testing:** <$15/month
- ✅ **Demo:** <$25/month
- ✅ **Emergency Controls:** Never needed

### **Business Metrics:**
- ✅ **AI Agent Performance:** All agents operational
- ✅ **Code Quality:** Automated analysis working
- ✅ **Security Scanning:** Vulnerability detection active
- ✅ **Performance Analysis:** Optimization recommendations

---

## 🚨 **Emergency Procedures**

### **Cost Exceeded:**
1. **Immediate Scale Down:**
   ```bash
   kubectl scale deployment --all --replicas=1
   ```

2. **Disable Auto-scaling:**
   ```bash
   kubectl delete hpa --all
   ```

3. **Reduce Cluster Size:**
   ```bash
   gcloud container clusters update ghostbusters-hackathon \
     --min-nodes 1 \
     --max-nodes 2
   ```

### **Service Failure:**
1. **Check Pod Status:**
   ```bash
   kubectl get pods --all-namespaces
   ```

2. **Restart Failed Services:**
   ```bash
   kubectl rollout restart deployment/<service-name> -n <namespace>
   ```

3. **Check Logs:**
   ```bash
   kubectl logs <pod-name> -n <namespace>
   ```

---

## 📚 **Additional Resources**

### **Documentation:**
- **GKE Documentation:** https://cloud.google.com/kubernetes-engine/docs
- **Kubernetes Documentation:** https://kubernetes.io/docs/
- **Cost Optimization:** https://cloud.google.com/kubernetes-engine/docs/concepts/cost-optimization

### **Tools:**
- **GKE Console:** https://console.cloud.google.com/kubernetes
- **Cloud Monitoring:** https://console.cloud.google.com/monitoring
- **Billing Console:** https://console.cloud.google.com/billing

### **Support:**
- **GCP Support:** https://cloud.google.com/support
- **Community:** https://stackoverflow.com/questions/tagged/google-kubernetes-engine

---

## 🎉 **Next Steps**

### **Immediate Actions:**
1. ✅ **Review Architecture** - Understand the system design
2. ✅ **Check Prerequisites** - Ensure all tools are installed
3. ✅ **Run Deployment** - Execute the deployment script
4. ✅ **Verify Deployment** - Check all services are running
5. ✅ **Test Functionality** - Verify AI agents are working

### **Development Actions:**
1. **Customize Configuration** - Update for your specific needs
2. **Add Custom AI Agents** - Extend the agent ecosystem
3. **Integrate External Services** - Connect to TiDB, Kiro, etc.
4. **Optimize Performance** - Fine-tune resource allocation
5. **Monitor Costs** - Track and optimize spending

---

**This implementation guide provides everything you need to deploy and manage the Ghostbusters AI microservices platform on GKE while maintaining strict cost control!** 🚀

**Ready to proceed with deployment? Run the deployment script and let's build something amazing!** 💪
