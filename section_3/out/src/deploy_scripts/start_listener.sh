#!/bin/bash

cd "$(dirname "$0")"
mkdir -p ../routed_studies
ROUTE_DIR="$(cd ../routed_studies && pwd)"
curl -X POST http://localhost:8042/tools/execute-script --data-binary @route_dicoms.lua -v

# Resolve full path since sudo's secure_path may not include storescp's location
STORESCP_BIN="$(command -v storescp)"
if [ -z "$STORESCP_BIN" ]; then
    echo "storescp not found on PATH. Install DCMTK (e.g. 'apt-get install dcmtk' or 'brew install dcmtk')." >&2
    exit 1
fi
sudo "$STORESCP_BIN" 106 -v -aet HIPPOAI -od "$ROUTE_DIR" --sort-on-study-uid st