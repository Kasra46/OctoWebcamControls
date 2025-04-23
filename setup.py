from setuptools import setup

setup(
    name="OctoPrint-WebcamControl",
    version="1.0.0",
    description="Control webcam settings and stream via SSH",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/OctoPrint-WebcamControl",
    license="AGPLv3",
    packages=["octoprint_webcamcontrol"],
    include_package_data=True,
    install_requires=[
        "OctoPrint>=1.4.0",
        "paramiko>=2.7.2"
    ],
    python_requires=">=3.7,<4"
) 