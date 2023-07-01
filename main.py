# importing required libraries
import cv2
import numpy as np
import time
from env import *
import collections
import pickle
import sklearn

def skip_frames(fps,duration):
    return round(duration/(1000/fps))

SKIP_FR = skip_frames(FPS,MIN_COLOR_DURATION)

# Load the saved model
LOADED_MODEL = pickle.load(open(MODEL_FILENAME, 'rb'))

# crops and returns the center part of frame
def crop_frame_center(img,width_scale=0.25,height_scale=0.25):
    center = img.shape
    h,w=center[0]*height_scale,center[1]*width_scale
    x = center[1]/2 - w/2
    y = center[0]/2 - h/2

    return img[int(y):int(y+h), int(x):int(x+w)]

# map color pixel values to closest valid pixel values
def closest_valid_value(input_value, valid_dec_codes = VALID_DEC_CODES):
  dec_codes = np.array(valid_dec_codes)
  min = (np.abs(dec_codes - input_value)).min()
  if min <= THRESHOLD:
    i = (np.abs(dec_codes - input_value)).argmin()
    return dec_codes[i]
  else:
    return -1

def closest_rgb(r,g,b):
    r_valid = closest_valid_value(r, VALID_DEC_CODES + [192])
    g_valid = closest_valid_value(g, VALID_DEC_CODES + [192])
    b_valid = closest_valid_value(b, VALID_DEC_CODES + [192])

    # check if all values is 192 else compute again without 192 (silver corner case)
    if len(set([r_valid, g_valid, b_valid])) == 1 and r_valid == 192:
        return (r_valid, g_valid, b_valid)
    else:
        r_valid = closest_valid_value(r)
        g_valid = closest_valid_value(g)
        b_valid = closest_valid_value(b)
    
        return (r_valid, g_valid, b_valid)


# Function to find dominant color from frame from webcam
def find_dominant_color(frame):
    # Convert the frame from BGR to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Reshape the frame to a flattened array of pixels
    pixels = frame.reshape(-1, 3).astype(np.float32)

    # Define the criteria for K-means clustering
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

    # Perform K-means clustering
    _, _, centers = cv2.kmeans(pixels, 1, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Convert the center values to the uint8 data type
    center_color = np.uint8(centers[0])
    r, g, b = center_color

    return r, g, b

# Find partial patterns
def partialMatch(subset):
    for pattern in valid_pattern:
        j=0
        while(j<len(subset)):
            if subset[j]!=pattern[j]:
                break
            j+=1
        if j==len(subset):
            print("Partial Pattern ", valid_pattern[pattern])
            return

# find the valid pattern for the given 4 color sequence
def decode_sequence(seq):
   return valid_pattern.get(tuple(seq), 'Invalid')

# predict color from webcam rgb
def predict_rgb(r,g,b):
    new_data = [[r, g, b]] 
    predicted_class = LOADED_MODEL.predict(new_data)
    return predicted_class[0]

def capture_color_sequence(**kwargs):
    
    right = 0
    partial_buffer = collections.deque()
    full_buffer = collections.deque()

    color_seq = []

    if 'video_file' in kwargs:
        # taking input from video file
        vid = cv2.VideoCapture(kwargs['video_file'])
    else:
        # taking the input from webcam
        vid = cv2.VideoCapture(0)

    milliseconds = 0
    prev_time = 0
    while vid.isOpened():
        
        # capturing the current frame
        valid, frame = vid.read()

        # Pattern matchining
        if right==4:
            tup=tuple(full_buffer)
            if tup in valid_pattern:
                if len(partial_buffer)>1 and len(partial_buffer)<=3:
                    partialMatch(tuple(partial_buffer))
                partial_buffer.clear()
                print("Valid Pattern ",valid_pattern[tup])
                full_buffer.clear()
                right=0
            else:
                if len(partial_buffer)>1 and len(partial_buffer)<=3:
                    partialMatch(tuple(partial_buffer))
                    temp=len(partial_buffer)
                    partial_buffer.clear()
                else:
                    print("Invalid Pattern")
                    temp=1
                partial_buffer.append(full_buffer[0])
                while temp:
                    full_buffer.popleft()
                    right-=1
                    temp-=1

        # Break if no frame captured
        if not valid:
            break

        if 'video_file' in kwargs:
            # forward by milliseconds
            milliseconds += MIN_COLOR_DURATION
            vid.set(cv2.CAP_PROP_POS_MSEC, milliseconds)
        else:
            # capture every min color duration 
            curr_time = cv2.getTickCount()
            elapsed_time = (curr_time - prev_time) / cv2.getTickFrequency()
            if elapsed_time < MIN_COLOR_DURATION / 1000:
                continue
            prev_time = curr_time

        # crop only the center part of frame
        frame = crop_frame_center(frame)

        # displaying the current frame
        cv2.imshow("captured frame", frame)

        # find dominant color from frame
        r_estimate, g_estimate, b_estimate = find_dominant_color(frame)

        if 'video_file' in kwargs:
            # finding closest rgb from estimate
            rgb = closest_rgb(r_estimate, g_estimate, b_estimate)
        else:
            # predict the rgb value for webcam input using trained model
            rgb = predict_rgb(r_estimate, g_estimate, b_estimate)

        color = dec_to_color.get(rgb, '404')

        # print((r_estimate,g_estimate,b_estimate), rgb, color)

        color_seq.append(color)

        if color != '404':
            if right>2 and (full_buffer[right-1]==color  and full_buffer[right-2]==color):
                continue
            full_buffer.append(color)
            right=right+1          

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    vid.release()
    cv2.destroyAllWindows()
    return color_seq

print('Color Sequence : ', capture_color_sequence(video_file='SeqOutput_TestVideo_3.avi'))

# seq = capture_color_sequence()
# print(len(seq))
# print(seq)