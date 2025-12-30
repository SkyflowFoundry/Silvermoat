#!/bin/bash
# Build psycopg2 Lambda layer for Amazon Linux 2023 (Python 3.12)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
LAYER_DIR="$PROJECT_ROOT/lambda-layer"
OUTPUT_ZIP="$PROJECT_ROOT/psycopg2-layer.zip"

echo "Building psycopg2 Lambda layer..."

# Clean up previous build
rm -rf "$LAYER_DIR"
rm -f "$OUTPUT_ZIP"

mkdir -p "$LAYER_DIR/python"

# Use Docker to build for Lambda environment (Amazon Linux 2023)
echo "Building psycopg2 using Docker (Amazon Linux 2023)..."
docker run --rm \
  --entrypoint /bin/bash \
  -v "$LAYER_DIR:/layer" \
  public.ecr.aws/lambda/python:3.12 \
  -c "
    yum install -y postgresql15-devel gcc python3-devel
    pip3 install psycopg2-binary -t /layer/python
    chown -R $(id -u):$(id -g) /layer
  "

# Create ZIP file
echo "Creating layer ZIP file..."
cd "$LAYER_DIR"
zip -r "$OUTPUT_ZIP" python/
cd "$PROJECT_ROOT"

# Clean up layer directory
rm -rf "$LAYER_DIR"

echo "✓ Layer created: $OUTPUT_ZIP"
echo "Size: $(du -h "$OUTPUT_ZIP" | cut -f1)"
echo ""
echo "Next steps:"
echo "  1. Upload to S3: aws s3 cp $OUTPUT_ZIP s3://YOUR_BUCKET/lambda/psycopg2-layer.zip"
echo "  2. Deploy stack with updated layer"
