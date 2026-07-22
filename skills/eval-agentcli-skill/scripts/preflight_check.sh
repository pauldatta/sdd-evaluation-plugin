#!/usr/bin/env bash
# Preflight Check Script for GCP Agent Runtime, APIs, IAM Permissions, and Services
set -e

echo "============================================================"
echo "🔍 Starting GCP ADK & Agent Runtime Preflight Check"
echo "============================================================"

# 1. Check Active GCloud Credentials
echo -n "Checking GCP Authentication... "
ACTIVE_ACCOUNT=$(gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>/dev/null || true)
if [ -z "$ACTIVE_ACCOUNT" ]; then
  echo "❌ FAIL: No active gcloud user/service account found."
  echo "👉 Please run: gcloud auth application-default login"
  exit 1
fi
echo "✅ PASS ($ACTIVE_ACCOUNT)"

# 2. Get GCP Project ID
PROJECT_ID=${GCP_PROJECT_ID:-$(gcloud config get-value project 2>/dev/null || true)}
if [ -z "$PROJECT_ID" ] || [ "$PROJECT_ID" == "(unset)" ]; then
  echo "❌ FAIL: GCP Project ID is unset."
  echo "👉 Set your project: gcloud config set project YOUR_PROJECT_ID"
  exit 1
fi
echo "📌 Active GCP Project: $PROJECT_ID"

# 3. Required GCP APIs for ADK, Vertex Reasoning Engine, Telemetry & Gemini Enterprise
REQUIRED_APIS=(
  "aiplatform.googleapis.com"           # Vertex AI / Reasoning Engines
  "cloudresourcemanager.googleapis.com" # Resource Manager
  "iam.googleapis.com"                  # Identity & Access Management
  "logging.googleapis.com"              # Cloud Logging
  "monitoring.googleapis.com"           # Cloud Monitoring & OpenTelemetry
  "bigquery.googleapis.com"             # BigQuery Agent Analytics
  "discoveryengine.googleapis.com"      # Gemini Enterprise Engine
)

echo "------------------------------------------------------------"
echo "🔄 Checking & Enabling Required GCP Service APIs..."
echo "------------------------------------------------------------"

ENABLED_SERVICES=$(gcloud services list --enabled --project="$PROJECT_ID" --format="value(config.name)" 2>/dev/null || true)

APIS_TO_ENABLE=()
for API in "${REQUIRED_APIS[@]}"; do
  if echo "$ENABLED_SERVICES" | grep -q "^${API}$"; then
    echo "  ✅ Enabled: $API"
  else
    echo "  ⚠️  Missing: $API (Queued for enabling)"
    APIS_TO_ENABLE+=("$API")
  fi
done

if [ ${#APIS_TO_ENABLE[@]} -ne 0 ]; then
  echo "🚀 Enabling missing APIs: ${APIS_TO_ENABLE[*]}..."
  gcloud services enable "${APIS_TO_ENABLE[@]}" --project="$PROJECT_ID"
  echo "✅ All APIs enabled successfully."
fi

# 4. Check Optional Google Maps Environment Credentials
echo "------------------------------------------------------------"
echo "🗺️  Checking Google Maps API Key Environment..."
if [ -z "$GOOGLE_MAPS_API_KEY" ]; then
  echo "  ℹ️  Note: GOOGLE_MAPS_API_KEY environment variable is not exported locally."
  echo "      Make sure to set GOOGLE_MAPS_API_KEY if testing Maps Places/Directions tools."
else
  echo "  ✅ GOOGLE_MAPS_API_KEY is exported."
fi

# 5. Check Gemini Enterprise App ID Configuration
echo "------------------------------------------------------------"
echo "🌐 Checking Gemini Enterprise Registration Environment..."
GE_APP_ID=${GEMINI_ENTERPRISE_APP_ID:-$GEMINI_ENTERPRISE_APP_RESOURCE_ID}
if [ -z "$GE_APP_ID" ]; then
  echo "  ℹ️  Note: GEMINI_ENTERPRISE_APP_ID environment variable is not exported locally."
  echo "      Default structure: projects/$PROJECT_ID/locations/global/collections/default_collection/engines/cymbal-app"
else
  echo "  ✅ GEMINI_ENTERPRISE_APP_ID is exported: $GE_APP_ID"
fi

echo "============================================================"
echo "🎉 Preflight Check Complete! All systems ready for ADK Eval, Deploy & GE Publish."
echo "============================================================"

