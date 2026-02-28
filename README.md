# SANKET: AI-Driven Digital Twin for Financial Resilience

**SANKET** (**S**ystemic **A**nalysis of **N**etwork-**K**not **E**rror **T**racking) is a standalone **Digital Twin framework** designed to simulate and stress-test financial microservice architectures. Using **Generative Adversarial Networks (GANs)**, SANKET synthesizes high-fidelity transactional environments to identify systemic vulnerabilities and **Carbon Risk** without compromising production stability or data privacy.


## 🛠️ Key Features
* **Neural Behavioral Synthesis**: Leverages **CTGAN** to learn and replicate complex financial logic (Credit, Debit, Transfer) from baseline metadata.
* **Adversarial Chaos Injection**: Acts as a chaos agent by injecting 5000ms latency spikes and "Logic Traps" into synthetic streams to find system breaking points.
* **Topographical Monitoring**: Maps microservice health onto a spatial coordinate grid to visualize "Transaction Leakage" in real-time.
* **ESG & Carbon Audit**: Correlates high-latency events with inefficient compute energy, providing actionable insights into the system's digital carbon footprint.

## 📂 Project Structure
```text
SANKET/
├── core/                # AI Logic: data_engine.py, stress_generator.py
├── dashboard/           # UI: monitor_app.py
├── analytics/           # Reporting: audit_report.py
├── data/                # Storage: normal_logs.csv, stress_test_logs.csv
├── model/               # Serialized AI: sanket_brain.pkl
└── requirements.txt     # Dependency list
```
## 🚀 How to Run

### 1. Environment Setup
To ensure a clean installation of the AI and visualization stack, initialize a virtual environment in your terminal.

```powershell
# Initialize Virtual Environment (Windows)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install required libraries
pip install -r requirements.txt
```
## 📈 Impact & Results

The **SANKET Digital Twin** provided the following high-fidelity insights during the adversarial stress-test simulation:

* **Global Leakage Rate**: Identified a **7.87% failure rate** across the network topography under extreme adversarial load.
* **Critical Bottleneck**: Pinpointed the **PAYMENT** node as the primary system vulnerability with a **91.28% resilience score**.
* **ESG & Carbon Risk**: Flagged **457 high-energy compute events**, identifying high-latency paths (5000ms) that require architectural optimization to reduce the system's digital carbon footprint.
