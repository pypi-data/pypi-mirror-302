import asyncio
import json
import os
import pty
import select
import subprocess
import websockets
import requests
import argparse
import time

class TerminalManager:
    def __init__(self, base_url):
        self.BASE_SERVER_URL = base_url
        self.terminals = []
        self.key = None

    async def read_and_forward_output(self, ws, master_fd: int, terminal_index: int):
        """持续读取伪终端的输出并通过 WebSocket 转发给客户端"""
        try:
            while True:
                await asyncio.sleep(0.1)  # 非阻塞等待
                rlist, _, _ = select.select([master_fd], [], [], 0.1)
                if master_fd in rlist:
                    output = os.read(master_fd, 2048).decode("utf-8", errors="ignore")
                    await ws.send(json.dumps({"operation": "RECEIVE_SERVEROUTPUT", "terminal_index": terminal_index, "data": output}))
        except Exception as e:
            print(f"Error while reading pty output: {e}")
    
    async def ping(self, ws):
        while True:
            # print("Ping for keeping connection.")
            await asyncio.sleep(60)  # 非阻塞等待
            await ws.send(json.dumps({"operation": "PING"}))

    async def on_message(self, ws):
        async for message in ws:
            try:
                data_json = json.loads(message)
                operation = data_json["operation"]
                if operation == "ASSIGN_KEY":
                    self.key = data_json['key']
                    print(f"Please use this code to connect to the pseudo terminal: {data_json['key']}")
                elif operation == "CREATE_TERMINAL":
                    # 创建伪终端
                    master_fd, slave_fd = pty.openpty()
                    process = subprocess.Popen(
                        ["/bin/bash"],
                        stdin=slave_fd, stdout=slave_fd, stderr=slave_fd, close_fds=True
                    )
                    self.terminals.append((process, master_fd, slave_fd))
                    requests.get(f"http://{self.BASE_SERVER_URL}/create_terminal_done?key={self.key}&terminal_index={len(self.terminals) - 1}")

                    # 使用 asyncio 创建任务
                    asyncio.create_task(self.read_and_forward_output(ws, master_fd, len(self.terminals) - 1))
                    print(f"Created new pseudo terminal #{len(self.terminals) - 1}")
                elif operation == "TERMINATE_TERMINAL":
                    terminal = self.terminals[data_json["terminal_index"]]
                    terminal[0].terminate()  # 终止子进程
                    os.close(terminal[1])
                    os.close(terminal[2])
                elif operation == "RECEIVE_USERINPUT":
                    terminal = self.terminals[data_json["terminal_index"]]
                    os.write(terminal[1], data_json["data"].encode('utf-8'))
            except Exception as e:
                print(f"Error handling message: {e}")

    async def main(self):
        websocket_url = f"ws://{self.BASE_SERVER_URL}/dockerserver"
        for i in range(0, 10):
            try:
                async with websockets.connect(websocket_url) as ws:
                    asyncio.create_task(self.ping(ws))
                    await self.on_message(ws)
            except websockets.exceptions.ConnectionClosedError as e:
                print(f"Connection closed: {e}. Reconnecting in 5 seconds...")
                await asyncio.sleep(5)  # 等待 5 秒后重新连接
            except Exception as e:
                print(f"Unexpected error: {e}. Reconnecting in 5 seconds...")
                await asyncio.sleep(5)

def run_terminal_manager(base_url="linkpty.codesocean.top:43143"):
    print(f"Your base url here: {base_url}")
    manager = TerminalManager(base_url)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(manager.main())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the terminal manager.')
    parser.add_argument('--base-url', type=str, required=False, default="linkpty.codesocean.top:43143", help='Base URL for the WebSocket server.')
    args = parser.parse_args()

    try:
        run_terminal_manager(args.base_url)
    except Exception as e:
        print(e)
