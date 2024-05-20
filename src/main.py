#!/usr/bin/env python

import sys
import os

# Add the directory containing the 'dagger' package to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import dagger
from dagger.pipelines import (
    lint_pipeline,
    test_pipeline,
    security_scan_pipeline,
    fix_vulnerabilities
)

if __name__ == "__main__":
    dagger.run([
        lint_pipeline,
        test_pipeline,
        security_scan_pipeline,
        fix_vulnerabilities
    ])
