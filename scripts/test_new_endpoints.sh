#!/bin/bash

# Quick test script for new API endpoints
# Usage: ./test_new_endpoints.sh

BASE_URL="http://localhost:5050/api/system"
BOLD='\033[1m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${BOLD}🧪 Testing Dashboard API Endpoints${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test 1: Main stats (should be fast)
echo -e "${BLUE}1. Testing /stats (main endpoint)${NC}"
START=$(date +%s%3N)
RESPONSE=$(curl -s $BASE_URL/stats)
END=$(date +%s%3N)
ELAPSED=$((END - START))
echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
echo -e "${GREEN}⏱️  Response time: ${ELAPSED}ms${NC}"
echo ""

# Test 2: Weather
echo -e "${BLUE}2. Testing /weather${NC}"
START=$(date +%s%3N)
RESPONSE=$(curl -s $BASE_URL/weather)
END=$(date +%s%3N)
ELAPSED=$((END - START))
echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
echo -e "${GREEN}⏱️  Response time: ${ELAPSED}ms${NC}"
echo ""

# Test 3: Public IP
echo -e "${BLUE}3. Testing /network/public-ip${NC}"
START=$(date +%s%3N)
RESPONSE=$(curl -s $BASE_URL/network/public-ip)
END=$(date +%s%3N)
ELAPSED=$((END - START))
echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
echo -e "${GREEN}⏱️  Response time: ${ELAPSED}ms${NC}"
echo ""

# Test 4: WiFi
echo -e "${BLUE}4. Testing /network/wifi${NC}"
START=$(date +%s%3N)
RESPONSE=$(curl -s $BASE_URL/network/wifi)
END=$(date +%s%3N)
ELAPSED=$((END - START))
echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
echo -e "${GREEN}⏱️  Response time: ${ELAPSED}ms${NC}"
echo ""

# Test 5: Complete network
echo -e "${BLUE}5. Testing /network${NC}"
START=$(date +%s%3N)
RESPONSE=$(curl -s $BASE_URL/network)
END=$(date +%s%3N)
ELAPSED=$((END - START))
echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
echo -e "${GREEN}⏱️  Response time: ${ELAPSED}ms${NC}"
echo ""

# Test 6: Audio devices
echo -e "${BLUE}6. Testing /audio${NC}"
START=$(date +%s%3N)
RESPONSE=$(curl -s $BASE_URL/audio)
END=$(date +%s%3N)
ELAPSED=$((END - START))
echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
echo -e "${GREEN}⏱️  Response time: ${ELAPSED}ms${NC}"
echo ""

# Test 7: System info
echo -e "${BLUE}7. Testing /system-info${NC}"
START=$(date +%s%3N)
RESPONSE=$(curl -s $BASE_URL/system-info)
END=$(date +%s%3N)
ELAPSED=$((END - START))
echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
echo -e "${GREEN}⏱️  Response time: ${ELAPSED}ms${NC}"
echo ""

# Test 8: Health check
echo -e "${BLUE}8. Testing /health${NC}"
START=$(date +%s%3N)
RESPONSE=$(curl -s $BASE_URL/health)
END=$(date +%s%3N)
ELAPSED=$((END - START))
echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
echo -e "${GREEN}⏱️  Response time: ${ELAPSED}ms${NC}"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ All tests complete!${NC}"
echo ""
echo -e "${YELLOW}💡 Tip: Run this script again to test cache performance${NC}"
echo -e "${YELLOW}   Cached endpoints should respond much faster on 2nd run${NC}"

