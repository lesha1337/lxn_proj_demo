from pyzbar import pyzbar
import argparse
import cv2
import matplotlib.pyplot as plt
import datetime
import numpy as np
from collections import deque
import multiprocessing as mp
import time
#from tqdm import tqdm_notebook as tqdm

OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "boosting": cv2.TrackerBoosting_create,
    "mil": cv2.TrackerMIL_create,
    "tld": cv2.TrackerTLD_create,
    "medianflow": cv2.TrackerMedianFlow_create,
    "mosse": cv2.TrackerMOSSE_create
}

BOUND_BOX_LIMITS = {
    'x_left': 200,
    'x_right': 1500,
    'y_bottom': 150,
    'y_top': 800
}

def get_tracker(name='mosse', trackers=OPENCV_OBJECT_TRACKERS):
    return trackers[name]()

def get_barcode(image):
    detect_status = True
    barcode = 0
    try:
        barcodes = pyzbar.decode(image)
        barcode = barcodes[0]

    except:
        detect_status = False
        
    return barcode, detect_status
                
def process_video(fname, tracker=get_tracker(), bound_box_limits=BOUND_BOX_LIMITS,
                          exit_tracker_value=48, skipped_frames=10):
    #print(type(bound_box_limits), bound_box_limits)
    x_left, x_right, y_bottom, y_top = bound_box_limits.values()
    
	
    cv2_video_capture = cv2.VideoCapture(fname)
    video_capture_status,image = cv2_video_capture.read()

    # Get FPS and total number of frames
    fps = cv2_video_capture.get(cv2.CAP_PROP_FPS)
    nframes = np.int(cv2_video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    # Create progress bar, convert units into seconds
    ##progress_bar = tqdm(total=1000*nframes//fps, initial=0)
    

    current_frame = 0
    
    output_data_boxes = np.zeros((nframes, 4))
    output_qr_data = np.zeros((nframes, 2), dtype='S15')
    
    initial_bound_box = None
    while current_frame <= nframes:

        if initial_bound_box is not None:

            video_capture_status,image = cv2_video_capture.read()
            # grab the new bounding box coordinates of the object
            (tracker_update_status, box) = tracker.update(image)

            # check to see if the tracking was a video_capture_status
            if tracker_update_status:
                (x, y, w, h) = box
                output_data_boxes[current_frame] = [*box]
                output_qr_data[current_frame] = [current_frame*1000//fps, qr_data]

                if ((x < x_left) or (x > x_right)) or ((y < y_bottom) or (y > y_top)):
                    initial_bound_box = None

            current_frame += 1
            #progress_bar.update(int(1000//fps))
            if current_frame % exit_tracker_value == 0:
                initial_bound_box = None
            continue

        if current_frame % skipped_frames != 0:
            video_capture_status,image = cv2_video_capture.read()
            current_frame += 1
            #progress_bar.update(int(1000//fps))
            continue


        video_capture_status,image = cv2_video_capture.read()


        if video_capture_status:
            barcode, detect_status = get_barcode(image)
            
        if (video_capture_status and detect_status):
            initial_bound_box = barcode.rect
            #initializing of a tracker
            
            tracker = OPENCV_OBJECT_TRACKERS['mosse']() #Type of tracker
            tracker.init(image, initial_bound_box)
            
            qr_data = barcode.data #.decode("utf-8")
            #progress_bar.set_description(qr_data.decode("utf-8"))

        current_frame += 1
        #progress_bar.update(int(1000//fps)) #updates progressbar
       
    non_zeros = (output_data_boxes[:, 0]!=0)
    output_data_boxes = output_data_boxes[non_zeros].astype(int)
    output_qr_data = output_qr_data[non_zeros, :].reshape((non_zeros.sum(), 2)).astype(float).astype(int)
    
    print(output_data_boxes.shape, output_qr_data.shape)
    
    return [output_qr_data, output_data_boxes]


def star_qr_decode_pyzbar(cit):
    """
    convert [count, image] into
    qr_decode_pyzbar(count, image)
    """
    return qr_decode_pyzbar(*cit)


def qr_decode_pyzbar(image, count=None, nofile=True):
    """
    Search for QRcode in image.

    Args:
        image: input image. Probably ndarray

        count: int
            count for cycle function called from

        nofile: bool
            Return image with boxes or not.
    Returns:
        count: count
            if count is not None. Else 0.

        image: ndarray
            if nofile=True. Else 0.

        detected_barcodes: deque
            deque with detected barcodes

        barcode_pos: deque(list)
            for each element there is list which contains (x, y, w, h) where w, h is width and height
    """
    # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray_image = cv2.resize(gray_image, (640, 360))
    barcodes = pyzbar.decode(image)
    detected_barcodes = deque()
    barcodes_areas = deque()
    barcode_pos = deque()
    (x, y, w, h) = 0, 0, 0, 0
    # loop over the detected barcodes
    for barcode in barcodes:
        # extract the bounding box location of the barcode and draw the
        # bounding box surrounding the barcode on the image
        (x, y, w, h) = barcode.rect
        # Probably pass list of coordinates of qr
        barcode_pos.append((x, y, w, h))
        barcodes_areas.append(w*h)
        # the barcode data is a bytes object so if we want to draw it on
        # our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        # draw the barcode data and barcode type on the image
        if nofile is False:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        detected_barcodes.append(barcodeData)
    return_list = []
    if count is None:
        return_list.append(0)
    else:
        return_list.append(count)

    if nofile:
        return_list.append(0)
    else:
        return_list.append(image)

    return_list.append(detected_barcodes)
    return_list.append(barcode_pos)
    return return_list
