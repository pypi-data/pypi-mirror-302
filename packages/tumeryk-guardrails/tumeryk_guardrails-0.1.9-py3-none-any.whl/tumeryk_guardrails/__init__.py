from .guardrails_client import TumerykGuardrailsClient
from dotenv import load_dotenv

load_dotenv()

client = TumerykGuardrailsClient()

# Expose client methods at the package level
login = client.login
get_policies = client.get_policies
set_policy = client.set_policy
tumeryk_completions = client.tumeryk_completions
get_base_url = client.get_base_url
set_base_url = client.set_base_url
set_token = client.set_token
