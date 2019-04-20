# Canopus_AI_Solutions

First Create a Virtual Environment bcz there are major dependency issues:
How to Create Virtual Env:

>>pip install virtualenv

#Folder where u wanna create ur Virtual Env
>>virtualenv some_name

Open cmd and go inside Script Folder which is located in ur VirtualEnv Created Files:

>>activate

>>pip install tensorflow==1.12.2
>>pip install Django==1.9.4
>>pip install google-images-download
>>pip install Pillow==5.4.1
>>pip install opencv-python==3.4.5.20

#After all this we will build keras from source bcz latest pip version of keras has some problems(Do this outside of ur Virtual Env Folder bcz this will become useless once u are done installing):

>>git clone https://github.com/keras-team/keras.git
>>cd keras
>>python setup.py install


>>pip install numpy -U


Still u might need few more packages to run the project that u can figure out on ur own..


Download weights:


Weight1 - >
  https://drive.google.com/open?id=1MXMs4YB98f3ggFUk528Ek0VNEX3alTCb

Weight2 - > https://drive.google.com/file/d/1T-BDuB8KQ97MrnZaOtcgukVyNJfDH8wS/view?usp=sharing


Download and Copy it in DLPart folder.

And u are good to go.
