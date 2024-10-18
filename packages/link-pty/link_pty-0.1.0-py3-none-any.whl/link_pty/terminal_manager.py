import asyncio
import json
import os
import pty
import select
import subprocess
import websockets
import requests

class TerminalManager:
    def __init__(self, base_url="linkpty.codesocean.top:43143"):
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
        async with websockets.connect(websocket_url) as ws:
            await self.on_message(ws)

def run_terminal_manager(base_url=None):
    manager = TerminalManager(base_url if base_url else "pseudoterminal.codesocean.top")
    asyncio.run(manager.main())

if __name__ == "__main__":
    run_terminal_manager()
