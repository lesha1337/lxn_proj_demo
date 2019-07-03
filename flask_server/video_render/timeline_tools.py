import datetime
import pandas as pd
import numpy as np
import subprocess
import itertools


def ms2time_for_vtt(time_ms):
    """
    convert milliseconds to hour, minute, seconds, milliseconds
    :param time_ms:
    :return:
    """
    time_s = time_ms/1000
    hour = time_s // 3600
    minute = int(time_s % 3600 // 60)
    second = int(time_s % 3600 % 60)
    millisecond = int(time_s % 3600 % 60 % 1*1000)
    return int(hour), int(minute), int(second), int(millisecond)


def extract_timeline(raw_list, equipment_list, time_gap=500):
    """
    Extracts timeline of each equipment.

    Args:
        raw_list: list
            in first column - time in ms, in second - number from qr decoded
            third - tuple (x, y, w, h) w, h - width and height respectively

        equipment_list: list
            first column - decoded qr, second - time in millisecond

        time_gap: int
            If there no QR code in time_gap in ms, next event

    Returns:
        timeline_list: deque
            first column - start time, second column - end time, third one - equipment
            name.
    """
    if len(raw_list) == 0:
        return []

    # Extracting area of barcode
    boxes = raw_list[1]#np.array([[*coord] for _, _, coord in raw_list])
    raw_timeline = np.c_[raw_list[0], raw_list[1][:, 2]*raw_list[1][:, 3]]
    # Creating raw dataframe
    raw_df = pd.DataFrame(raw_timeline, columns=['time', 'qr', 'area'])
    equipment_df = pd.DataFrame(equipment_list, columns=['qr', 'item'])
    # equipment_df = pd.read_csv('Communication_room_Equipment.csv', index_col = False)

    sorted_time = np.sort(raw_df.time.unique())
    dbg_count = 0
    index_to_drop = []
    # drop rows in case of simultaneous detection
    df_unique_val, df_unique_counts = np.unique(raw_df.time.values,
                                                return_counts=True)
    for time, time_counts in zip(df_unique_val, df_unique_counts):
        if time_counts > 1:
            max_area = raw_df[raw_df['time'] == time]['area'].max()
            filter_by_area = raw_df[raw_df['time'] == time]['area'] != max_area
            index_to_drop.append(filter_by_area[filter_by_area].index.tolist())
            dbg_count += filter_by_area.shape[0] - 1

    merged_index_to_drop = list(itertools.chain.from_iterable(index_to_drop))

    raw_df.drop(raw_df.index[merged_index_to_drop],inplace=True)
    raw_df.sort_values(by=['time'], inplace=True)

    in_frame_crit = ((sorted_time[1:] - sorted_time[:-1]) < time_gap) == False
    change_qr_crit = abs(raw_df['qr'].values[1:] - raw_df['qr'].values[:-1]) != 0

    time_index_of_qr_end = np.where(in_frame_crit | change_qr_crit==True)[0]
    time_index_of_qr_end = np.append(0, time_index_of_qr_end)

    qr_data = str(equipment_df.iloc[equipment_df['qr'].values.astype(int)
                                    == raw_df.qr.values[raw_df.time.values ==
                                                        sorted_time[0]][0]]['item'].values[0])

    timeline_list = []
    for begin_detect, end_detect \
            in zip(time_index_of_qr_end[:-1], time_index_of_qr_end[1:]):
        begin_detect += 1
        end_detect += 1
    #     print(ms2time_for_vtt(sorted_time[begin_detect - 1]), ms2time_for_vtt(sorted_time[end_detect - 1]))
        
        time_ms = sorted_time[begin_detect]
        # detected_qr = raw_df.qr_data.values[raw_df.time.values==time_ms][0]
        detected_qr = raw_df[raw_df.time.values == time_ms]['qr'].unique()
        qr_data = ''
        for value in detected_qr:
            item = equipment_df.iloc[equipment_df['qr'].values.astype(int) == value]['item'].values[0]
            qr_data += str(item) + '_'
        timeline_list.append([sorted_time[begin_detect], sorted_time[end_detect], qr_data[:-1]])

    qr_data = str(equipment_df.iloc[equipment_df['qr'].values.astype(int)
                                    == raw_df.qr.values[raw_df.time.values
                                                        == sorted_time[-1]][0]]['item'].values[0])
    timeline_list.append([sorted_time[end_detect], sorted_time[-1], qr_data])

    return timeline_list

def timeData_conv(timeline):
    timeData = []
    for timeEvent in timeline:
        timeData.append({'timestamp': np.round(timeEvent[0]/1000, 3), 'objectName': timeEvent[2]})
    return timeData


# def ms_to_timestamp(fname, timeline):
#     ffmpeg_get_mediafile_length = [
#         'sh', '-c', 'ffmpeg -i "$1" 2>&1 | grep Duration | awk \'{print $2}\' | tr -d ,',
#          '_', fname]
#     ffmpeg_get_creation_time = [
#         'sh', '-c', 'ffmpeg -i "$1" 2>&1 | grep creation_time | awk \'{print $3}\' | tr -d ,',
#          '_', fname]
#     video_length = subprocess.Popen(ffmpeg_get_mediafile_length,
#                                 stdout = subprocess.PIPE
#                                 ).stdout.read().decode("utf-8").replace('\n', '')
#     creation_time = subprocess.Popen(ffmpeg_get_creation_time,
#                                 stdout = subprocess.PIPE
#                                 ).stdout.read().decode("utf-8").split('\n')
#     if len(creation_time) < len(creation_time[0]):
#         creation_time = creation_time[0]
