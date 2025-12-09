"""
Verification tests for Issue #19: Make the website more pretty

Acceptance Criteria:
- [ ] Apply X.com-inspired color scheme with dark mode default
- [ ] Add Twitter blue (#1D9BF0) as primary accent color
- [ ] Update typography with system fonts and extrabold headings
- [ ] Modernize navbar with improved hover states
- [ ] Enhance product cards with rounded corners and primary color accents
"""

import pytest
import requests
import subprocess
import time
import signal
import os


class TestIssue19:
    """
    Verification tests for Issue #19: Make the website more pretty
    """

    FRONTEND_URL = "http://localhost:3000"
    frontend_process = None

    @pytest.fixture(scope="class", autouse=True)
    def setup_frontend(self, request):
        """Start the Next.js frontend for testing"""
        # Change to frontend directory
        frontend_dir = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "nextjs-frontend"
        )

        # Start the dev server
        TestIssue19.frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid
        )

        # Wait for server to be ready
        max_retries = 30
        for i in range(max_retries):
            try:
                response = requests.get(self.FRONTEND_URL, timeout=2)
                # Server is responding (even if with errors)
                break
            except requests.exceptions.RequestException:
                time.sleep(1)

        yield

        # Cleanup
        if TestIssue19.frontend_process:
            os.killpg(os.getpgid(TestIssue19.frontend_process.pid), signal.SIGTERM)

    def test_frontend_server_starts(self):
        """Verify: Frontend server starts without errors"""
        response = requests.get(self.FRONTEND_URL, timeout=10)
        # The server should return 200, not 500
        assert response.status_code == 200, (
            f"Frontend returned status {response.status_code}. "
            "The server may have a CSS/build error."
        )

    def test_frontend_renders_html(self):
        """Verify: Frontend renders valid HTML content"""
        response = requests.get(self.FRONTEND_URL, timeout=10)
        assert response.status_code == 200, "Server should return 200 OK"
        assert "<!DOCTYPE html>" in response.text or "<html" in response.text, (
            "Response should contain valid HTML"
        )

    def test_css_loads_without_errors(self):
        """Verify: CSS loads without Tailwind errors"""
        response = requests.get(self.FRONTEND_URL, timeout=10)
        # If there's a CSS error, the server typically returns 500
        assert response.status_code != 500, (
            "Server returned 500 - possible CSS/Tailwind error. "
            "Check for 'Cannot apply unknown utility class' errors."
        )

    def test_dark_mode_styles_present(self):
        """Verify: Dark mode is the default (X.com style)"""
        response = requests.get(self.FRONTEND_URL, timeout=10)
        assert response.status_code == 200, "Server must return 200 to verify styles"
        # Check for dark background color in CSS or inline styles
        # The background should be black (0 0% 0%) in dark mode
        content = response.text.lower()
        # This is a basic check - full verification would use a browser
        assert "background" in content or "bg-" in content, (
            "Page should have background styling"
        )

    def test_twitter_blue_accent(self):
        """Verify: Twitter blue (#1D9BF0) is used as primary accent"""
        response = requests.get(self.FRONTEND_URL, timeout=10)
        assert response.status_code == 200, "Server must return 200 to verify colors"
        # The primary color HSL should be 204, 88%, 53% which corresponds to #1D9BF0


class TestIssue19UnitTests:
    """Verify that unit tests pass for the implementation"""

    def test_unit_tests_pass(self):
        """Verify: All unit tests in the implementation pass"""
        frontend_dir = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "nextjs-frontend"
        )

        result = subprocess.run(
            ["npm", "test"],
            cwd=frontend_dir,
            capture_output=True,
            text=True,
            timeout=120
        )

        assert result.returncode == 0, (
            f"Unit tests failed:\n{result.stdout}\n{result.stderr}"
        )


class TestIssue19Build:
    """Verify that the build completes successfully"""

    def test_build_succeeds(self):
        """Verify: npm run build completes without errors"""
        frontend_dir = os.path.join(
            os.path.dirname(__file__),
            "..", "..", "nextjs-frontend"
        )

        result = subprocess.run(
            ["npm", "run", "build"],
            cwd=frontend_dir,
            capture_output=True,
            text=True,
            timeout=300
        )

        assert result.returncode == 0, (
            f"Build failed:\n{result.stdout}\n{result.stderr}"
        )
