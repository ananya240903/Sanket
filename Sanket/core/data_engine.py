import pandas as pd
import numpy as np
from ctgan import CTGAN
import pickle
import logging

# Setup logging to track progress instead of just print statements
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SanketDataEngine:
    def __init__(self, output_file='normal_logs.csv'):
        self.output_file = output_file
        self.services = ["DEBIT", "CREDIT", "TRANSFER", "PAYMENT"]

    def generate_baseline(self, num_records=5000):
        """Generates the initial dataset for model training."""
        logger.info(f"Generating {num_records} baseline records...")
        data = {
            "transaction_id": [f"TXN-{10000 + i}" for i in range(num_records)],
            "transaction_type": [np.random.choice(self.services) for _ in range(num_records)],
            "amount": np.round(np.random.uniform(10.0, 500.0, num_records), 2),
            "latency_ms": np.random.randint(50, 250, num_records),
            "currency": ["USD"] * num_records,
            "status_code": [200] * num_records
        }
        df = pd.DataFrame(data)
        df.to_csv(self.output_file, index=False) 
        return df

    def train_model(self, input_csv):
        """Trains the CTGAN on clean patterns."""
        df = pd.read_csv(input_csv)
        # Drop identifiers to focus on behavior 
        train_set = df.drop(columns=['transaction_id']) 
        
        cat_features = ['transaction_type', 'currency', 'status_code'] 
        model = CTGAN(epochs=100)
        
        logger.info("Training NMT-based generative model...")
        model.fit(train_set, cat_features) 
        
        with open('sanket_brain.pkl', 'wb') as f:
            pickle.dump(model, f) 
        logger.info("Model serialized to sanket_brain.pkl")

if __name__ == "__main__":
    engine = SanketDataEngine()
    engine.generate_baseline()
    engine.train_model('normal_logs.csv')