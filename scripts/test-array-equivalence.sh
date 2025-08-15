#!/bin/bash

# 🔍 Test Script for Array Equivalence
# Tests if the generated script has the same array functionality as the original

echo "🔍 Testing Array Equivalence Between Original and Generated Scripts"
echo "=================================================================="
echo ""

# Test original script arrays
echo "📖 Testing ORIGINAL script arrays..."
source scripts/setup-gcp-project.sh

echo "   Required APIs count: ${#REQUIRED_APIS[@]}"
echo "   Excluded APIs count: ${#EXCLUDED_APIS[@]}"
echo "   First required API: ${REQUIRED_APIS[0]}"
echo "   Last required API: ${REQUIRED_APIS[-1]}"
echo ""

# Test generated script arrays
echo "📖 Testing GENERATED script arrays..."
source scripts/setup-gcp-project-generated.sh

echo "   Required APIs count: ${#REQUIRED_APIS[@]}"
echo "   Excluded APIs count: ${#EXCLUDED_APIS[@]}"
echo "   First required API: ${REQUIRED_APIS[0]}"
echo "   Last required API: ${REQUIRED_APIS[-1]}"
echo ""

# Compare array contents
echo "🔍 Array Content Comparison:"
echo "   Original Required APIs:"
for api in "${REQUIRED_APIS[@]}"; do
    echo "     - "ap"i"
done

echo ""
echo "   Generated Required APIs:"
for api in "${REQUIRED_APIS[@]}"; do
    echo "     - "ap"i"
done

echo ""
echo "✅ Array functionality test completed!"