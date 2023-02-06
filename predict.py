import time
import cv2
import numpy as np
from openni import openni2
from retinaface import Retinaface

if __name__ == "__main__":
    retinaface = Retinaface()

    # computer_camera 为电脑自带的摄像头或者nvc免驱动摄像头
    # astra为奥比中光astra深度相机
    mode = "astra"

    if mode == "astra":
        openni2.initialize()

        dev = openni2.Device.open_any()
        # 打印设备型号
        print(dev.get_device_info())
        # 彩色通道
        color_stream = dev.create_color_stream()

        color_stream.start()

        fps = 0.0
        while (True):

            t1 = time.time()

            cframe = color_stream.read_frame()

            cframe_data = np.array(cframe.get_buffer_as_triplet()).reshape([480, 640, 3])
            R = cframe_data[:, :, 0]
            G = cframe_data[:, :, 1]
            B = cframe_data[:, :, 2]
            cframe_data = np.transpose(np.array([B, G, R]), [1, 2, 0])

            # 进行检测
            cframe_data = np.array(retinaface.detect_image(cframe_data))


            fps = (fps + (1. / (time.time() - t1))) / 2
            # print("fps= %.2f" % (fps))

            cframe_data = cv2.putText(cframe_data, "fps= %.2f" % (fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                      (0, 255, 0), 2)

            cv2.imshow("video", cframe_data)

            # waitkey(0)表示函数无限长，waitkey（1）表示每1ms检查一次按键
            c = cv2.waitKey(1) & 0xff
            # 如果有esc（esc的ASCII为27）键按下，退出循环（break）
            if c == 27:
                color_stream.stop()
                break
        print("Video Detection Done!")

        cv2.destroyAllWindows()
    elif mode == "computer_camera":
        # 读取摄像头或者视频
        capture = cv2.VideoCapture(0)

        ref, frame = capture.read()
        if not ref:
            raise ValueError("未能正确读取摄像头（视频），请注意是否正确安装摄像头（是否正确填写视频路径）。")

        fps = 0.0
        while (True):
            # 时间戳
            t1 = time.time()
            # 获取视频的返回值 ref 和视频中的每一帧 frame
            ref, frame = capture.read()
            if not ref:
                break
            # 格式转变，BGRtoRGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # 进行检测
            frame = np.array(retinaface.detect_image(frame))
            # RGBtoBGR满足opencv显示格式
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            # 计算帧数 假设目标检测网络处理1帧要0.02s，此时FPS就是1/0.02=50。
            # 也可以直接算fps=1./(time.time()-t1),两者的结果很接近
            fps = (fps + (1. / (time.time() - t1))) / 2

            frame = cv2.putText(frame, "fps= %.2f" % (fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow("video", frame)
            # waitkey(0)表示函数无限长，waitkey（1）表示每1ms检查一次按键
            c = cv2.waitKey(1) & 0xff

            # 如果有esc（esc的ASCII为27）键按下，退出循环（break）
            if c == 27:
                capture.release()
                break
        print("Video Detection Done!")
        capture.release()

        cv2.destroyAllWindows()
