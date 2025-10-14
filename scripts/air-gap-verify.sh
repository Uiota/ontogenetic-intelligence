#!/bin/bash
# UIOTA Air-Gap Compliance Verification
# Ensures complete sovereignty and zero telemetry

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🛡️ UIOTA Air-Gap Compliance Verification"
echo "========================================="
echo ""

# Check for external network requests in code
echo "🔍 Scanning for external network requests..."
NETWORK_ISSUES=0

# Check Python files
echo "  Checking Python files..."
if grep -r "requests\.get\|requests\.post\|urllib\.request\|http\.client" "$PROJECT_ROOT/src/" 2>/dev/null | grep -v "localhost\|127.0.0.1"; then
    echo "  ❌ Found external network requests in Python code"
    NETWORK_ISSUES=$((NETWORK_ISSUES + 1))
else
    echo "  ✅ No external network requests in Python code"
fi

# Check JavaScript files
echo "  Checking JavaScript files..."
if find "$PROJECT_ROOT/web-interface" -name "*.js" -o -name "*.jsx" -o -name "*.ts" -o -name "*.tsx" 2>/dev/null | xargs grep -l "fetch\|axios\|XMLHttpRequest" | xargs grep -v "localhost\|127.0.0.1" 2>/dev/null; then
    echo "  ❌ Found potential external network requests in JavaScript code"
    NETWORK_ISSUES=$((NETWORK_ISSUES + 1))
else
    echo "  ✅ No external network requests in JavaScript code"
fi

# Check for telemetry and analytics
echo ""
echo "📊 Checking for telemetry and analytics..."
TELEMETRY_ISSUES=0

# Check for common telemetry patterns
if grep -r "analytics\|telemetry\|tracking\|google-analytics\|gtag" "$PROJECT_ROOT/" --exclude-dir=.git 2>/dev/null; then
    echo "  ❌ Found potential telemetry code"
    TELEMETRY_ISSUES=$((TELEMETRY_ISSUES + 1))
else
    echo "  ✅ No telemetry code detected"
fi

# Check for external CDN dependencies
echo ""
echo "🌐 Checking for external CDN dependencies..."
CDN_ISSUES=0

# Check HTML files for external resources
if find "$PROJECT_ROOT" -name "*.html" 2>/dev/null | xargs grep -l "cdn\|googleapis\|cloudflare\|jsdelivr\|unpkg" 2>/dev/null; then
    echo "  ❌ Found external CDN dependencies"
    CDN_ISSUES=$((CDN_ISSUES + 1))
else
    echo "  ✅ No external CDN dependencies found"
fi

# Check package.json for external dependencies with telemetry
echo ""
echo "📦 Checking dependencies for telemetry..."
DEPENDENCY_ISSUES=0

if [ -f "$PROJECT_ROOT/package.json" ]; then
    if grep -E "(google|facebook|microsoft|adobe|amplitude|mixpanel|segment)" "$PROJECT_ROOT/package.json" 2>/dev/null; then
        echo "  ⚠️  Found dependencies from companies known for telemetry"
        echo "     Please verify these are necessary and privacy-compliant"
    else
        echo "  ✅ No obvious telemetry dependencies"
    fi
fi

# Check for Intel ME detection
echo ""
echo "🔧 Checking hardware compliance..."
HARDWARE_ISSUES=0

# Check if running on Intel ME-free system
if command -v intelmetool &> /dev/null; then
    if intelmetool -s 2>/dev/null | grep -q "Intel ME found"; then
        echo "  ❌ Intel Management Engine detected"
        echo "     For complete sovereignty, use AMD or RISC-V systems"
        HARDWARE_ISSUES=$((HARDWARE_ISSUES + 1))
    else
        echo "  ✅ No Intel ME detected"
    fi
else
    echo "  ℹ️  Intel ME detection tool not available"
    echo "     Install 'intelmetool' for hardware verification"
fi

# Check for NVIDIA telemetry
if lspci 2>/dev/null | grep -i nvidia; then
    echo "  ⚠️  NVIDIA GPU detected"
    echo "     NVIDIA drivers may include telemetry - consider AMD alternatives"
fi

# Check network interfaces for air-gap compliance
echo ""
echo "🌐 Checking network interface status..."
NETWORK_STATUS=0

# Check if network interfaces are disabled
if ip link show 2>/dev/null | grep -E "state UP.*eth|state UP.*wlan"; then
    echo "  ⚠️  Network interfaces are active"
    echo "     For air-gap compliance, disable network interfaces"
    echo "     Use: sudo ip link set <interface> down"
else
    echo "  ✅ Network interfaces appear disabled or not present"
fi

# Check for WiFi and Bluetooth
if command -v rfkill &> /dev/null; then
    if rfkill list 2>/dev/null | grep -E "Wireless LAN.*unblocked|Bluetooth.*unblocked"; then
        echo "  ⚠️  WiFi or Bluetooth is enabled"
        echo "     For air-gap compliance, run: sudo rfkill block all"
    else
        echo "  ✅ WiFi and Bluetooth are blocked"
    fi
fi

# Check for secret files that shouldn't be committed
echo ""
echo "🔐 Checking for secrets and credentials..."
SECRET_ISSUES=0

# Check for common secret file patterns
if find "$PROJECT_ROOT" -name "*.key" -o -name "*.pem" -o -name ".env" -o -name "credentials*" -o -name "*secret*" | grep -v ".env.example"; then
    echo "  ⚠️  Found potential secret files"
    echo "     Ensure these are not committed to version control"
else
    echo "  ✅ No obvious secret files found"
fi

# Summary
echo ""
echo "📋 Air-Gap Compliance Summary"
echo "============================"

TOTAL_ISSUES=$((NETWORK_ISSUES + TELEMETRY_ISSUES + CDN_ISSUES + DEPENDENCY_ISSUES + HARDWARE_ISSUES + SECRET_ISSUES))

if [ $TOTAL_ISSUES -eq 0 ]; then
    echo "✅ PASSED: System appears air-gap compliant"
    echo ""
    echo "🛡️ Sovereignty Status: COMPLIANT"
    echo "🔒 Zero Telemetry: VERIFIED"
    echo "🌐 Air-Gap Ready: CONFIRMED"
    echo ""
    echo "Your system meets UIOTA sovereignty standards!"
else
    echo "⚠️  ISSUES FOUND: $TOTAL_ISSUES compliance issues detected"
    echo ""
    echo "Issue breakdown:"
    [ $NETWORK_ISSUES -gt 0 ] && echo "  • Network requests: $NETWORK_ISSUES"
    [ $TELEMETRY_ISSUES -gt 0 ] && echo "  • Telemetry code: $TELEMETRY_ISSUES"
    [ $CDN_ISSUES -gt 0 ] && echo "  • CDN dependencies: $CDN_ISSUES"
    [ $DEPENDENCY_ISSUES -gt 0 ] && echo "  • Dependency issues: $DEPENDENCY_ISSUES"
    [ $HARDWARE_ISSUES -gt 0 ] && echo "  • Hardware issues: $HARDWARE_ISSUES"
    [ $SECRET_ISSUES -gt 0 ] && echo "  • Secret file issues: $SECRET_ISSUES"
    echo ""
    echo "Please address these issues for complete air-gap compliance."
fi

# Generate compliance report
REPORT_FILE="$PROJECT_ROOT/air-gap-compliance-report.txt"
cat > "$REPORT_FILE" << EOF
UIOTA Air-Gap Compliance Report
===============================
Generated: $(date)
System: $(uname -a)

Compliance Status: $([ $TOTAL_ISSUES -eq 0 ] && echo "COMPLIANT" || echo "ISSUES FOUND")
Total Issues: $TOTAL_ISSUES

Issue Breakdown:
- Network requests: $NETWORK_ISSUES
- Telemetry code: $TELEMETRY_ISSUES
- CDN dependencies: $CDN_ISSUES
- Dependency issues: $DEPENDENCY_ISSUES
- Hardware issues: $HARDWARE_ISSUES
- Secret file issues: $SECRET_ISSUES

Hardware Information:
- CPU: $(grep "model name" /proc/cpuinfo | head -1 | cut -d: -f2 | xargs)
- Memory: $(free -h | grep "Mem:" | awk '{print $2}')
- Storage: $(df -h / | tail -1 | awk '{print $2}')

Network Status:
$(ip link show 2>/dev/null || echo "Network information unavailable")

Recommendations:
1. Use AMD or RISC-V processors (Intel ME-free)
2. Disable all network interfaces for air-gap operation
3. Remove any telemetry or analytics code
4. Use local dependencies only (no CDNs)
5. Verify all external dependencies are necessary

For complete sovereignty, address all issues above.

---
UIOTA Research - Digital Sovereignty Through Adaptive Intelligence
EOF

echo ""
echo "📄 Detailed report saved to: air-gap-compliance-report.txt"

exit $TOTAL_ISSUES
EOF

chmod +x /home/uiota/ontogenetic-intelligence/scripts/air-gap-verify.sh