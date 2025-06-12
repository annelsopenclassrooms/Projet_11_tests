# gudlift-registration

1. Why


    This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is the keep things as light as possible, and use feedback from the users to iterate.

2. Getting Started

    This project uses the following technologies:

    * Python v3.x+

    * [Flask](https://flask.palletsprojects.com/en/1.1.x/)

        Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need. 
     

    * [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

        This ensures you'll be able to install the correct packages without interfering with Python on your machine.

        Before you begin, please ensure you have this installed globally. 


3. Installation

- Clone the project

    ```bash
    git clone https://github.com/OpenClassrooms-Student-Center/Python_Testing.git
    cd Python_Testing/
    ```
- Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```
    To deactivate type <code>deactivate</code>.

- Install the dependencies:

    Rather than hunting around for the packages you need, you can install in one step.
   ```sh
   pip install -r requirements.txt
   ```
    This will install all the packages listed in the respective file.
    If you install a package, make sure others know by updating the requirements.txt file. An easy way to do this is <code>pip freeze > requirements.txt</code>

- Flask requires that you set an environmental variable to the python file. However you do that, you'll want to set the file to be <code>server.py</code>. Check [here](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application) for more details

- You should now be ready to test the application. In the directory, type either <code>flask run</code> or <code>python -m flask run</code>. The app should respond with an address you should be able to go to using your browser.

4. Current Setup

    The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). This is to get around having a DB until we actually need one. The main ones are:
     
    * competitions.json - list of competitions
    * clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.

5. Testing

    You are free to use whatever testing framework you like-the main thing is that you can show what tests you are using.

    We also like to show how well we're testing, so there's a module called 
    [coverage](https://coverage.readthedocs.io/en/coverage-5.1/) you should add to your project.

6. Branches nomenclature

    The branches created to resolve the issues from the original repo are named:

    <code>iss&lt;number&gt;-&lt;type&gt;-&lt;descriptive-name&gt;</code>

    The others branches are named:

    <code>&lt;type&gt;/&lt;descriptive-name&gt;</code>

    Where **`type`** is one of: `Feature`, `Bug`, or `Improvement`.
