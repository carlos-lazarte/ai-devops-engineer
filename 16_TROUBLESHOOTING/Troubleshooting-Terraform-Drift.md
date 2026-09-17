---
type: troubleshooting
domain: iac
technology: Terraform
difficulty: intermediate
severity: medium
status: active
tags: [iac, troubleshooting]
---
# Troubleshooting-Terraform-Drift

Drift means real infrastructure differs from the desired configuration/state represented to Terraform.

## First checks
```bash
terraform plan
terraform state list
```

## Evidence
Determine whether drift came from manual changes, another automation path, provider behavior, or an intentional change missing from code.

## Rule
Do not blindly apply a plan to eliminate drift. Review the diff and confirm intended state.
