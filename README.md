# Footy Tipping Automation with Squiggle

## Introduction
This project is a Python-based automation tool for footy tipping, leveraging the Squiggle API to make predictions and manage tips. It's designed to help users automatically update their tips based on the latest predictions and statistics provided by Squiggle.

## Prerequisites
Before you begin, ensure you have met the following requirements:
- Python 3.x installed on your system
- Basic knowledge of Python and command-line operations

## Installation

### Clone the Repository
First, clone this repository to your local machine using Git:

```
git clone https://github.com/myth-0/footytips
cd footytips
```

### Setup a Virtual Environment (Optional but Recommended)
It's a good practice to use a virtual environment for Python projects. 
This keeps dependencies required by different projects separate by creating isolated environments for them. You can create a virtual environment and activate it using:

```
python3 -m venv venv
source venv/bin/activate

# On Windows, use venv\Scripts\activate
```
### Install Dependencies
Install all the necessary Python packages using pip:

```
pip install -r requirements.txt

```
## Running the script
Launch main.py from the footytips directory
```
python3 ./main.py
```
Use the --no-email flag to avoid having the email sent out to you

User Agents must be entered regardless as per Squiggle's API conditions. 
The User Agent App Name is used to identify what your application is.
The User Agent Contact Email is used in the case that Squiggle needs to contact you regarding API usage.


