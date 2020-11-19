# Install Instructions
Make sure to have [Pipenv](https://pipenv.pypa.io/en/latest/basics/) installed:

    pip install pipenv

Navigate to main project folder and run the following command:

    pipenv install

Activate the Pipenv shell:

    pipenv shell

Pipenv is used to create a virtual environment setup with all the dependencies used for this project.

**IMPORTANT** Once in Pipenv shell run the following commands:

    conda install swig
    pip install box2d-py

This is to avoid an issue with some of the Gym environments.


# Running the Poject
Run all files from inside the Pipenv shell:

    pipenv shell


## Note for me
running `pipenv lock` seems to timeout unless I run it in the Pipenv shell...not sure why ¯\\_(ツ)_/¯