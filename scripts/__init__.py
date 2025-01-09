from typing import Dict, Any
import os
import boto3
import yaml

def load_aws_config() -> Dict[str, Any]:
    """Load AWS configuration from config file"""
    config_path = os.path.join('config', 'aws_config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_aws_client(service_name: str):
    """Get AWS client for specific service"""
    config = load_aws_config()
    return boto3.client(
        service_name,
        region_name=config['region'],
        aws_access_key_id=config['access_key_id'],
        aws_secret_access_key=config['secret_access_key']
    )

def get_eks_cluster_name() -> str:
    """Get EKS cluster name from config"""
    config = load_aws_config()
    return config['eks_cluster_name']