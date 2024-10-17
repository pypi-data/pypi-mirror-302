import setuptools

setuptools.setup(
    name="streamlit-sortable-list",
    version="0.1.2",
    author="tonyli",
    author_email="renshou753@gmail.com",
    description="Streamlit component to sort a list based on provided input.",
    long_description="A Streamlit component to sort a list, for more information please check https://github.com/renshou753/streamlit-sortable-list",
    long_description_content_type="text/plain",
    url="https://github.com/renshou753/streamlit-sortable-list",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 0.63",
    ],
)
