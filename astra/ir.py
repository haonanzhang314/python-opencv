import numpy as np
import cv2
from openni import openni2
from openni import _openni2 as c_api

openni2.initialize()
device = openni2.Device.open_any()

ir_stream = device.create_ir_stream()
# ir_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_GRAY16, resolutionX = 320, resolutionY = 240, fps = 30))
ir_stream.start()

while(True):
    frame = ir_stream.read_frame()

    # returns a 1-dim c_ushort_array of len: 76'800 = 320x240 each pixel having an uint16 value 0..65535
    frame_data = frame.get_buffer_as_uint16()

    # converting to numpy.ndarray which is still 1-dimension only
    img = np.frombuffer(frame_data, dtype=np.uint16)

    # convert to 3-dimensional array
    img.shape = (480, 640)

    # normalize values
    img = img.astype(np.float) / 1024

    # Display image
    cv2.imshow("image", img)

    # Wait for input
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

ir_stream.stop()
openni2.unload()