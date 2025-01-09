import boto3
import subprocess
import os
import time

def deploy_to_aws():
    """Deploy the application to AWS EKS"""
    
    # Initialize AWS clients
    ecr = boto3.client('ecr')
    eks = boto3.client('eks')
    
    # Create ECR repository if it doesn't exist
    try:
        ecr.create_repository(repositoryName='ai-customer-service')
    except ecr.exceptions.RepositoryAlreadyExistsException:
        pass
    
    # Get ECR repository URI
    repository_uri = ecr.describe_repositories(
        repositoryNames=['ai-customer-service']
    )['repositories'][0]['repositoryUri']
    
    # Build Docker image
    print("Building Docker image...")
    subprocess.run([
        'docker', 'build', 
        '-t', 'ai-customer-service:latest',
        '.'
    ], check=True)
    
    # Tag and push to ECR
    print("Pushing to ECR...")
    subprocess.run([
        'docker', 'tag',
        'ai-customer-service:latest',
        f'{repository_uri}:latest'
    ], check=True)
    
    # Get ECR login token and login
    auth_token = ecr.get_authorization_token()
    subprocess.run([
        'docker', 'login',
        '-u', 'AWS',
        '-p', auth_token['authorizationData'][0]['authorizationToken'],
        auth_token['authorizationData'][0]['proxyEndpoint']
    ], check=True)
    
    subprocess.run([
        'docker', 'push',
        f'{repository_uri}:latest'
    ], check=True)
    
    # Update kubeconfig for EKS cluster
    print("Updating kubeconfig...")
    subprocess.run([
        'aws', 'eks', 'update-kubeconfig',
        '--name', 'ai-customer-service',
        '--region', 'us-east-1'
    ], check=True)
    
    # Deploy to EKS
    print("Deploying to EKS...")
    # Replace ECR registry in deployment file
    with open('kubernetes/deployment.yaml', 'r') as f:
        deployment = f.read().replace('${ECR_REGISTRY}', repository_uri)
    
    with open('kubernetes/deployment_temp.yaml', 'w') as f:
        f.write(deployment)
    
    subprocess.run([
        'kubectl', 'apply',
        '-f', 'kubernetes/deployment_temp.yaml'
    ], check=True)
    
    # Wait for deployment to complete
    print("Waiting for deployment to complete...")
    time.sleep(30)
    
    # Get service URL
    service = subprocess.check_output([
        'kubectl', 'get', 'service',
        'ai-customer-service',
        '-o', 'jsonpath="{.status.loadBalancer.ingress[0].hostname}"'
    ]).decode().strip('"')
    
    print(f"\nDeployment complete!")
    print(f"Service URL: http://{service}")
    return service

if __name__ == "__main__":
    deploy_to_aws()