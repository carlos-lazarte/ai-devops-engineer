{{- define "ai-devops.fullname" -}}
{{- printf "%s-%s" .Release.Name "runtime" | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- define "ai-devops.labels" -}}
app.kubernetes.io/name: ai-devops-runtime
app.kubernetes.io/part-of: ai-devops-platform
app.kubernetes.io/managed-by: {{ .Release.Service }}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version | replace "+" "_" }}
{{- end -}}
