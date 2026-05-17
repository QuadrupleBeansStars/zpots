import sys
import os

# Ensure apps/api/ is on sys.path so tests can import main, routers, etc.
sys.path.insert(0, os.path.dirname(__file__))
