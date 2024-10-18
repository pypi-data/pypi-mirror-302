# Browseek: Advanced Multi-Browser Automation Library

Browseek is a sophisticated Python library designed for advanced multi-task and multi-browser automation. It provides a robust solution for managing complex web automation scenarios, including request redirection, DNS security, CAPTCHA handling, device simulation, and fine-grained network control.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Concepts](#core-concepts)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Examples](EXAMPLES.md)
- [Contributing](CONTRIBUTING.md)
- [Testing](TESTING.md)
- [Changelog](CHANGELOG.md)

## Installation

```bash
pip install browseek
```

## Quick Start

```python
from browseek import BrowserRouter

# Initialize the router
router = BrowserRouter()

# Add browser instances
router.add_browser("chrome", count=2)
router.add_browser("firefox", count=1)

# Use the router to perform a task
result = router.execute("https://example.com", lambda page: page.title())
print(result)

# Clean up
router.close()
```

## Core Concepts

- **BrowserRouter**: The main class for managing browser instances and routing requests.
- **BrowserInstance**: Represents a single headless browser instance.
- **Route**: Defines rules for how specific requests should be handled.
- **Task**: A unit of work to be executed in a browser instance.

## API Reference

### BrowserRouter

```python
class BrowserRouter:
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the BrowserRouter with optional configuration."""

    def add_browser(self, browser_type: str, count: int = 1, options: Dict[str, Any] = None):
        """Add browser instances to the router."""

    def remove_browser(self, browser_id: str):
        """Remove a browser instance from the router."""

    def add_route(self, pattern: str, handler: Callable):
        """Add a route for specific URL patterns."""

    def execute(self, url: str, task: Callable, timeout: int = 30):
        """Execute a task on a suitable browser instance."""

    def close(self):
        """Close all browser instances and clean up resources."""
```

### BrowserInstance

```python
class BrowserInstance:
    def __init__(self, browser_type: str, options: Dict[str, Any] = None):
        """Initialize a browser instance."""

    def navigate(self, url: str):
        """Navigate to a specific URL."""

    def execute_script(self, script: str):
        """Execute JavaScript in the browser context."""

    def take_screenshot(self) -> bytes:
        """Capture a screenshot of the current page."""
```

## Configuration

Browseek can be configured via a Python dictionary or a YAML file:

```python
config = {
    "max_concurrent_browsers": 5,
    "default_timeout": 30,
    "retry_attempts": 3,
    "proxy": {
        "enabled": True,
        "rotate_on_failure": True
    }
}

router = BrowserRouter(config)
```

## Examples

For detailed examples of how to use Browseek for various scenarios, please refer to the [EXAMPLES.md](EXAMPLES.md) file.

## Contributing

We welcome contributions to Browseek! Please see our [Contributing Guide](CONTRIBUTING.md) for more information on how to get started.

## Testing

Browseek uses the `unittest` framework for testing. For information on running tests and writing new tests, please refer to the [TESTING.md](TESTING.md) file.

## Changelog

For a detailed list of changes and version history, please see the [CHANGELOG.md](CHANGELOG.md) file.
