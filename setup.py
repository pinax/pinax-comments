from distutils.core import setup


setup(
    name = "dialogos",
    version = "0.1.dev1",
    author = "Eldarion",
    author_email = "development@eldarion.com",
    description = "a flaggable comments app",
    long_description = open("README.rst").read(),
    license = "BSD",
    url = "http://github.com/eldarion/dialogos",
    packages = [
        "dialogos",
        "dialogos.templatetags",
        "dialogos.tests",
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)
