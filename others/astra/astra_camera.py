from openni import openni2
import numpy as np
import cv2


if __name__ == "__main__":

    openni2.initialize()
    #设备型号
    dev = openni2.Device.open_any()
    #打印设备型号
    print(dev.get_device_info())

    #创建深度流的通道
    depth_stream = dev.create_depth_stream()
    depth_stream.start()
    #彩色通道
    color_stream = dev.create_color_stream()
    color_stream.start()
    #红外通道
    #ir_stream = dev.create_ir_stream()
    #ir_stream.start()



    #深度窗口
    cv2.namedWindow('depth')
    #彩色窗口
    #cv2.namedWindow('color')
    #红外窗口
    #cv2.namedWindow('ir')

    capture_flag = 0

    base_path = '../../'

    count = 1
    #设置视频的分辨率和长宽以及fps等等内容
    # ir_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_GRAY16, resolutionX = 320, resolutionY = 240, fps = 30))

    while True:
    # 显示深度图像
        dframe = depth_stream.read_frame()
        # 转换数据格式
        dframe_data = np.array(dframe.get_buffer_as_triplet()).reshape([480, 640, 2])
        dpt1 = np.asarray(dframe_data[:, :, 0], dtype='float32')
        dpt2 = np.asarray(dframe_data[:, :, 1], dtype='float32')

        dpt2 *= 255
        # 对于为什么要乘于255的解答
        # 深度图像的深度值 是按照16位长度（两字节）的数据格式存储的，也可以认为前八位是高字节，后八位是低字节。
        # 因此一张深度图像如果是 640480分辨率的话，那么图像字节大小 就是 640480*2，其中一个字节是8位（255）
        dpt = dpt1 + dpt2
        # 转换一下，重要，陈20221222
        dpt = dpt.astype(np.uint16)

        # cv2里面的函数，就是类似于一种筛选
        '假设我们需要让我们的深度摄像头感兴趣的距离范围有差别地显示，那么我们就需要确定一个合适的alpha值，公式为：有效距离*alpha=255，' \
        '假设我们想让深度摄像头8m距离内的深度被显示，>8m的与8m的颜色显示相同，那么alpha=255/(8*10^3)≈0.03，' \
        '假设我们想让深度摄像头6m距离内的深度被显示，>6m的与6m的颜色显示相同，那么alpha=255/(6*10^3)≈0.0425'
        dim_gray = cv2.convertScaleAbs(dpt, alpha=0.5)
        # 对深度图像进行一种图像的渲染，目前有11种渲染方式，大家可以逐一去试下
        depth_colormap = cv2.applyColorMap(dim_gray, 10)  # 有0~11种渲染的模式
        cv2.imshow('depth', depth_colormap)
    #
    # # 显示RGB图像
    #     cframe = color_stream.read_frame()
    #     cframe_data = np.array(cframe.get_buffer_as_triplet()).reshape([480, 640, 3])
    #     R = cframe_data[:, :, 0]
    #     G = cframe_data[:, :, 1]
    #     B = cframe_data[:, :, 2]
    #     cframe_data = np.transpose(np.array([B, G, R]), [1, 2, 0])
    #     # print(cframe_data.shape)
    #     cv2.imshow('color', cframe_data)

    # 显示ir图像
    #     iframe = ir_stream.read_frame()
    #     iframe_data = iframe.get_buffer_as_uint16()
    #     img = np.frombuffer(iframe_data, dtype=np.uint16)
    #     img.shape = (480, 640)
    #     img = img.astype(np.float) / 1024
    #     cv2.imshow("ir", img)

        key = cv2.waitKey(30)
        if int(key) == ord('q'):
            break

        if int(key) == ord('r'):
            capture_flag = 1
        if capture_flag == 1:
            name = str(count).zfill(8)
            cv2.imwrite(base_path + 'img/' + name + ".jpg", depth_colormap)
            #cv2.imwrite(base_path + 'img/' + name + ".jpg", cframe_data)
            # cv2.imwrite(base_path + 'img/' + name + ".jpg", img)
            count = count + 1

    depth_stream.stop()
    color_stream.stop()
    #ir_stream.stop()
    dev.close()

