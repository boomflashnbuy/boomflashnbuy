#!/bin/sh
# uso: last.sh N out  -> unisce gli ultimi N risultati salvati del browser
D=/tmp/claude-tool-results/91413245-7fdf-5e0b-844f-6cb1badfc9b3
python3 /home/claude/boomflashnbuy/ads/bf/grab.py "$2" $(ls $D/mcp-remote-devices-Claude_Browser__javascript_tool-*.txt | sort | tail -n "$1")
