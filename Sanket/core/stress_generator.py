import pandas as pd
import pickle
import numpy as np

def inject_adversarial_patterns(model_path='model/sanket_brain.pkl', num_samples=10000):
    with open(model_path, 'rb') as f:
        model = pickle.load(f) 
    
    # Generate realistic base data
    df = model.sample(num_samples) 
    
    # Inject Specific Stressors (Adversarial Logic)
    # 1. Latency Spikes (Simulating Network Congestion) 
    df.loc[df.sample(frac=0.05).index, 'latency_ms'] = 5000 
    
    # 2. Logic Errors (Negative Values) 
    df.loc[df.sample(frac=0.02).index, 'amount'] = -100.0 
    
    # 3. Protocol Failures (Internal Server Errors) 
    df.loc[df.sample(frac=0.03).index, 'status_code'] = 500 
    
    # Re-attach IDs for tracking 
    df['transaction_id'] = [f"SYN-{i}" for i in range(num_samples)]
    
    df.to_csv('data/stress_test_logs.csv', index=False) 
    print("Stress test vector generated successfully.")

if __name__ == "__main__":
    inject_adversarial_patterns('sanket_brain.pkl')
    