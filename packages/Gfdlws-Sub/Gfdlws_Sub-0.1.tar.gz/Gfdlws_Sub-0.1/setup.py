from setuptools import setup, find_packages

setup(
    name="Gfdlws_Sub",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "websockets",  # Add other dependencies here
    ],
    author="Surendran M",
    description="A WebSocket client library for real-time streaming",
    url="https://github.com/yourusername/my_websocket_lib",
)
