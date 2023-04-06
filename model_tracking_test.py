import cv2
import collections

def select_roi_callback(event, x, y, flags, param):
    global ref_point, cropping, frame_copy, current_x, current_y

    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point = [(x, y)]
        cropping = True
    elif event == cv2.EVENT_LBUTTONUP:
        ref_point.append((x, y))
        cropping = False
        cv2.rectangle(frame_copy, ref_point[0], ref_point[1], (0, 255, 0), 2)
        cv2.imshow("Select ROI", frame_copy)
    elif event == cv2.EVENT_MOUSEMOVE and cropping:
        current_x, current_y = x, y

def select_roi(video):
    global frame_copy, ref_point, cropping, current_x, current_y

    
    # 从视频中读取第一帧
    _, frame = video.read()
    frame_copy = frame.copy()

    # 定义全局变量
    ref_point = []
    cropping = False
    current_x, current_y = 0, 0

    # 创建窗口，设置鼠标回调
    cv2.namedWindow("Select ROI")
    cv2.setMouseCallback("Select ROI", select_roi_callback)

    # 循环，直到用户选择完 ROI
    while True:
        if not cropping:
            cv2.imshow("Select ROI", frame_copy)
        else:
            temp_frame = frame.copy()
            cv2.rectangle(temp_frame, ref_point[0], (current_x, current_y), (0, 255, 0), 2)
            cv2.imshow("Select ROI", temp_frame)

        key = cv2.waitKey(1) & 0xFF
        # enter以确认选择
        if key == 13:
            break

    cv2.destroyAllWindows()

    # 计算选择的边界框
    x1, y1 = ref_point[0]
    x2, y2 = ref_point[1]
    bbox = (min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))
    
    return bbox

def draw_box(frame, bbox, color):
    x, y, width, height = [int(i) for i in bbox]
    cv2.rectangle(frame, (x, y), (x + width, y + height), color, 2)

def track_object(video, tracker):
    
    # 帧缓冲区，用于在跟踪失败时重新初始化跟踪器
    buffer_length = 30
    frame_buffer = collections.deque(maxlen=buffer_length)
    
    while True:
        # 从视频读取下一帧
        _, frame = video.read()
        # 更新跟踪器并获取物体的新边界框
        success, bbox = tracker.update(frame)

        if success:
            # 如果跟踪成功，绘制边界框
            draw_box(frame, bbox, (0, 255, 0))
            # 将当前帧及其对应的边界框添加到缓冲区
            frame_buffer.append((frame.copy(), bbox))  
        else:
            cv2.putText(frame, "Tracking failed", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
            # tracker2 = cv2.TrackerKCF_create()
            # tracker2.init(*frame_buffer[0])
            # for old_frame, old_bbox in frame_buffer:
            #     success, bbox = tracker2.update(old_frame)
            # success, bbox = tracker2.update(frame)    
            # if success:
            #     draw_box(frame, bbox, (0, 255, 0))
            #     x, y, width, height = [int(i) for i in bbox]
            #     cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255), 2)
            # if not success:
            #     # 如果仍然跟踪失败，显示提示信息
            #     cv2.putText(frame, "Tracking failed", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        # 显示帧
        cv2.imshow("Frame", frame)

        # esc以退出循环
        if cv2.waitKey(1) & 0xFF == 27:
            break

    video.release()
    cv2.destroyAllWindows()

def main():
    # 读取视频文件
    video_path = "cvtest1.mp4"
    video = cv2.VideoCapture(video_path)
    # 创建一个 KCF 跟踪器
    tracker = cv2.TrackerKCF_create()

    # 跟踪对象初始位置
    bbox = select_roi(video)
    # 初始化跟踪器
    tracker.init(video.read()[1], bbox)
    track_object(video, tracker)

if __name__ == "__main__":
    main()
