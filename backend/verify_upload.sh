#!/bin/bash
# Verification script for Hugging Face upload

echo "=== Hugging Face Backend Upload Verification ==="
echo ""
echo "Checking required files in to-do folder:"
echo ""

# Check for essential files
REQUIRED_FILES=(
    "app.py"
    "Dockerfile"
    "requirements.txt"
    "README.md"
    "app.json"
    "src/api/main.py"
    ".gitignore"
)

MISSING_FILES=()
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "to-do/$file" ]; then
        echo "✓ $file - Found"
    else
        echo "✗ $file - Missing"
        MISSING_FILES+=("$file")
    fi
done

echo ""
if [ ${#MISSING_FILES[@]} -eq 0 ]; then
    echo "✓ All required files are present!"
    echo ""
    echo "Folder structure looks good for Hugging Face upload."
    echo ""
    echo "To upload to Hugging Face:"
    echo "1. Go to https://huggingface.co/spaces"
    echo "2. Click 'Create new Space'"
    echo "3. Choose 'Docker' SDK"
    echo "4. Upload all files from the 'to-do' folder"
    echo "5. Add environment variables (OPENAI_API_KEY, etc.) in Space settings"
    echo ""
    echo "The application will run on port 8000 as configured."
else
    echo "✗ Some required files are missing. Please address before upload."
fi