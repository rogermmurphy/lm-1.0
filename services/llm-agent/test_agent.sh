#!/bin/bash
# Test Agent Tool Calling with bash curl
# Proper quoting for bash

echo "=================================="
echo "Testing Agent Tool Calling POC"
echo "=================================="
echo ""

echo "TEST 1: List user's classes (should use list_user_classes tool)"
echo "----------------------------------------------------------------"
curl -X POST http://localhost:8005/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "show me my classes", "use_rag": false}' \
  2>/dev/null | python3 -m json.tool
echo ""
echo ""

echo "TEST 2: Create a class (should use create_class_tool)"
echo "----------------------------------------------------------------"
curl -X POST http://localhost:8005/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "create a class called Chemistry 101", "use_rag": false}' \
  2>/dev/null | python3 -m json.tool
echo ""
echo ""

echo "TEST 3: General question (should answer directly, no tool)"
echo "----------------------------------------------------------------"
curl -X POST http://localhost:8005/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "what is 2+2", "use_rag": false}' \
  2>/dev/null | python3 -m json.tool
echo ""

echo "=================================="
echo "Tests Complete"
echo "=================================="
