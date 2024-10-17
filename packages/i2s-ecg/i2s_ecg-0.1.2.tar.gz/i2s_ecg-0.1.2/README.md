# ecg_i2s

Transform ECG Images to Signals

You can use this code to transform ECG images into 1D signals. Follow the instructions below to get started.

## Setup Instructions

1. **Create a Conda Environment**

We recommend using Python version 3.9.7.
   ```
   conda create -n ecg python=3.9.7
   ```
Then you should activate the environment using:
   ```
   conda activate ecg
   ```

2. **Install Required Packages**

Install the necessary packages using the following:
   
   - `scikit-learn`
   - `scikit-image`
   - `unzip`
   - `joblib`
   - `pandas`
   - `matplotlib`
   - `natsort`
   - `streamlit==1.37.0`

   Alternatively, you can use the `requirements.txt` file to install the required packages by running:
   
   ```bash
   pip install -r requirements.txt
   ```

3. **Download the Pre-Trained Models**

you should find your app.py file, which is the main file of the project.
In the app.py file, you can modify the code to fit your own ECG image.
You should substitute the path of your own ECG image and the path of the pre-trained models.

4. **Run the Code**

you can run the code by:
```
streamlit run app.py
```

5. **Open the Webpage**

The webpage will be opened in your default browser.
if you can't open the webpage, you can update the streamlit version==1.37.0.

if you run the code with AxiosError: Request failed with status code 403, you can use the following command to run the code:

```
streamlit run app.py --server.enableXsrfProtection=false
```