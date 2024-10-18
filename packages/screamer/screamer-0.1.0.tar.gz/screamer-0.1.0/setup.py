from skbuild import setup

setup(
    name="screamer",
    version="0.1.0",
    description="Screamingly fast streaming indicators with C++ performance and Python simplicity.",
    long_description="Screamer is a high-performance Python library designed for efficient streaming indicator algorithms. Built with a core of optimized C++ code and integrated through Python bindings, Screamer delivers lightning-fast computations for real-time data processing. The library is perfect for real-time algorithmic trading applications that need low-latency indicators.",
    author="Thijs van den Berg",
    author_email="thijs@sitmo.com",
    packages=["screamer"],
    cmake_install_dir="screamer",
    python_requires='>=3.9',
)