from setuptools import setup, find_packages

setup(
    name="bcsl_python",
    version="0.3.0",
    author="Guo, Xianjie",
    author_email="albert.buchard@gmail.com",
    description="Bootstrap-based Causal Structure Learning",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/albertbuchard/bcsl_python",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.18.0",
        "scipy>=1.4.0",
        "scikit-learn>=0.22.0",
        "causal-learn==0.1.3.8",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
