import os
from os import listdir
from os.path import isfile, join
from pathlib import Path
import cv2
import glob
import shutil
import time
import os



class Helper:

    def get_frames_margin(self, videos, total):
        '''
        claculate the margin between the frames we save by calculating the total number of frames we have and
        the total we want save
        '''
        total_frames = 0
        for v in videos:
            cap = cv2.VideoCapture(v)
            total_frames += int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        margin = total_frames // total
        margin = margin if margin > 0 else 1
        return margin


class PreparingDataset:
    '''
    Take list of videos, convert them into frames, using previous model to generate annotaions so
    we can adjust them using labelimg and retrain them so we increase the accuarcy
    '''

    def __init__(self, config):
        self.config = config
        self.herlper = Helper()
        self.videos = []
        self.frames_margin = 5

    def preparing_data(self):
        '''
        1. change path to project path if exist
        2. prepare videos patha
        '''

        if self.config.get('project_path'):
            os.chdir(self.config['project_path'])

        videos = [f"{self.config['videos_folder_name']}/{f}" for f in listdir(self.config['videos_folder_name']) if
                  isfile(join(self.config['videos_folder_name'], f))]
        self.videos = [f for f in videos if f[-3:] in self.config['videos_extensions']]

        # create saving folder if not exist
        Path(self.config['saving_path']).mkdir(parents=True, exist_ok=True)

        # get the frames margin
        self.frames_margin = self.herlper.get_frames_margin(self.videos, self.config['frames_number'])

    def preprocessing(self):
        '''
        read videos and convert them into frames using the configrations
        '''
        count = 0
        i = 0

        # Create a video capture object, in this case we are reading the video from a file
        for video in self.videos:
            vid_capture = cv2.VideoCapture(video)

            while (vid_capture.isOpened()):
                ret, frame = vid_capture.read()
                if ret == True:
                    if i % self.frames_margin == 0:
                        cv2.imwrite(os.path.join(self.config['saving_path'], f'frame{count}.jpg'), frame)
                        key = cv2.waitKey(20)
                        count += 1
                        if count % 10 == 0:
                            print(count)
                    i += 1
                    if key == ord('q') or count >= self.config['frames_number']:
                        break
                else:
                    break

        # Release the video capture object
        vid_capture.release()
        cv2.destroyAllWindows()

    def processing(self):
        '''
        generate annotaions using previous model
        '''

        bashCommand = f"python yolov5/detect.py --weights {self.config['model_path']} --img {int(self.config['resolution'])} --conf {float(self.config['conf'])} --source {self.config['saving_path']} --save-txt --project {self.config['saving_path']}"
        os.system(bashCommand)

    def post_processing(self):
        '''
        organize files so we can use labeling directly without need of any manual work
        '''

        # move text files to frames folder
        data_path = os.path.join(os.path.join(Path(self.config['saving_path']), '**\\labels'), '*txt')
        all_data = glob.glob(data_path)
        for file in all_data:
            try:
                shutil.move(file, Path(self.config['saving_path']))
            except Exception as e:
                print(e)

        # move classes.txt file to frames folder
        shutil.copy(self.config['classes_file_path'], self.config['saving_path'])

        # remove any folder
        files = os.listdir(Path(self.config['saving_path']))
        folders = [f for f in files if not (f.endswith('jpg') or f.endswith('txt'))]
        for folder in folders:
            shutil.rmtree(os.path.join(Path(self.config['saving_path']), folder))

    def run(self):
        print("------------------------------- preparing required data/ configrations -------------------------------")
        self.preparing_data()

        print(
            "------------------------------- read videos and convert them into frames -------------------------------")
        self.preprocessing()

        print(
            "------------------------------- generate annotaions using previous model -------------------------------")
        self.processing()

        try:
            time.sleep(2)
            print("------------------------------- organize files -------------------------------")
            self.post_processing()
        except:
            time.sleep(5)
            print("------------------------------- re-organize files -------------------------------")
            self.post_processing()
