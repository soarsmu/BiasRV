import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bias_rv",
    version="0.0.8",
    author="Zhou Yang",
    author_email="zyang@smu.edu.sg",
    description="A package to generate biased mutants for texts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/soarsmu/BiasFinder",
    packages=setuptools.find_packages(),
    include_package_data=True,
   package_data={
      'bias_rv': ['asset/gender_associated_word/*.txt', 'asset/gender_computer/*.csv'],
   },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

