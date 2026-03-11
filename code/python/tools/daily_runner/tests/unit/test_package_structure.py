"""
Tests for verifying the package structure and imports.

Test ID: 1.T1 - Verify all imports work correctly
"""


class TestPackageImports:
    """Test that all package imports work correctly."""

    def test_import_src_package(self) -> None:
        """Test that the main src package can be imported."""
        import src

        assert hasattr(src, "__version__")
        assert src.__version__ != "0.0.0-dev"

    def test_import_core_package(self) -> None:
        """Test that the core package can be imported."""
        import src.core

        assert src.core is not None

    def test_import_data_package(self) -> None:
        """Test that the data package can be imported."""
        import src.data

        assert src.data is not None

    def test_import_services_package(self) -> None:
        """Test that the services package can be imported."""
        import src.services

        assert src.services is not None

    def test_import_ui_package(self) -> None:
        """Test that the ui package can be imported."""
        import src.ui

        assert src.ui is not None

    def test_import_ui_components_package(self) -> None:
        """Test that the ui.components package can be imported."""
        import src.ui.components

        assert src.ui.components is not None

    def test_import_cli_package(self) -> None:
        """Test that the cli package can be imported."""
        import src.cli

        assert src.cli is not None


class TestPackageMetadata:
    """Test package metadata."""

    def test_version_format(self) -> None:
        """Test that version follows semver format."""
        import src

        version_parts = src.__version__.split(".")
        assert len(version_parts) == 3
        assert all(part.isdigit() for part in version_parts)

    def test_author_defined(self) -> None:
        """Test that author is defined."""
        import src

        assert hasattr(src, "__author__")
        assert src.__author__ == "Yosi Izaq"
