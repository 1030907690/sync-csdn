---
layout:					post
title:					"scrcpy-client pyscrcpy 报ConnectionError(“Video stream is disconnected“)"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
## 异常
```
Video stream is disconnected
```

- 代码详情，scrcpy-client 使用0.4.7版本

```python
import time
import scrcpy
from adbutils import adb
import cv2


def on_frame(frame):
    # If you set non-blocking (default) in constructor, the frame event receiver
    # may receive None to avoid blocking event.
    if frame is not None:
       cv2.imshow("frame", frame)
    cv2.waitKey(10)


def on_init():
    # Print device name
    print(client.device_name)
    # If you already know the device serial


devices = adb.device_list()
client = scrcpy.Client(device=devices[0])
#解决方案
# client = scrcpy.Client(device=devices[0], max_width=1000)
# client = scrcpy.Client(device="5105f5810920")
client.add_listener(scrcpy.EVENT_FRAME, on_frame)
client.add_listener(scrcpy.EVENT_INIT, on_init)
client.start(threaded=True)
print("threaded ")
while True:
    time.sleep(999)

# Mousedown
# client.control.touch(323, 965, scrcpy.ACTION_DOWN)
# time.sleep(0.01)
# # Mouseup
# client.control.touch(323, 965, scrcpy.ACTION_UP)
# print("end")

```
- 运行结果
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/3f1d24e338a2445e93cfa7d97996856b.png)
- 使用 pyscrcpy 1.0.1 出现同样情况
## 解决方案
- scrcpy-client  设置`max_width`属性。

```python
client = scrcpy.Client(device=devices[0], max_width=1000)
```
- 运行成功
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/13bcec45836642e9a382d83863d19db3.png)

- pyscrcpy  同理设置`max_size`属性。

```
 client = Client(device=devices[0],max_fps=20,max_size=1000)
```
- 修改后结果
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/9255c1307fb947d5bd689211d0472bac.png)
