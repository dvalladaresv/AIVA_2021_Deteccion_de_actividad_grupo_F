import glob
import csv
import re
import sys

sys.path.append("../app/")
from affluence_counter import AffluenceCounter

if __name__=="__main__":
    videos_path = sorted(glob.glob("../../videos/*.mpg"))
    # Sorted imgs path
    r = re.compile(r"(\d+)")

    videos_path.sort(key=lambda x: int(r.search(x).group(1)))

    count = 1
    for video_path in videos_path:
        with open('./results.csv', 'w', newline='') as csvfile:
            fieldnames = ['id', 'enter', 'noenter']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            app = AffluenceCounter(video_path)
            count_enter, count_noenter, time_process = app.process_video()
            writer.writerow({'id': count, 'enter': count_enter, 'noenter': count_noenter})
        count = count + 1
