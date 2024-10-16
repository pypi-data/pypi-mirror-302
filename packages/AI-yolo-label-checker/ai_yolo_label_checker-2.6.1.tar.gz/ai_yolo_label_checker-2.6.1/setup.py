from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="AI_yolo_label_checker",  # tên của gói thư viện
    version="2.6.1",
    description="Thư viện hữu ích của Tuấn Anh.",
    url="https://pypi.org/project/AI-yolo-label-checker/",
    author="Tuấn Anh - Foxconn",
    author_email="nt.anh.fai@gmail.com",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    package_data={"AI_yolo_label_checker": ["IVIS_data/*"]},
    install_requires=["collection", "matplotlib", "numpy", "opencv-python"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # package_dir={"": "ntanh"},
    # packages=find_packages(where="ntanh"),
    entry_points={
        "console_scripts": [
            "AI_yolo_label_checker=AI_yolo_label_checker:runApp",
            "AI_check=AI_yolo_label_checker:runApp",
        ],
    },
)
