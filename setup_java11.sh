#!/bin/bash
# Setup script to configure Java 17 for this project (PySpark 4.0.1 requires Java 17+)

# Find Java 17 installation (required for PySpark 4.0.1)
JAVA17_HOME="/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home"

if [ -d "$JAVA17_HOME" ]; then
    export JAVA_HOME="$JAVA17_HOME"
    export PATH="$JAVA_HOME/bin:$PATH"
    echo "✓ Java 17 configured: $JAVA_HOME"
    java -version
else
    echo "⚠️  Java 17 not found at $JAVA17_HOME"
    echo "   Trying alternative location..."
    JAVA17_ALT=$(/usr/libexec/java_home -v 17 2>/dev/null)
    if [ -n "$JAVA17_ALT" ]; then
        export JAVA_HOME="$JAVA17_ALT"
        export PATH="$JAVA_HOME/bin:$PATH"
        echo "✓ Java 17 configured: $JAVA_HOME"
        java -version
    else
        echo "❌ Java 17 not found. Please install: brew install openjdk@17"
        echo "   (PySpark 4.0.1 requires Java 17 or higher)"
        exit 1
    fi
fi

