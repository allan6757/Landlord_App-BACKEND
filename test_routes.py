#!/usr/bin/env python3
"""Test API routes locally"""

from app import create_app
from app.config import ProductionConfig

app = create_app(ProductionConfig)

with app.app_context():
    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.methods} {rule.rule}")