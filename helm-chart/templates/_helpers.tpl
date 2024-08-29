{{/*
Generate a fullname for the release
*/}}
{{- define "eol-alert.fullname" -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Generate labels for the resources
*/}}
{{- define "eol-alert.labels" -}}
app.kubernetes.io/name: {{ include "eol-alert.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
helm.sh/chart: {{ include "eol-alert.chart" . }}
app.kubernetes.io/managed-by: Helm
{{- end -}}

{{/*
Generate the name of the chart
*/}}
{{- define "eol-alert.name" -}}
{{- .Chart.Name -}}
{{- end -}}

{{/*
Generate the chart version
*/}}
{{- define "eol-alert.chart" -}}
{{- .Chart.Name }}-{{ .Chart.Version | replace "+" "_" }}
{{- end -}}
