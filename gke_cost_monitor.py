#!/usr/bin/env python3
"""
💰 GKE Cost Monitor

Monitor and control costs for GKE hackathon implementation.
Integrates with existing GCP cost control system.
"""

import json
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


class GKECostMonitor:
    """Monitor and control GKE costs for hackathon implementation"""

    def __init__(self):
        """Initialize the GKE cost monitor"""
        self.cluster_name = "ghostbusters-hackathon"
        self.project_id = self._get_project_id()
        self.billing_account = self._get_billing_account()
        
        # Cost thresholds for different phases
        self.cost_thresholds = {
            "development": {
                "daily": 0.20,      # $0.20/day = ~$6/month
                "weekly": 1.40,     # $1.40/week
                "monthly": 5.00     # $5/month
            },
            "testing": {
                "daily": 0.50,      # $0.50/day = ~$15/month
                "weekly": 3.50,     # $3.50/week
                "monthly": 15.00    # $15/month
            },
            "demo": {
                "daily": 0.83,      # $0.83/day = ~$25/month
                "weekly": 5.83,     # $5.83/week
                "monthly": 25.00    # $25/month
            }
        }
        
        # Current phase (start with development)
        self.current_phase = "development"
        
        # Data directory for cost reports
        self.data_dir = Path("cost_reports")
        self.data_dir.mkdir(exist_ok=True)

    def _get_project_id(self) -> str:
        """Get current GCP project ID"""
        try:
            result = subprocess.run(
                ["gcloud", "config", "get-value", "project"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except Exception as e:
            print(f"❌ Failed to get project ID: {e}")
            return "unknown"

    def _get_billing_account(self) -> str:
        """Get current GCP billing account"""
        try:
            result = subprocess.run(
                ["gcloud", "billing", "accounts", "list", "--format=value(name)"],
                capture_output=True,
                text=True,
                check=True
            )
            billing_accounts = result.stdout.strip().split('\n')
            if billing_accounts and billing_accounts[0]:
                return billing_accounts[0].split('/')[-1]
            return "unknown"
        except Exception as e:
            print(f"❌ Failed to get billing account: {e}")
            return "unknown"

    def get_gke_cluster_status(self) -> Dict[str, Any]:
        """Get current GKE cluster status"""
        try:
            result = subprocess.run([
                "gcloud", "container", "clusters", "describe", self.cluster_name,
                "--format=json"
            ], capture_output=True, text=True, check=True)
            
            cluster_info = json.loads(result.stdout)
            
            return {
                "name": cluster_info.get("name"),
                "status": cluster_info.get("status"),
                "node_count": cluster_info.get("currentNodeCount", 0),
                "node_pools": len(cluster_info.get("nodePools", [])),
                "machine_type": cluster_info.get( \
    "nodePools", [{}])[0].get("config", {}).get("machineType", "unknown"),
                "disk_size_gb": cluster_info.get( \
    "nodePools", [{}])[0].get("config", {}).get("diskSizeGb", 0),
                "preemptible": cluster_info.get( \
    "nodePools", [{}])[0].get("config", {}).get("preemptible", False)
            }
        except Exception as e:
            print(f"❌ Failed to get cluster status: {e}")
            return {}

    def get_gke_pod_status(self) -> Dict[str, Any]:
        """Get current GKE pod status and resource usage"""
        try:
            # Get pod information
            result = subprocess.run([
                "kubectl", "get", "pods", "--all-namespaces", "--output=json"
            ], capture_output=True, text=True, check=True)
            
            pods_info = json.loads(result.stdout)
            
            # Get resource usage
            result = subprocess.run([
                "kubectl", "top", "pods", "--all-namespaces", "--output=json"
            ], capture_output=True, text=True, check=True)
            
            try:
                usage_info = json.loads(result.stdout)
            except Exception:
                usage_info = {"items": []}
            
            # Analyze pod status
            total_pods = len(pods_info.get("items", []))
            running_pods = sum(1 for pod in pods_info.get("items", []) 
                             if pod.get("status", {}).get("phase") == "Running")
            pending_pods = sum(1 for pod in pods_info.get("items", []) 
                             if pod.get("status", {}).get("phase") == "Pending")
            failed_pods = sum(1 for pod in pods_info.get("items", []) 
                            if pod.get("status", {}).get("phase") == "Failed")
            
            # Calculate resource usage
            total_cpu = 0
            total_memory = 0
            
            for usage in usage_info.get("items", []):
                cpu_str = usage.get("usage", {}).get("cpu", "0m")
                memory_str = usage.get("usage", {}).get("memory", "0Mi")
                
                            # Convert CPU to millicores
            if cpu_str.endswith('m'):
                total_cpu += int(cpu_str[:-1])
            else:
                total_cpu += int(float(cpu_str) * 1000)

            # Convert memory to Mi
            if memory_str.endswith('Ki'):
                total_memory += int(memory_str[:-2]) // 1024
            elif memory_str.endswith('Mi'):
                total_memory += int(memory_str[:-2])
            elif memory_str.endswith('Gi'):
                total_memory += int(float(memory_str[:-2]) * 1024)
            
            return {
                "total_pods": total_pods,
                "running_pods": running_pods,
                "pending_pods": pending_pods,
                "failed_pods": failed_pods,
                "total_cpu_millicores": total_cpu,
                "total_memory_mi": total_memory,
                "cpu_utilization_percent": min( \
    100, (total_cpu / (total_pods * 100)) * 100) if total_pods > 0 else 0,
                "memory_utilization_percent": min( \
    100, (total_memory / (total_pods * 256)) * 100) if total_pods > 0 else 0
            }
        except Exception as e:
            print(f"❌ Failed to get pod status: {e}")
            return {}

    def estimate_gke_costs(self) -> Dict[str, float]:
        """Estimate current GKE costs based on resource usage"""
        try:
            cluster_status = self.get_gke_cluster_status()
            pod_status = self.get_gke_pod_status()
            
            if not cluster_status or not pod_status:
                return {}
            
            # Cost estimates (approximate GCP pricing)
            node_count = cluster_status.get("node_count", 0)
            machine_type = cluster_status.get("machine_type", "e2-micro")
            preemptible = cluster_status.get("preemptible", False)
            
            # Machine type costs per month (approximate)
            machine_costs = {
                "e2-micro": 4.50,      # $4.50/month
                "e2-small": 9.00,      # $9.00/month
                "e2-medium": 18.00,    # $18.00/month
                "e2-standard-2": 36.00, # $36.00/month
            }
            
            # Get base cost for machine type
            base_cost = machine_costs.get(machine_type, 4.50)
            
            # Apply preemptible discount (50% off)
            if preemptible:
                base_cost *= 0.5
            
            # Calculate daily cost
            daily_cost = (base_cost * node_count) / 30
            
            # Add storage costs (approximate)
            disk_size_gb = cluster_status.get("disk_size_gb", 20)
            storage_cost_per_gb_month = 0.08  # $0.08/GB/month
            daily_storage_cost = (disk_size_gb * storage_cost_per_gb_month) / 30
            
            # Add network costs (approximate)
            daily_network_cost = 0.10  # $0.10/day base network cost
            
            total_daily_cost = daily_cost + daily_storage_cost + daily_network_cost
            
            return {
                "daily_cost": round(total_daily_cost, 2),
                "weekly_cost": round(total_daily_cost * 7, 2),
                "monthly_cost": round(total_daily_cost * 30, 2),
                "node_cost": round(daily_cost, 2),
                "storage_cost": round(daily_storage_cost, 2),
                "network_cost": round(daily_network_cost, 2),
                "preemptible_savings": "50%" if preemptible else "0%"
            }
        except Exception as e:
            print(f"❌ Failed to estimate costs: {e}")
            return {}

    def check_cost_thresholds(self) -> Dict[str, Any]:
        """Check if current costs exceed thresholds"""
        costs = self.estimate_gke_costs()
        if not costs:
            return {"error": "Could not estimate costs"}
        
        current_phase = self.current_phase
        thresholds = self.cost_thresholds.get(current_phase, {})
        
        alerts = []
        warnings = []
        
        # Check daily costs
        daily_cost = costs.get("daily_cost", 0)
        daily_threshold = thresholds.get("daily", float('inf'))
        
        if daily_cost > daily_threshold:
            alerts.append(f"🚨 Daily cost ${daily_cost} exceeds threshold ${daily_threshold}")
        elif daily_cost > daily_threshold * 0.8:
            warnings.append(f"⚠️ Daily cost ${daily_cost} approaching threshold ${daily_threshold}")
        
        # Check weekly costs
        weekly_cost = costs.get("weekly_cost", 0)
        weekly_threshold = thresholds.get("weekly", float('inf'))
        
        if weekly_cost > weekly_threshold:
            alerts.append(f"🚨 Weekly cost ${weekly_cost} exceeds threshold ${weekly_threshold}")
        elif weekly_cost > weekly_threshold * 0.8:
            warnings.append( \
    f"⚠️ Weekly cost ${weekly_cost} approaching threshold ${weekly_threshold}")
        
        # Check monthly costs
        monthly_cost = costs.get("monthly_cost", 0)
        monthly_threshold = thresholds.get("monthly", float('inf'))
        
        if monthly_cost > monthly_threshold:
            alerts.append(f"🚨 Monthly cost ${monthly_cost} exceeds threshold ${monthly_threshold}")
        elif monthly_cost > monthly_threshold * 0.8:
            warnings.append( \
    f"⚠️ Monthly cost ${monthly_cost} approaching threshold ${monthly_threshold}")
        
        return {
            "current_phase": current_phase,
            "costs": costs,
            "thresholds": thresholds,
            "alerts": alerts,
            "warnings": warnings,
            "within_budget": len(alerts) == 0,
            "status": "critical" if alerts else "warning" if warnings else "healthy"
        }

    def get_cost_optimization_recommendations(self) -> List[str]:
        """Get recommendations for cost optimization"""
        recommendations = []
        
        cluster_status = self.get_gke_cluster_status()
        pod_status = self.get_gke_pod_status()
        
        if not cluster_status or not pod_status:
            return ["Unable to analyze cluster status"]
        
        # Check machine type
        machine_type = cluster_status.get("machine_type", "")
        if machine_type != "e2-micro":
            recommendations.append( \
    "💡 Consider using e2-micro machine type for development (cheaper)")
        
        # Check preemptible instances
        if not cluster_status.get("preemptible", False):
            recommendations.append("💡 Enable preemptible instances for 50% cost savings")
        
        # Check node count
        node_count = cluster_status.get("node_count", 0)
        if node_count > 2:
            recommendations.append("💡 Consider reducing node count during development")
        
        # Check pod resource usage
        cpu_util = pod_status.get("cpu_utilization_percent", 0)
        memory_util = pod_status.get("memory_utilization_percent", 0)
        
        if cpu_util < 30:
            recommendations.append("💡 CPU utilization is low - consider reducing resource requests")
        
        if memory_util < 40:
            recommendations.append( \
    "💡 Memory utilization is low - consider reducing resource requests")
        
        # Check for failed pods
        failed_pods = pod_status.get("failed_pods", 0)
        if failed_pods > 0:
            recommendations.append("🔧 Fix failed pods to avoid resource waste")
        
        if not recommendations:
            recommendations.append("✅ Current configuration is cost-optimized")
        
        return recommendations

    def generate_cost_report(self) -> str:
        """Generate comprehensive cost report"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Get all cost information
        cluster_status = self.get_gke_cluster_status()
        pod_status = self.get_gke_pod_status()
        costs = self.estimate_gke_costs()
        threshold_check = self.check_cost_thresholds()
        recommendations = self.get_cost_optimization_recommendations()
        
        # Generate report
        report = f"""# 💰 GKE Cost Report
Generated: {timestamp}

## 📋 Project Information
- **Project ID**: {self.project_id}
- **Billing Account**: {self.billing_account}
- **Cluster Name**: {self.cluster_name}
- **Current Phase**: {self.current_phase}

## 🏗️ Cluster Status
- **Status**: {cluster_status.get('status', 'Unknown')}
- **Node Count**: {cluster_status.get('node_count', 0)}
- **Machine Type**: {cluster_status.get('machine_type', 'Unknown')}
- **Disk Size**: {cluster_status.get('disk_size_gb', 0)} GB
- **Preemptible**: {'Yes' if cluster_status.get('preemptible') else 'No'}

## 📊 Pod Status
- **Total Pods**: {pod_status.get('total_pods', 0)}
- **Running Pods**: {pod_status.get('running_pods', 0)}
- **Pending Pods**: {pod_status.get('pending_pods', 0)}
- **Failed Pods**: {pod_status.get('failed_pods', 0)}
- **CPU Utilization**: {pod_status.get('cpu_utilization_percent', 0):.1f}%
- **Memory Utilization**: {pod_status.get('memory_utilization_percent', 0):.1f}%

## 💰 Cost Analysis
- **Daily Cost**: ${costs.get('daily_cost', 0):.2f}
- **Weekly Cost**: ${costs.get('weekly_cost', 0):.2f}
- **Monthly Cost**: ${costs.get('monthly_cost', 0):.2f}
- **Node Cost**: ${costs.get('node_cost', 0):.2f}/day
- **Storage Cost**: ${costs.get('storage_cost', 0):.2f}/day
- **Network Cost**: ${costs.get('network_cost', 0):.2f}/day
- **Preemptible Savings**: {costs.get('preemptible_savings', '0%')}

## 🎯 Cost Thresholds
- **Phase**: {threshold_check.get('current_phase', 'Unknown')}
- **Daily Threshold**: ${threshold_check.get('thresholds', {}).get('daily', 0):.2f}
- **Weekly Threshold**: ${threshold_check.get('thresholds', {}).get('weekly', 0):.2f}
- **Monthly Threshold**: ${threshold_check.get('thresholds', {}).get('monthly', 0):.2f}
- **Status**: {threshold_check.get('status', 'Unknown').upper()}

## 🚨 Alerts & Warnings
"""
        
        # Add alerts
        for alert in threshold_check.get('alerts', []):
            report += f"- {alert}\n"
        
        # Add warnings
        for warning in threshold_check.get('warnings', []):
            report += f"- {warning}\n"
        
        if not threshold_check.get('alerts') and not threshold_check.get('warnings'):
            report += "- ✅ All costs within budget\n"
        
        # Add recommendations
        report += f"""
## 💡 Cost Optimization Recommendations
"""
        
        for rec in recommendations:
            report += f"- {rec}\n"
        
        # Add footer
        report += f"""
---
**Report Status**: {threshold_check.get('status', 'Unknown').upper()}
**Budget Status**: {'✅ Within Budget' if threshold_check.get( \
    'within_budget') else '❌ Over Budget'}
**Generated**: {timestamp}
"""
        
        return report

    def save_cost_report(self, report: str) -> str:
        """Save cost report to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gke_cost_report_{timestamp}.md"
        filepath = self.data_dir / filename
        
        try:
            with open(filepath, 'w') as f:
                f.write(report)
            
            print(f"💾 Cost report saved to: {filepath}")
            return str(filepath)
        except Exception as e:
            print(f"❌ Failed to save report: {e}")
            return ""

    def set_phase(self, phase: str) -> bool:
        """Set current development phase"""
        if phase in self.cost_thresholds:
            self.current_phase = phase
            print(f"✅ Set phase to: {phase}")
            return True
        else:
            print(f"❌ Invalid phase: {phase}. Valid phases: {list(self.cost_thresholds.keys())}")
            return False

    def emergency_cost_control(self) -> bool:
        """Emergency cost control - scale down everything"""
        try:
            print("🚨 EMERGENCY COST CONTROL ACTIVATED!")
            
            # Scale down all deployments
            result = subprocess.run([
                "kubectl", "scale", "deployment", "--all", "--replicas=1"
            ], capture_output=True, text=True, check=True)
            
            print("✅ Scaled down all deployments to 1 replica")
            
            # Delete HPA (Horizontal Pod Autoscaler)
            result = subprocess.run([
                "kubectl", "delete", "hpa", "--all"
            ], capture_output=True, text=True, check=True)
            
            print("✅ Disabled all auto-scaling")
            
            # Scale down cluster to minimum nodes
            result = subprocess.run([
                "gcloud", "container", "clusters", "update", self.cluster_name,
                "--node-pool", "default-pool",
                "--min-nodes", "1",
                "--max-nodes", "2"
            ], capture_output=True, text=True, check=True)
            
            print("✅ Scaled down cluster to 1-2 nodes")
            
            return True
        except Exception as e:
            print(f"❌ Emergency cost control failed: {e}")
            return False

    def run_cost_monitoring(self, interval_minutes: int = 60) -> None:
        """Run continuous cost monitoring"""
        print(f"💰 Starting GKE cost monitoring (checking every {interval_minutes} minutes)")
        print(f"📊 Current phase: {self.current_phase}")
        
        try:
            while True:
                # Generate and save report
                report = self.generate_cost_report()
                self.save_cost_report(report)
                
                # Check thresholds
                threshold_check = self.check_cost_thresholds()
                
                # Display status
                status_emoji = {
                    "healthy": "✅",
                    "warning": "⚠️",
                    "critical": "🚨"
                }
                
                status = threshold_check.get("status", "unknown")
                emoji = status_emoji.get(status, "❓")
                
                print(f"{emoji} Cost Status: {status.upper()}")
                print(f"💰 Daily Cost: ${threshold_check.get('costs', {}).get('daily_cost', 0):.2f}")
                
                # Show alerts
                for alert in threshold_check.get("alerts", []):
                    print(f"  {alert}")
                
                # Emergency control if critical
                if status == "critical":
                    print("🚨 CRITICAL COSTS DETECTED!")
                    response = input("Activate emergency cost control? (y/N): ")
                    if response.lower() == 'y':
                        self.emergency_cost_control()
                
                print(f"⏰ Next check in {interval_minutes} minutes...")
                time.sleep(interval_minutes * 60)
                
        except KeyboardInterrupt:
            print("\n🛑 Cost monitoring stopped by user")
        except Exception as e:
            print(f"❌ Cost monitoring failed: {e}")


def main():
    """Main function for GKE cost monitoring"""
    print("💰 GKE Cost Monitor")
    print("=" * 50)
    
    monitor = GKECostMonitor()
    
    # Check if cluster exists
    cluster_status = monitor.get_gke_cluster_status()
    if not cluster_status:
        print("❌ GKE cluster not found or not accessible")
        print("💡 Make sure you have:")
        print("   - gcloud CLI configured")
        print("   - kubectl configured for the cluster")
        print("   - Proper permissions")
        return
    
    print(f"✅ Connected to GKE cluster: {cluster_status.get('name', 'Unknown')}")
    
    # Generate initial report
    print("📊 Generating initial cost report...")
    report = monitor.generate_cost_report()
    monitor.save_cost_report(report)
    
    # Check current status
    threshold_check = monitor.check_cost_thresholds()
    print(f"💰 Current cost status: {threshold_check.get('status', 'Unknown').upper()}")
    
    # Show recommendations
    recommendations = monitor.get_cost_optimization_recommendations()
    print("\n💡 Cost optimization recommendations:")
    for rec in recommendations:
        print(f"  {rec}")
    
    # Interactive mode
    print("\n🎮 Interactive Mode:")
    print("  1. Generate cost report")
    print("  2. Check cost thresholds")
    print("  3. Set development phase")
    print("  4. Start continuous monitoring")
    print("  5. Emergency cost control")
    print("  6. Exit")
    
    while True:
        try:
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == "1":
                report = monitor.generate_cost_report()
                monitor.save_cost_report(report)
                print("✅ Cost report generated and saved")
                
            elif choice == "2":
                threshold_check = monitor.check_cost_thresholds()
                print(f"💰 Cost Status: {threshold_check.get('status', 'Unknown').upper()}")
                for alert in threshold_check.get("alerts", []):
                    print(f"  {alert}")
                for warning in threshold_check.get("warnings", []):
                    print(f"  {warning}")
                    
            elif choice == "3":
                print(f"Current phase: {monitor.current_phase}")
                print(f"Available phases: {list(monitor.cost_thresholds.keys())}")
                phase = input("Enter new phase: ").strip()
                monitor.set_phase(phase)
                
            elif choice == "4":
                interval = input("Check interval in minutes (default 60): ").strip()
                try:
                    interval_minutes = int(interval) if interval else 60
                    monitor.run_cost_monitoring(interval_minutes)
                except ValueError:
                    print("❌ Invalid interval, using default 60 minutes")
                    monitor.run_cost_monitoring()
                    
            elif choice == "5":
                response = input("⚠️ This will scale down everything. Continue? (y/N): ")
                if response.lower() == 'y':
                    monitor.emergency_cost_control()
                    
            elif choice == "6":
                print("👋 Exiting GKE Cost Monitor")
                break
                
            else:
                print("❌ Invalid option, please select 1-6")
                
        except KeyboardInterrupt:
            print("\n👋 Exiting GKE Cost Monitor")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()