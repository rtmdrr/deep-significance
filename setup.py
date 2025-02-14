from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="deep-signifcance",  # Replace with your own username
    version="0.9.2",
    author="Dennis Ulmer",
    description="Easy Significance Testing for Deep Neural Networks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kaleidophon/deep-significance",
    classifiers=[
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    license="GPL",
    python_requires=">=3.5.3",
    keywords=[
        "machine learning",
        "deep learning",
        "reinforcement learning",
        "computer vision",
        "natural language processing",
        "nlp",
        "rl",
        "cv",
        "statistical significance testing",
        "statistical hypothesis testing",
        "pytorch",
        "tensorflow",
        "numpy",
        "jax",
    ],
    packages=find_packages(exclude=["docs", "dist"]),
)
