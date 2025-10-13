#!/bin/bash
echo "Stopping Order Processing System..."

# Kill application services
if [ -n "$ORDER_SERVICE_PID" ]; then
    kill $ORDER_SERVICE_PID 2>/dev/null || true
fi

if [ -n "$DELIVERY_SERVICE_PID" ]; then
    kill $DELIVERY_SERVICE_PID 2>/dev/null || true
fi

# Stop Docker services
docker-compose down

echo "Services stopped."
