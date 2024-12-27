import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

# [Previous generate_realistic_customer_data function remains exactly the same]
def generate_realistic_customer_data():
    scenarios = [
        {
            "type": "complaint",
            "messages": [
                "My order hasn't arrived yet and it's been 5 days",
                "I received a damaged product",
                "The quality is not what I expected",
                "I was charged twice for my order",
                "The product doesn't match the description"
            ],
            "priority": "high"
        },
        {
            "type": "inquiry",
            "messages": [
                "What's the status of my order?",
                "Do you ship internationally?",
                "How long does delivery usually take?",
                "Are there any ongoing promotions?",
                "What's your return policy?"
            ],
            "priority": "medium"
        },
        {
            "type": "support",
            "messages": [
                "How do I reset my password?",
                "The app keeps crashing",
                "I can't login to my account",
                "Where do I find my order history?",
                "How do I update my shipping address?"
            ],
            "priority": "medium"
        },
        {
            "type": "feedback",
            "messages": [
                "Great service, very helpful support team!",
                "The product exceeded my expectations",
                "Quick delivery and perfect packaging",
                "Very dissatisfied with the quality",
                "Amazing customer support experience"
            ],
            "priority": "low"
        }
    ]

    channels = ['email', 'chat', 'voice']
    
    interactions = []
    
    for _ in range(20):
        scenario = random.choice(scenarios)
        channel = random.choice(channels)
        timestamp = datetime.now() - timedelta(minutes=random.randint(1, 60))
        
        interaction = {
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "channel": channel,
            "type": scenario["type"],
            "message": random.choice(scenario["messages"]),
            "priority": scenario["priority"],
            "customer_id": f"CUST-{random.randint(1000, 9999)}"
        }
        interactions.append(interaction)
    
    return interactions

def create_visualizations(df):
    """
    Create and save various visualizations of the customer service data
    """
    # Set figure size
    plt.figure(figsize=(20, 15))
    
    # 1. Channel Distribution (Pie Chart)
    plt.subplot(2, 3, 1)
    channel_dist = df['channel'].value_counts()
    plt.pie(channel_dist, labels=channel_dist.index, autopct='%1.1f%%')
    plt.title('Channel Distribution', pad=20)
    
    # 2. Interaction Types (Bar Chart)
    plt.subplot(2, 3, 2)
    type_counts = df['type'].value_counts()
    plt.bar(type_counts.index, type_counts.values, color='skyblue')
    plt.title('Interaction Types')
    plt.xticks(rotation=45)
    
    # 3. Priority Levels (Bar Chart)
    plt.subplot(2, 3, 3)
    order = ['high', 'medium', 'low']
    priority_counts = df['priority'].value_counts()
    plt.bar(priority_counts.index, priority_counts.values, color='lightgreen')
    plt.title('Priority Levels')
    
    # 4. Hourly Distribution (Line Plot)
    plt.subplot(2, 3, 4)
    hourly_dist = df.groupby(df['timestamp'].dt.hour)['customer_id'].count()
    plt.plot(hourly_dist.index, hourly_dist.values, marker='o', color='orange')
    plt.title('Hourly Distribution')
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Interactions')
    
    # 5. Channel by Type (Heatmap)
    plt.subplot(2, 3, 5)
    channel_type_matrix = pd.crosstab(df['channel'], df['type'])
    sns.heatmap(channel_type_matrix, annot=True, fmt='d', cmap='YlOrRd')
    plt.title('Channel by Type')
    
    # 6. Channel by Priority (Heatmap)
    plt.subplot(2, 3, 6)
    channel_priority_matrix = pd.crosstab(df['channel'], df['priority'])
    sns.heatmap(channel_priority_matrix, annot=True, fmt='d', cmap='YlOrRd')
    plt.title('Channel by Priority')
    
    # Adjust layout and save
    plt.tight_layout()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'customer_service_analysis_{timestamp}.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    return filename

def generate_detailed_report(interactions):
    """
    Generate a comprehensive analysis report of customer service interactions
    """
    df = pd.DataFrame(interactions)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    report = {
        "summary_metrics": {
            "total_interactions": len(interactions),
            "unique_customers": df['customer_id'].nunique()
        },
        
        "channel_analysis": {
            "distribution": df['channel'].value_counts().to_dict(),
            "percentage": df['channel'].value_counts(normalize=True).mul(100).round(2).to_dict()
        },
        
        "interaction_types": {
            "distribution": df['type'].value_counts().to_dict(),
            "percentage": df['type'].value_counts(normalize=True).mul(100).round(2).to_dict()
        },
        
        "priority_levels": {
            "distribution": df['priority'].value_counts().to_dict(),
            "percentage": df['priority'].value_counts(normalize=True).mul(100).round(2).to_dict()
        },
        
        "temporal_analysis": {
            "hourly_distribution": df.groupby(df['timestamp'].dt.hour)['customer_id'].count().to_dict(),
            "peak_hour": df.groupby(df['timestamp'].dt.hour)['customer_id'].count().idxmax()
        },
        
        "cross_analysis": {
            "channel_by_type": pd.crosstab(df['channel'], df['type']).to_dict(),
            "channel_by_priority": pd.crosstab(df['channel'], df['priority']).to_dict()
        }
    }
    
    return report, df

def format_report(report):
    # [Previous format_report function remains exactly the same]
    report_str = """
CUSTOMER SERVICE INTERACTION ANALYSIS REPORT
==========================================

1. SUMMARY METRICS
-----------------
Total Interactions: {total}
Unique Customers: {unique}

2. CHANNEL ANALYSIS
------------------
Distribution:
{channel_dist}

3. INTERACTION TYPES
-------------------
Distribution:
{type_dist}

4. PRIORITY LEVELS
-----------------
Distribution:
{priority_dist}

5. TEMPORAL ANALYSIS
-------------------
Peak Hour: {peak_hour}:00

6. CROSS ANALYSIS
----------------
Channel by Type:
{channel_type}

Channel by Priority:
{channel_priority}
""".format(
        total=report["summary_metrics"]["total_interactions"],
        unique=report["summary_metrics"]["unique_customers"],
        channel_dist="\n".join([f"- {k}: {v} ({report['channel_analysis']['percentage'][k]}%)" 
                               for k, v in report['channel_analysis']['distribution'].items()]),
        type_dist="\n".join([f"- {k}: {v} ({report['interaction_types']['percentage'][k]}%)" 
                            for k, v in report['interaction_types']['distribution'].items()]),
        priority_dist="\n".join([f"- {k}: {v} ({report['priority_levels']['percentage'][k]}%)" 
                                for k, v in report['priority_levels']['distribution'].items()]),
        peak_hour=report["temporal_analysis"]["peak_hour"],
        channel_type="\n".join([f"- {k}: {v}" for k, v in report["cross_analysis"]["channel_by_type"].items()]),
        channel_priority="\n".join([f"- {k}: {v}" for k, v in report["cross_analysis"]["channel_by_priority"].items()])
    )
    
    return report_str

def main():
    print("Generating customer service interactions...")
    interactions = generate_realistic_customer_data()
    
    print("Analyzing data and generating report...")
    report_data, df = generate_detailed_report(interactions)
    formatted_report = format_report(report_data)
    
    print("Creating visualizations...")
    viz_filename = create_visualizations(df)
    
    # Save the report to a file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"customer_service_report_{timestamp}.txt"
    
    with open(report_filename, 'w') as f:
        f.write(formatted_report)
    
    print(f"\nDetailed report has been generated and saved to {report_filename}")
    print(f"Visualizations have been saved to {viz_filename}")
    print("\nReport Preview:")
    print(formatted_report)

if __name__ == "__main__":
    main()