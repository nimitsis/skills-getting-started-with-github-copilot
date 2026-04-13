"""Tests for main routes."""
import pytest


def test_root_redirect(client):
    """Test root endpoint redirects to static index.html."""
    # Arrange
    # No special arrangement needed

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/static/index.html"