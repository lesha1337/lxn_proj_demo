from video_render.barcode_functions import process_video
from video_render.timeline_tools import extract_timeline
from video_render.timeline_tools import timeData_conv

import pandas as pd

def get_barcode_time(fname, equipment_list=pd.read_csv('video_render/qr_data.csv', index_col = False).values.tolist(), 
                      nframes=1, bs=100, pn=7,
                      output_video_name='default'):
    raw_deque =  process_video(fname)
    timeline = extract_timeline(raw_deque, equipment_list)
    return timeData_conv(timeline)


if __name__ == '__main__':
    import pandas as pd
    equipment_list = pd.read_csv('Communication_room_Equipment.csv', index_col = False).values.tolist()
    print( get_barcode_time('input/Комната_связи.MP4', equipment_list, output_video_name='no'))
