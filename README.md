# MirrorrDataExtraction

The repository contains the following codes

- Codes to extract information from the Instagram user's profile page 
- Codes to launch the extractor as a web service
- Demonstration on usage of the extractor
- Demonstration on extracting info and storing it in a Data store

## Setup the Environment

### Google Cloud Platform

1. Navigate to **Compute Engine**  --> **VM Instances**

2. Create an Instance:
    
    - Option 1: Choose New Instance VM and choose Ubuntu 14.04 LTS


    - Option 2: Go to Marketplace and search for **"LAMP Certified by Bitnami"**. This includes other webserver functionalities 
    
3. Access your VM, navigate to Compute Engine --> VM Instances and click **SSH**

4. Clone the repository by typing this on the terminal:

```
git clone https://github.com/timotdsantos/MirrorrDataExtraction.git
```

5. Go to the MirrorDataExtraction folder:

```
cd MirrorDataExtraction
```
    
6. Install the requirements

```
pip install -r requirements.txt
```

7. Download the ChromeDriver, which will be used by Selenium. Make sure it is extracted to the MirrorDataExtraction folder.

```
wget https://chromedriver.storage.googleapis.com/2.42/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
```

   
### Linux Machine

1. Access your Linux machine and go to your terminal

2. Clone the repository by typing this on the terminal:

```
git clone https://github.com/timotdsantos/MirrorrDataExtraction.git
```

3. Go to the MirrorDataExtraction folder:

```
cd MirrorDataExtraction
```
    
4. Install the requirements

```
pip install -r requirements.txt
```

5. Download the ChromeDriver, which will be used by Selenium. Make sure it is extracted to the MirrorDataExtraction folder.

```
wget https://chromedriver.storage.googleapis.com/2.42/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
```    

### Running the Quick Demo Notebook

Make sure you have jupyter-notebook installed

``` 
# Update your pip
pip install -U pip setuptools
```

Once pip is updated, download jupyter notebook
```
# Python2
pip install jupyter
# Python 3
pip3 install jupyter
```

Launch Jupyter Notebook

```
# Type the code in your terminal
jupyter-notebook
# To keep the notebook server running persistently
nohup jupyter-notebook &
```

Launch the notebook **Extract Profile - Quick Demo.ipynb**. This should bring you to the notebook and just follow the steps to see the features.

### Running the Web App 

Go to the terminal and navigate to the MirrorDataExtraction folder
```
cd MirrorDataExtraction
```

Define the variables for the main web app and database configuration

```
export GOOGLE_APPLICATION_CREDENTIALS='/home/mirroraidev/config.json'
export FLASK_APP=~/MirrorrDataExtraction/main.py
```

Launch the webapp

```
flask run --host=0.0.0.0
# To launch it in the background
nohup flask run --host=0.0.0.0 &
```

You should see a confirmation that flask is running the app and should look like this:

```
flask run --host=0.0.0.0
 * Serving Flask app "/home/mirroraidev/MirrorrDataExtraction/main.py"
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

You will notice that the app will be listening to the port 5000. You can visit the webapp by typing **http://localhost:5000** on the browser. If your public ip is exposed, you can also test the app by going to **http://server.public.ip.address:5000**. 

For demo purposes, there is a server that's set up to test the code ***http://testbucket-217010.appspot.com:5000***.


It will bring you to a welcome page. The instagram profile extractor is available as a POST request in this format:

```
http://server.ip.address/userid/{userid} 
http://testbucket-217010.appspot.com/userid/{userid}
```


