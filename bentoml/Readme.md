# Setup venv
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install "bentoml>=1.1.7,<1.4.0"
pip install scikit-learn pandas

# Run the service
 bentoml serve model_service_v1:svc