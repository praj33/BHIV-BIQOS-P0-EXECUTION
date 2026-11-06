"""
Pytest configuration and shared fixtures for CLO Agent test suite.
"""

import os
import sys
import pytest
from fastapi.testclient import TestClient

# Add project root to sys.path so 'clo' package is importable
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from clo.runtime.api import app, registry, reasoning_engine, mdu_adapter, tantra_adapter, vajra_adapter, insightflow_adapter


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def canonical_registry():
    return registry


@pytest.fixture
def engine():
    return reasoning_engine


@pytest.fixture
def mdu():
    return mdu_adapter


@pytest.fixture
def tantra():
    return tantra_adapter


@pytest.fixture
def vajra():
    return vajra_adapter


@pytest.fixture
def insightflow():
    return insightflow_adapter

