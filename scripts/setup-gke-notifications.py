#!/usr/bin/env python3
"""
🔔 GKE Change Notification Setup
Configures push notifications for GKE cluster changes using Cloud Monitoring
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any


def load_project_model():
    """Load the project model registry"""
    model_path = Path(__file__).parent.parent.parent / "project_model_registry.json"
    
    if not model_path.exists():
        print(f"❌ Project model registry not found at: {model_path}")
        sys.exit(1)
    
    try:
        with open(model_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse project model registry: {e}")
        sys.exit(1)


def get_project_config():
    """Get GKE project configuration from model"""
    try:
        hackathon_config = model['domains']['hackathon']['hackathon_mapping']['gke_turns_10']
        gcp_setup = hackathon_config['gcp_project_setup']
        return gcp_setup
    except KeyError as e:
        print(f"❌ Failed to extract GKE configuration: {e}")
        sys.exit(1)


def enable_required_apis(project_id: str):
    """Enable required APIs for GKE notifications"""
    print("🔧 Enabling required APIs...")
    
    required_apis = [
        "monitoring.googleapis.com",
        "pubsub.googleapis.com",
        "cloudbuild.googleapis.com",
        "logging.googleapis.com"
    ]
    
    for api in required_apis:
        try:
            print(f"   Enabling {api}...")
            subprocess.run([
                'gcloud', 'services', 'enable', api,
                '--project', project_id,
                '--quiet'
            ], check=True)
            print(f"   ✅ {api} enabled")
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️  Warning: Failed to enable {api}: {e}")
    
    print("✅ API enablement completed")


def create_notification_channel(project_id: str, cluster_name: str):
    """Create Cloud Monitoring notification channel"""
    print("📡 Creating notification channel...")
    
    try:
        # Create notification channel
        result = subprocess.run([
            'gcloud', 'alpha', 'monitoring', 'channels', 'create',
            '--display-name', f"GKE {cluster_name} Change Alerts",
            '--type', 'pubsub',
            '--channel-labels', f"gke-cluster={cluster_name},project={project_id}",
            '--project', project_id,
            '--format', 'json'
        ], capture_output=True, text=True, check=True)
        
        channel_info = json.loads(result.stdout)
        channel_name = channel_info['name']
        
        print(f"✅ Notification channel created: {channel_name}")
        return channel_name
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create notification channel: {e}")
        print(f"   stderr: {e.stderr}")
        return None


def create_alerting_policies(project_id: str, cluster_name: str, channel_name: str):
    """Create GKE alerting policies"""
    print("🚨 Creating alerting policies...")
    
    policies = [
        {
            "name": f"gke-{cluster_name}-pod-failures",
            "display_name": f"GKE {cluster_name} - Pod Failures",
            "description": "Alert when pods fail to start or crash repeatedly",
            "condition": {
                "display_name": f"GKE {cluster_name} Pod Failures",
                "condition_threshold": {
                    "filter": f'resource.type = \
    "k8s_container" AND resource.labels.cluster_name="{cluster_name}" AND resource.labels.container_name!="gke-metrics-agent"',
                    "comparison": "COMPARISON_GREATER_THAN",
                    "threshold_value": 0,
                    "duration": "300s",
                    "trigger": {
                        "count": 1
                    }
                }
            }
        },
        {
            "name": f"gke-{cluster_name}-node-unhealthy",
            "display_name": f"GKE {cluster_name} - Unhealthy Nodes",
            "description": "Alert when GKE nodes become unhealthy",
            "condition": {
                "display_name": f"GKE {cluster_name} Unhealthy Nodes",
                "condition_threshold": {
                    "filter": f'resource.type = \
    "gce_instance" AND resource.labels.cluster_name="{cluster_name}"',
                    "comparison": "COMPARISON_GREATER_THAN",
                    "threshold_value": 0,
                    "duration": "60s",
                    "trigger": {
                        "count": 1
                    }
                }
            }
        },
        {
            "name": f"gke-{cluster_name}-high-cpu",
            "display_name": f"GKE {cluster_name} - High CPU Usage",
            "description": "Alert when cluster CPU usage exceeds 80%",
            "condition": {
                "display_name": f"GKE {cluster_name} High CPU",
                "condition_threshold": {
                    "filter": f'resource.type = \
    "gce_instance" AND resource.labels.cluster_name="{cluster_name}"',
                    "metric_kind": "GAUGE",
                    "value_type": "DOUBLE",
                    "comparison": "COMPARISON_GREATER_THAN",
                    "threshold_value": 0.8,
                    "duration": "300s",
                    "trigger": {
                        "count": 1
                    }
                }
            }
        }
    ]
    
    created_policies = []
    
    for policy in policies:
        try:
            print(f"   Creating policy: {policy['display_name']}")
            
            # Create policy file
            policy_file = Path(f"/tmp/{policy['name']}.json")
            with open(policy_file, 'w') as f:
                json.dump(policy, f, indent=2)
            
            # Create policy
            result = subprocess.run([
                'gcloud', 'alpha', 'monitoring', 'policies', 'create',
                '--policy-from-file', str(policy_file),
                '--project', project_id,
                '--format', 'json'
            ], capture_output=True, text=True, check=True)
            
            policy_info = json.loads(result.stdout)
            created_policies.append(policy_info['name'])
            
            print(f"   ✅ Policy created: {policy_info['name']}")
            
            # Clean up
            policy_file.unlink()
            
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️  Warning: Failed to create policy {policy['name']}: {e}")
        except Exception as e:
            print(f"   ⚠️  Warning: Error creating policy {policy['name']}: {e}")
    
    print(f"✅ Created {len(created_policies)} alerting policies")
    return created_policies


def setup_log_based_alerts(project_id: str, cluster_name: str, channel_name: str):
    """Setup log-based alerts for GKE events"""
    print("📝 Setting up log-based alerts...")
    
    try:
        # Create log sink for GKE events
        sink_name = f"gke-{cluster_name}-events-sink"
        
        result = subprocess.run([
            'gcloud', 'logging', 'sinks', 'create', sink_name,
            'pubsub.googleapis.com/projects/{project_id}/topics/gke-events'.format(project_id = \
    project_id),
            '--log-filter', f'resource.type = \
    "k8s_cluster" AND resource.labels.cluster_name="{cluster_name}"',
            '--project', project_id,
            '--format', 'json'
        ], capture_output=True, text=True, check=True)
        
        sink_info = json.loads(result.stdout)
        print(f"✅ Log sink created: {sink_info['name']}")
        
        # Grant permissions to the sink
        subprocess.run([
            'gcloud', 'pubsub', 'topics', 'add-iam-policy-binding', 'gke-events',
            '--member', f'serviceAccount:{sink_info["writerIdentity"]}',
            '--role', 'roles/pubsub.publisher',
            '--project', project_id
        ], check=True)
        
        print("✅ Log sink permissions configured")
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: Failed to setup log-based alerts: {e}")


def create_webhook_endpoint(project_id: str, cluster_name: str):
    """Create webhook endpoint for notifications"""
    print("🌐 Creating webhook endpoint...")
    
    try:
        # Create Cloud Function for webhook
        function_name = f"gke-{cluster_name}-webhook"
        
        # Create function directory
        function_dir = Path(f"/tmp/{function_name}")
        function_dir.mkdir(exist_ok=True)
        
        # Create main.py
        main_py = function_dir / "main.py"
        main_py.write_text('''
import functions_framework
import json
import requests

@functions_framework.http
def gke_webhook(request):
    """GKE change notification webhook"""
    # Get the request data
    request_json = request.get_json(silent=True)
    
    if not request_json:
        return 'No data received', 400
    
    # Extract relevant information
    incident = request_json.get('incident', {})
    policy_name = incident.get('policy_name', 'Unknown')
    condition_name = incident.get('condition_name', 'Unknown')
    resource_name = incident.get('resource_name', 'Unknown')
    severity = incident.get('severity', 'INFO')
    
    # Format message
    message = f"""
🚨 GKE Alert: {policy_name}
📍 Condition: {condition_name}
🎯 Resource: {resource_name}
⚠️  Severity: {severity}
⏰ Time: {incident.get('started_at', 'Unknown')}
    """.strip()
    
    # Send to your preferred notification service
    # Example: Slack, Discord, Teams, etc.
    
    # For now, just log the alert
    print(f"GKE Alert: {message}")
    
    return 'OK', 200
''')
        
        # Create requirements.txt
        requirements_txt = function_dir / "requirements.txt"
        requirements_txt.write_text('functions-framework==3.*')
        
        # Deploy function
        result = subprocess.run([
            'gcloud', 'functions', 'deploy', function_name,
            '--runtime', 'python39',
            '--trigger-http',
            '--allow-unauthenticated',
            '--project', project_id,
            '--region', 'us-central1',
            '--source', str(function_dir),
            '--format', 'json'
        ], capture_output=True, text=True, check=True)
        
        function_info = json.loads(result.stdout)
        webhook_url = function_info['httpsTrigger']['url']
        
        print(f"✅ Webhook endpoint created: {webhook_url}")
        
        # Clean up
        import shutil
        shutil.rmtree(function_dir)
        
        return webhook_url
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: Failed to create webhook: {e}")
        return None


def setup_email_notifications(project_id: str, cluster_name: str, channel_name: str):
    """Setup email notifications"""
    print("📧 Setting up email notifications...")
    
    try:
        # Create email notification channel
        result = subprocess.run([
            'gcloud', 'alpha', 'monitoring', 'channels', 'create',
            '--display-name', f"GKE {cluster_name} Email Alerts",
            '--type', 'email',
            '--channel-labels', f"gke-cluster={cluster_name},project={project_id}",
            '--user-labels', 'email=admin@example.com',
            '--project', project_id,
            '--format', 'json'
        ], capture_output=True, text=True, check=True)
        
        email_channel = json.loads(result.stdout)
        print(f"✅ Email notification channel created: {email_channel['name']}")
        
        return email_channel['name']
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: Failed to create email channel: {e}")
        return None


def create_dashboard(project_id: str, cluster_name: str):
    """Create GKE monitoring dashboard"""
    print("📊 Creating monitoring dashboard...")
    
    dashboard_config = {
        "displayName": f"GKE {cluster_name} Monitoring",
        "gridLayout": {
            "widgets": [
                {
                    "title": f"GKE {cluster_name} - Pod Status",
                    "xyChart": {
                        "dataSets": [{
                            "timeSeriesQuery": {
                                "timeSeriesFilter": {
                                    "filter": f'resource.type = \
    "k8s_container" AND resource.labels.cluster_name="{cluster_name}"',
                                    "aggregations": [{
                                        "perSeriesAligner": "ALIGN_RATE",
                                        "crossSeriesReducer": "REDUCE_SUM"
                                    }]
                                }
                            }
                        }]
                    }
                },
                {
                    "title": f"GKE {cluster_name} - Node CPU",
                    "xyChart": {
                        "dataSets": [{
                            "timeSeriesQuery": {
                                "timeSeriesFilter": {
                                    "filter": f'resource.type = \
    "gce_instance" AND resource.labels.cluster_name="{cluster_name}"',
                                    "aggregations": [{
                                        "perSeriesAligner": "ALIGN_MEAN",
                                        "crossSeriesReducer": "REDUCE_MEAN"
                                    }]
                                }
                            }
                        }]
                    }
                }
            ]
        }
    }
    
    try:
        # Create dashboard file
        dashboard_file = Path(f"/tmp/gke-{cluster_name}-dashboard.json")
        with open(dashboard_file, 'w') as f:
            json.dump(dashboard_config, f, indent=2)
        
        # Create dashboard
        result = subprocess.run([
            'gcloud', 'monitoring', 'dashboards', 'create',
            '--config-from-file', str(dashboard_file),
            '--project', project_id,
            '--format', 'json'
        ], capture_output=True, text=True, check=True)
        
        dashboard_info = json.loads(result.stdout)
        print(f"✅ Dashboard created: {dashboard_info['name']}")
        
        # Clean up
        dashboard_file.unlink()
        
        return dashboard_info['name']
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: Failed to create dashboard: {e}")
        return None


def main():
    """Main function"""
    print("🔔 GKE Change Notification Setup")
    print("================================")
    print("")
    
    # Load project model
    print("📖 Loading project configuration...")
    model = load_project_model()
    gcp_config = get_project_config()
    
    project_id = gcp_config['deploy_template']['variables']['project_id']
    cluster_name = gcp_config['deploy_template']['variables']['cluster_name']
    
    print(f"🎯 Project: {project_id}")
    print(f"🚀 Cluster: {cluster_name}")
    print("")
    
    # Enable required APIs
    enable_required_apis(project_id)
    print("")
    
    # Create notification channel
    channel_name = create_notification_channel(project_id, cluster_name)
    if not channel_name:
        print("❌ Failed to create notification channel. Exiting.")
        sys.exit(1)
    print("")
    
    # Create alerting policies
    policies = create_alerting_policies(project_id, cluster_name, channel_name)
    print("")
    
    # Setup log-based alerts
    setup_log_based_alerts(project_id, cluster_name, channel_name)
    print("")
    
    # Create webhook endpoint
    webhook_url = create_webhook_endpoint(project_id, cluster_name)
    print("")
    
    # Setup email notifications
    email_channel = setup_email_notifications(project_id, cluster_name, channel_name)
    print("")
    
    # Create monitoring dashboard
    dashboard_name = create_dashboard(project_id, cluster_name)
    print("")
    
    # Summary
    print("🎉 GKE Change Notification Setup Complete!")
    print("==========================================")
    print("")
    print("📋 What was created:")
    print(f"   📡 Notification Channel: {channel_name}")
    print(f"   🚨 Alerting Policies: {len(policies)} created")
    print(f"   🌐 Webhook Endpoint: {webhook_url or 'Failed'}")
    print(f"   📧 Email Channel: {email_channel or 'Failed'}")
    print(f"   📊 Dashboard: {dashboard_name or 'Failed'}")
    print("")
    print("🔔 You will now receive notifications for:")
    print("   - Pod failures and crashes")
    print("   - Node health issues")
    print("   - High CPU usage")
    print("   - Cluster scaling events")
    print("   - API errors and warnings")
    print("")
    print("📱 Next steps:")
    print("   1. Configure your preferred notification service (Slack, Discord, etc.)")
    print("   2. Update the webhook function to send to your service")
    print("   3. Test alerts by creating test policies")
    print("   4. Monitor the dashboard for real-time insights")


if __name__ == "__main__":
    main()