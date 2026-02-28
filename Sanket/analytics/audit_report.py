import pandas as pd
from datetime import datetime
import os

class SanketAuditEngine:
    def __init__(self, logs_file='data/stress_test_logs.csv'):
        if not os.path.exists(logs_file):
            raise FileNotFoundError(f"Missing {logs_file}. Please run stress_generator.py first.")
        
        # 1. Ingest raw stress data
        df_raw = pd.read_csv(logs_file)
        
        # 2. Apply Domain Logic to calculate health on the fly
        df_raw['is_error'] = (df_raw['amount'] < 0) | (df_raw['status_code'] == 500)
        df_raw['is_slow'] = (df_raw['latency_ms'] > 500) & (~df_raw['is_error'])
        
        # 3. Aggregate metrics by service knot
        self.df = df_raw.groupby('transaction_type').agg(
            total_txns=('transaction_id', 'count'),
            errors=('is_error', 'sum'),
            slow=('is_slow', 'sum')
        ).reset_index()
        
        self.df['health_score'] = 100 - ((self.df['errors'] / self.df['total_txns']) * 100)
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def generate_resilience_audit(self):
        """Generates the final executive report for the Digital Twin simulation."""
        print(f"\n{'='*60}")
        print(f"SANKET EXECUTIVE AUDIT | {self.timestamp}")
        print(f"{'='*60}")

        # Vulnerability Analysis
        weakest = self.df.loc[self.df['health_score'].idxmin()]
        print(f"\n[VULNERABILITY ASSESSMENT]")
        print(f" ? Critical Bottleneck:  {weakest['transaction_type']}")
        print(f" ? Resilience Score:     {weakest['health_score']:.2f}/100")
        print(f" ? Detected Leakage:     {int(weakest['errors'])} units")

        # Systemic Impact
        total_vol = self.df['total_txns'].sum()
        total_err = self.df['errors'].sum()
        print(f"\n[SYSTEMIC LEAKAGE DATA]")
        print(f" ? Stress Volume:        {int(total_vol)} synthetic transactions")
        print(f" ? Global Leakage Rate:  {(total_err/total_vol)*100:.2f}%")

        # ESG & Carbon Risk
        total_slow = self.df['slow'].sum()
        print(f"\n[ESG & CARBON RISK IMPACT]")
        print(f" ? Latency Inefficiency: {int(total_slow)} high-energy compute events")
        print(" ? Risk Summary: High-latency paths (5000ms) indicate code paths")
        print("   that increase server thermals and energy consumption.")
        
        print(f"\n{'='*60}")
        print("STATUS: AUDIT COMPLETE | SYSTEM OPTIMIZATION RECOMMENDED")
        print(f"{'='*60}\n")

if __name__ == "__main__":
    try:
        auditor = SanketAuditEngine()
        auditor.generate_resilience_audit()
    except Exception as e:
        print(f"Error: {e}")