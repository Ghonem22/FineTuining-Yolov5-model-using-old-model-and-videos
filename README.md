# FineTuining-Yolov5-model-using-old-model-and-videos-

Here we have Yolo V5 model that is trained on specific enviroment, but with time this envireoment changes and the model accuarcy decreases.


## So How to re-increase the model accuarcy ?

We can solve this problem by re-training the model on dataset from this new envireoment as follow:  
  1. record some videos for this new enviroment.
  2. Convert this videos randomly into frames, say We will save one frame every 30 frames (we can increase or decrease this number)
  3. label these frames again  using any annotaion tool (we use here labelimage https://github.com/heartexlabs/labelImg)
  4. returin the model on this new dataset
  
### But this process may take a lot of time, so I semi- automated this process to minimize the time I need to re-increase the model accuarcy.


## How I semi- autmated re-training the model?

### Even the model accuarcy decrased, it will recognize some objects and theit locations (say 70% of them), so we can get use of that.
### We can automate converting videos into frames and control the total number of frames we save and maximize margin between the frames.

  1. We need to adjust  hyperparameters in "utilities/configs.yml" to give you more control  :
  
    * videos_folder_name: the path of the folder that contain the videos
    * saving_path: the path of the folders that we will use to save the output
    * model_path: path of the old model
    * classes_file_path: the path of classes.txt file
    * videos_extensions: We will exclude any extendions not included under videos_extensions
    * frames_number: the total number of frames we want to save
    * conf: the old model won't detect any object with lower conf that this threshold
    * resolution: the model will resize frames to this resolution
  
  2. The code will convert the videos into frames in the path you defined (default: frames)
  
  3. We will use the old model to get the predictions for each frame and save result in txt file
  
  4. clean files, and move text files and classes.txt so images and prediction exist in same folder
  
 
## How to run ?

  1. adjusting hyperparameters in config file and arrange your file
  2. in your terminal in the projuct path run: git clone https://github.com/ultralytics/yolov5.git
  3. run python main.py
      
**Then you just need to use labelimage to enhance prdictions and the dataset is ready now**


### Now we have a dataset but using the power of the old model, we need to to manulally increse adjust this dataset and fix any error in predictions (using labelimg)


## In the future:

We Will add training the model to the pipeline

