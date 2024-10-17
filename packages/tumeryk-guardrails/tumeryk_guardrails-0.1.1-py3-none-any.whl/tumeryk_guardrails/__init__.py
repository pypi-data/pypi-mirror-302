from .guardrails_client import TumerykGuardrailsClient

client = TumerykGuardrailsClient()

login = client.login
get_policies = client.get_policies
set_policy = client.set_policy
send_guard = client.send_guard