#!/bin/bash
# Trigger daily preview workflow on GitHub Actions
# Add to crontab: 0 14 * * * /path/to/trigger-preview-workflow.sh

set -e

REPO="loliba92/Scenario"
WORKFLOW="daily-preview.yml"
LOG_DIR="/home/user/Scenario/logs"

mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/trigger-preview-$(date +%Y-%m-%d).log"

{
    echo "=========================================="
    echo "Triggering Preview Workflow - $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
    echo "=========================================="

    # Trigger workflow via gh CLI
    gh workflow run "$WORKFLOW" -R "$REPO" 2>&1

    if [ $? -eq 0 ]; then
        echo "✅ Workflow triggered successfully"
        echo "Check progress at: https://github.com/$REPO/actions/workflows/$WORKFLOW"
    else
        echo "❌ Failed to trigger workflow"
        exit 1
    fi

    echo "=========================================="
} | tee "$LOG_FILE"
