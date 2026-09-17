# SLO Burn-Rate Alerting

Burn rate expresses how quickly an SLO error budget is being consumed relative to the allowed rate.

For a service SLO, use two windows:

- short window: catch severe incidents quickly;
- long window: confirm sustained budget consumption.

A common starting pattern is a multi-window, multi-burn-rate alert. Tune thresholds from actual traffic and incident history rather than copying generic values unchanged.
