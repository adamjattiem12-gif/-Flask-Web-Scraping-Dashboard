"""TC-BE-01: Does the Flask app import/start at all?"""
import importlib
import sys


def test_app_module_imports():
    sys.modules.pop("app", None)
    importlib.import_module("app")
