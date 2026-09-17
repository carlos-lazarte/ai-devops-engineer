from pathlib import Path
import sys

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))

from orchestrator.orchestrator import AgentSpec, FederationPolicy, MCPServerSpec, Orchestrator, Task, demo_agents


def build_orchestrator():
    agents = {
        "devops": AgentSpec("devops", ("kubernetes", "linux")),
        "sre": AgentSpec("sre", ("incident", "observability")),
    }
    servers = {
        "vault-knowledge": MCPServerSpec("vault-knowledge", True, ("lab", "test"), ("search_notes", "read_note")),
    }
    policy = FederationPolicy(agents, servers)
    orch = Orchestrator(policy)
    for name, handler in demo_agents().items():
        if name in agents:
            orch.register_agent_handler(name, handler)
    return orch


def test_routes_registered_agent():
    orch = build_orchestrator()
    result = orch.run(Task("user", "t1", "lab", "devops", "analyze node notready"))
    assert result.status == "completed"
    assert result.correlation_id


def test_denies_unknown_agent():
    orch = build_orchestrator()
    result = orch.run(Task("user", "t1", "lab", "unknown", "do something"))
    assert result.status == "denied"


def test_denies_excessive_hops():
    orch = build_orchestrator()
    result = orch.run(Task("user", "t1", "lab", "devops", "delegate", allowed_hops=3))
    assert result.status == "denied"


def test_mcp_policy_is_fail_closed():
    orch = build_orchestrator()
    task = Task("user", "t1", "prod", "devops", "read")
    allowed, reason = orch.policy.allow_mcp(task, "vault-knowledge", "search_notes")
    assert not allowed
    assert reason == "environment_not_allowed"
