#!/usr/bin/env python3
"""Bounded, local-only multi-agent federation reference implementation."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional
from uuid import uuid4


@dataclass(frozen=True)
class Task:
    principal: str
    tenant_id: str
    environment: str
    requested_agent: str
    goal: str
    allowed_hops: int = 2
    approval_id: Optional[str] = None
    correlation_id: str = ""

    def with_correlation_id(self) -> "Task":
        return self if self.correlation_id else Task(**{**self.__dict__, "correlation_id": str(uuid4())})


@dataclass(frozen=True)
class AgentResult:
    agent_id: str
    status: str
    findings: List[str]
    references: List[str]
    delegated_tasks: List[str]
    correlation_id: str


@dataclass(frozen=True)
class AgentSpec:
    agent_id: str
    domains: tuple[str, ...]
    enabled: bool = True


@dataclass(frozen=True)
class MCPServerSpec:
    server_id: str
    enabled: bool
    environments: tuple[str, ...]
    capabilities: tuple[str, ...]


class FederationPolicy:
    """Fail-closed policy checks for federation routing."""

    def __init__(self, agents: Dict[str, AgentSpec], servers: Dict[str, MCPServerSpec], max_agents: int = 4, max_hops: int = 2):
        self.agents = agents
        self.servers = servers
        self.max_agents = max_agents
        self.max_hops = max_hops

    def allow_agent(self, task: Task) -> tuple[bool, str]:
        spec = self.agents.get(task.requested_agent)
        if not spec or not spec.enabled:
            return False, "agent_not_registered_or_disabled"
        if task.allowed_hops > self.max_hops:
            return False, "delegation_depth_exceeded"
        return True, "allowed"

    def allow_mcp(self, task: Task, server_id: str, tool: str) -> tuple[bool, str]:
        server = self.servers.get(server_id)
        if not server or not server.enabled:
            return False, "mcp_server_not_registered_or_disabled"
        if task.environment not in server.environments:
            return False, "environment_not_allowed"
        if tool not in server.capabilities:
            return False, "capability_not_registered"
        return True, "allowed"


class Orchestrator:
    def __init__(self, policy: FederationPolicy):
        self.policy = policy
        self.agents: Dict[str, Callable[[Task], AgentResult]] = {}

    def register_agent_handler(self, agent_id: str, handler: Callable[[Task], AgentResult]) -> None:
        if agent_id not in self.policy.agents:
            raise ValueError("agent must be present in registry")
        self.agents[agent_id] = handler

    def run(self, task: Task) -> AgentResult:
        task = task.with_correlation_id()
        allowed, reason = self.policy.allow_agent(task)
        if not allowed:
            return AgentResult(task.requested_agent, "denied", [reason], [], [], task.correlation_id)

        handler = self.agents.get(task.requested_agent)
        if handler is None:
            return AgentResult(task.requested_agent, "failed", ["agent_handler_not_configured"], [], [], task.correlation_id)

        result = handler(task)
        if result.correlation_id != task.correlation_id:
            raise ValueError("handler must preserve correlation_id")
        return result


def demo_agents() -> Dict[str, Callable[[Task], AgentResult]]:
    def devops(task: Task) -> AgentResult:
        return AgentResult(
            "devops",
            "completed",
            ["Simulated DevOps analysis completed", "No production action executed"],
            ["26_OPERATIONAL_AGENT_LAB/scenarios/K8S-NOTREADY-001.yaml"],
            [],
            task.correlation_id,
        )

    def sre(task: Task) -> AgentResult:
        return AgentResult(
            "sre",
            "completed",
            ["Simulated SRE correlation completed"],
            ["36_OBSERVABILITY_SRE/README.md"],
            [],
            task.correlation_id,
        )

    return {"devops": devops, "sre": sre}
