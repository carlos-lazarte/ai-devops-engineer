from planner.planner import AdaptivePlanner

planner = AdaptivePlanner()

result = planner.plan(
    task_id="PLAN-K8S-DEMO",
    goal="diagnose Kubernetes node not ready incident",
    tenant_id="demo",
    environment="lab",
)

print(result)
