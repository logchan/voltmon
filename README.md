Voltmon
===

[English](#english)

使用电压表监控CPU和内存使用率。Python服务端，理论上支持 Windows / macOS / Linux 全平台。客户端是 Arduino，使用有线串口连接。

灵感来源：[【有手就能做】30元自制电脑状态监控仪表,没有光污染,资料全开源](https://www.bilibili.com/video/BV1jL4y1x7gx) / [CpuRamGet](https://github.com/ShaderFallback/CpuRamGet)

## 使用方法

- Python环境需要安装 `pyserial psutil` 两个包
- 把 [voltmon-client](voltmon-client) 上传到 Arduino
  - 如果你用的不是 Arduino Nano，请先把 `N_PINS` 和 `pin_ids` 改成支持 `analogWrite` 的 pin
- 运行 `python voltmon.py`
  - 默认使用第一个串口，如果你有多个串口也可以用 `--port name` 指定串口
  - 默认输出端口是 `pin_ids` 里的第1个和第4个（对应 Nano 的 pin 3, 9）（*注：非初音未来梗）。可以用 `--cpu_pin` 和 `--ram_pin` 来指定使用 `pin_ids` 里的第几个 pin

# English

Monitor CPU and RAM usage on an analog voltmeter. Python server supports Windows / macOS / Linux. Arduino client with wired serial connection.

This is a Python + Arduino version of [CpuRamGet](https://github.com/ShaderFallback/CpuRamGet)

## How to use

- Install `pyserial psutil` in your Python environment
- Upload [voltmon-client](voltmon-client) to Arduino
  - If your device is not Arduino Nano, change `N_PINS` and `pin_ids` to the correct pins that support `analogWrite`
- Run `python voltmon.py`
  - By default, the first serial port is used; you can use `--port name` to specify a name like `COM3`
  - Use `--cpu_pin` and `--ram_pin` to specify the indices of the pins (in `pin_ids`) to use. For Arduino Nano, the defaults are `0` and `3` (which map to pins `3` and `9`)
