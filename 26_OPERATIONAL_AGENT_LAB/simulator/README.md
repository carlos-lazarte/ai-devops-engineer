# Incident Simulator

The simulator creates local scenario manifests only.

Example:

```bash
python incident_generator.py \
  --scenario K8S-NOTREADY-001 \
  --output ./workspace/K8S-NOTREADY-001
```

No network connections, Kubernetes API calls, SSH sessions, or production mutations are performed.
