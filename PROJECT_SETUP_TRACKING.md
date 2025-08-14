# 🚀 GKE Hackathon Project Setup Tracking

**Project:** Ghostbusters AI Microservices Platform on GKE  
**Year:** 2025  
**Status:** 🔄 **SETUP IN PROGRESS**  
**Tracking:** Complete API and resource tracking  

---

## 🎯 **Project Setup Overview**

### **New GCP Project:**
- **Project ID:** `ghostbusters-hackathon-2025`
- **Project Name:** "Ghostbusters AI Hackathon 2025"
- **Purpose:** Dedicated tracking for GKE hackathon costs and APIs
- **Billing:** Separate billing account for cost isolation

### **Setup Status:**
- ❌ **Project Creation** - Not started
- ❌ **API Enablement** - Not started  
- ❌ **Billing Setup** - Not started
- ❌ **IAM Configuration** - Not started
- ❌ **GKE Deployment** - Not started

---

## 🔌 **Required APIs (Explicit List)**

### **Core APIs for GKE Hackathon:**

#### **1. Container Engine API**
- **API Name:** `container.googleapis.com`
- **Purpose:** GKE cluster creation and management
- **Required:** ✅ **CRITICAL**
- **Cost Impact:** High (GKE cluster costs)
- **Status:** ❌ Not enabled

#### **2. Compute Engine API**
- **API Name:** `compute.googleapis.com`
- **Purpose:** VM instances, networking, disks
- **Required:** ✅ **CRITICAL**
- **Cost Impact:** High (VM instance costs)
- **Status:** ❌ Not enabled

#### **3. Cloud Monitoring API**
- **API Name:** `monitoring.googleapis.com`
- **Purpose:** Metrics, alerts, dashboards
- **Required:** ✅ **CRITICAL**
- **Cost Impact:** Low (monitoring costs)
- **Status:** ❌ Not enabled

#### **4. Cloud Logging API**
- **API Name:** `logging.googleapis.com`
- **Purpose:** Log aggregation and analysis
- **Required:** ✅ **CRITICAL**
- **Cost Impact:** Low (logging costs)
- **Status:** ❌ Not enabled

#### **5. Resource Manager API**
- **API Name:** `cloudresourcemanager.googleapis.com`
- **Purpose:** Project and resource management
- **Required:** ✅ **CRITICAL**
- **Cost Impact:** None (free)
- **Status:** ❌ Not enabled

#### **6. IAM API**
- **API Name:** `iam.googleapis.com`
- **Purpose:** Identity and access management
- **Required:** ✅ **CRITICAL**
- **Cost Impact:** None (free)
- **Status:** ❌ Not enabled

---

## 🚫 **APIs We DON'T Need (Explicit Exclusion)**

### **Excluded APIs (Cost Control):**

#### **1. Cloud Functions API**
- **API Name:** `cloudfunctions.googleapis.com`
- **Reason:** Using GKE instead of serverless
- **Cost Impact:** Avoided (no function costs)
- **Status:** ❌ **EXPLICITLY DISABLED**

#### **2. Cloud Run API**
- **API Name:** `run.googleapis.com`
- **Reason:** Using GKE instead of Cloud Run
- **Cost Impact:** Avoided (no Cloud Run costs)
- **Status:** ❌ **EXPLICITLY DISABLED**

#### **3. Firestore API**
- **API Name:** `firestore.googleapis.com`
- **Reason:** Using local storage for hackathon
- **Cost Impact:** Avoided (no database costs)
- **Status:** ❌ **EXPLICITLY DISABLED**

#### **4. Pub/Sub API**
- **API Name:** `pubsub.googleapis.com`
- **Reason:** Not using messaging for hackathon
- **Cost Impact:** Avoided (no messaging costs)
- **Status:** ❌ **EXPLICITLY DISABLED**

#### **5. Cloud Storage API**
- **API Name:** `storage.googleapis.com`
- **Reason:** Using local storage for hackathon
- **Cost Impact:** Avoided (no storage costs)
- **Status:** ❌ **EXPLICITLY DISABLED**

---

## 💰 **Cost Tracking by API**

### **API Cost Impact Analysis:**

| API | Monthly Cost | Purpose | Required |
|-----|--------------|---------|----------|
| `container.googleapis.com` | $15-25 | GKE clusters | ✅ Critical |
| `compute.googleapis.com` | $10-20 | VM instances | ✅ Critical |
| `monitoring.googleapis.com` | $2-5 | Metrics & alerts | ✅ Critical |
| `logging.googleapis.com` | $1-3 | Log aggregation | ✅ Critical |
| `cloudresourcemanager.googleapis.com` | $0 | Project management | ✅ Critical |
| `iam.googleapis.com` | $0 | Access control | ✅ Critical |
| **TOTAL REQUIRED** | **$28-53** | **All hackathon needs** | **✅ Complete** |

### **APIs Avoided (Cost Savings):**
| API | Monthly Cost | Reason | Status |
|-----|--------------|---------|---------|
| `cloudfunctions.googleapis.com` | $18.72 | Using GKE instead | ❌ Disabled |
| `run.googleapis.com` | $2.66 | Using GKE instead | ❌ Disabled |
| `firestore.googleapis.com` | $0.56 | Using local storage | ❌ Disabled |
| `pubsub.googleapis.com` | $0.28 | Not needed | ❌ Disabled |
| `storage.googleapis.com` | $0.14 | Using local storage | ❌ Disabled |
| **TOTAL SAVINGS** | **$22.36** | **Avoided costs** | **✅ Saved** |

---

## 🔧 **Project Setup Commands**

### **Step 1: Create New Project**
```bash
# Create new project for 2025 hackathon
gcloud projects create ghostbusters-hackathon-2025 \
  --name="Ghostbusters AI Hackathon 2025" \
  --set-as-default

# Verify project creation
gcloud projects list --filter="project_id=ghostbusters-hackathon-2025"
```

### **Step 2: Set Billing Account**
```bash
# Link billing account (replace with your billing account ID)
gcloud billing projects link ghostbusters-hackathon-2025 \
  --billing-account=01F112-E73FD5-795507

# Verify billing link
gcloud billing projects describe ghostbusters-hackathon-2025
```

### **Step 3: Enable Required APIs**
```bash
# Enable ONLY the APIs we need
gcloud services enable \
  container.googleapis.com \
  compute.googleapis.com \
  monitoring.googleapis.com \
  logging.googleapis.com \
  cloudresourcemanager.googleapis.com \
  iam.googleapis.com

# Verify enabled APIs
gcloud services list --enabled --project=ghostbusters-hackathon-2025
```

### **Step 4: Verify API Status**
```bash
# Check all enabled APIs
gcloud services list --enabled --project=ghostbusters-hackathon-2025

# Check specific API status
gcloud services list --enabled --project=ghostbusters-hackathon-2025 \
  --filter="name:container.googleapis.com"

gcloud services list --enabled --project=ghostbusters-hackathon-2025 \
  --filter="name:compute.googleapis.com"
```

---

## 📊 **Setup Verification Checklist**

### **Project Creation:**
- [ ] **Project ID:** `ghostbusters-hackathon-2025` exists
- [ ] **Project Name:** "Ghostbusters AI Hackathon 2025" set
- [ ] **Project Status:** ACTIVE
- [ ] **Default Project:** Set for gcloud

### **Billing Setup:**
- [ ] **Billing Account:** Linked to project
- [ ] **Billing Status:** ACTIVE
- [ ] **Budget Alerts:** Configured for $25/month
- [ ] **Cost Monitoring:** Enabled

### **API Enablement:**
- [ ] **Container Engine API:** `container.googleapis.com` ✅
- [ ] **Compute Engine API:** `compute.googleapis.com` ✅
- [ ] **Cloud Monitoring API:** `monitoring.googleapis.com` ✅
- [ ] **Cloud Logging API:** `logging.googleapis.com` ✅
- [ ] **Resource Manager API:** `cloudresourcemanager.googleapis.com` ✅
- [ ] **IAM API:** `iam.googleapis.com` ✅

### **API Exclusion Verification:**
- [ ] **Cloud Functions API:** `cloudfunctions.googleapis.com` ❌
- [ ] **Cloud Run API:** `run.googleapis.com` ❌
- [ ] **Firestore API:** `firestore.googleapis.com` ❌
- [ ] **Pub/Sub API:** `pubsub.googleapis.com` ❌
- [ ] **Cloud Storage API:** `storage.googleapis.com` ❌

---

## 🚨 **Cost Control Setup**

### **Budget Configuration:**
```bash
# Create project budget
gcloud billing budgets create \
  --billing-account=01F112-E73FD5-795507 \
  --budget-amount=25.00USD \
  --budget-filter="project=ghostbusters-hackathon-2025" \
  --display-name="Ghostbusters Hackathon 2025 Budget"

# Verify budget creation
gcloud billing budgets list --billing-account=01F112-E73FD5-795507
```

### **Cost Alerts:**
```bash
# Set up cost threshold alerts
gcloud alpha monitoring policies create \
  --policy-from-file=cost-alert-policy.yaml \
  --project=ghostbusters-hackathon-2025
```

---

## 📝 **Setup Log**

### **Date:** [Current Date]
### **Setup By:** [Your Name]
### **Status:** 🔄 **IN PROGRESS**

#### **Completed Steps:**
- ❌ Project creation
- ❌ Billing setup
- ❌ API enablement
- ❌ Cost control configuration

#### **Next Steps:**
1. **Create new GCP project** `ghostbusters-hackathon-2025`
2. **Link billing account** for cost tracking
3. **Enable required APIs** (6 core APIs only)
4. **Verify API exclusions** (5 APIs explicitly disabled)
5. **Configure cost control** and budget alerts
6. **Update deployment scripts** with new project ID

---

## 🎯 **Success Criteria**

### **Setup Complete When:**
- ✅ **New project** `ghostbusters-hackathon-2025` exists and active
- ✅ **Billing linked** and active
- ✅ **6 required APIs** enabled and working
- ✅ **5 excluded APIs** explicitly disabled
- ✅ **Cost control** configured with $25/month budget
- ✅ **All configurations** updated with new project ID
- ✅ **Deployment ready** with clean project environment

---

**This tracking document ensures we're explicit about every API we enable and every cost we track for the 2025 hackathon!** 📝✅

**Ready to start the project setup process?** 🚀
