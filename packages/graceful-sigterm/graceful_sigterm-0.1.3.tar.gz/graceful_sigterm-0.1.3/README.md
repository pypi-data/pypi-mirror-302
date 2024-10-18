# graceful-sigterm

Receive the kill signal from the operating system and gracefully wait for the worker thread to end.

Note: The package name is `graceful-sigterm` but the module name is `sigterm` for short.

## Install

```
pip install graceful-sigterm
```

## Usage Example 1

*example1.py*

```
import time
import signal
import sigterm


def worker():
    print("Press Ctrl+C, and wait 5 seconds to stop...")
    while not sigterm.is_stopped():
        print(".", end="", flush=True)
        sigterm.wait_until_stop(timeout=1)
    print("")
    for i in range(5):
        print("x", end="", flush=True)
        time.sleep(1)


def main():
    sigterm.setup()
    sigterm.setup(signal.SIGINT)
    sigterm.register_worker(worker)
    sigterm.execute()


if __name__ == "__main__":
    main()
```

*output*

```
test@test sigterm % python example1.py
Press Ctrl+C, and wait 5 seconds to stop...
....^C
xxxxx%      
```


## Releases

### 0.1.0

- 版本首发。

### 0.1.1

- 文档修改。

### 0.1.2

- 修正主线程中长时间待子线程结束导致无法拦截信号的问题。

### 0.1.3

- 更友好的提示信息。

