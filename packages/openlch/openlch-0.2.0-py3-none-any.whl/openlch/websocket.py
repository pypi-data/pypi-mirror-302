"""Defines the ServoClient class for controlling the OpenLCH servo motors."""

import asyncio
import json
from enum import Enum
from typing import Any

import websockets
from pydantic import BaseModel


class ServoMode(Enum):
    Position = 0
    ConstantSpeed = 1
    PWMOpenLoop = 2
    StepServo = 3


class ServoDirection(Enum):
    Clockwise = 0
    Counterclockwise = 1


class MemoryLockState(Enum):
    Unlocked = 0
    Locked = 1


class TorqueMode(Enum):
    Disabled = 0
    Enabled = 1
    Stiff = 2


class ServoData(BaseModel):
    acceleration: int
    async_write_flag: int
    current_current: int
    current_load: int
    current_location: int
    current_speed: int
    current_temperature: int
    current_voltage: int
    lock_mark: int
    mobile_sign: int
    reserved1: int
    reserved2: int
    running_speed: int
    running_time: int
    servo_status: int
    target_location: int
    torque_limit: int
    torque_switch: int

    def __repr__(self) -> str:
        attrs = [
            f"current_location={self.current_location}",
            f"current_speed={self.current_speed}",
            f"current_temperature={self.current_temperature}",
        ]
        return f"ServoData({', '.join(attrs)})"


class ContinuousReadResponse(BaseModel):
    servo_data: list[ServoData]
    task_run_count: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ContinuousReadResponse":
        return cls(servo_data=[ServoData(**servo) for servo in data["servo"]], task_run_count=data["task_run_count"])

    def __repr__(self) -> str:
        attrs = [
            f"servos={len(self.servo_data)}",
            f"task_run_count={self.task_run_count}",
        ]
        return f"ContinuousReadResponse({', '.join(attrs)})"


class WriteMultipleCommand(BaseModel):
    ids: list[int]
    positions: list[int]
    times: list[int]
    speeds: list[int]
    only_write_positions: int

    def __repr__(self) -> str:
        attrs = [
            f"ids={self.ids}",
            f"positions={self.positions}",
            f"times={self.times}",
            f"speeds={self.speeds}",
            f"only_write_positions={self.only_write_positions}",
        ]
        return f"WriteMultipleCommand({', '.join(attrs)})"


class ServoClient:
    def __init__(self, uri: str = "ws://192.168.42.1:8080") -> None:
        self.uri = uri
        self.websocket = None

    async def connect(self) -> None:
        if self.websocket is None or self.websocket.closed:
            self.websocket = await websockets.connect(self.uri)

    async def disconnect(self) -> None:
        if self.websocket and not self.websocket.closed:
            await self.websocket.close()

    async def _send_command(self, command: str, params: dict[str, Any] | None) -> dict[str, Any] | None:
        try:
            await self.connect()
            message = json.dumps({"command": command, "params": params})
            await self.websocket.send(message)
            response = await self.websocket.recv()
            parsed_response = json.loads(response)

            if not parsed_response["success"]:
                error_msg = parsed_response.get("error", "Unknown error")
                print(f"Error in command {command}: {error_msg}")
                return None

            return parsed_response.get("data")
        except websockets.exceptions.WebSocketException as e:
            print(f"WebSocket error: {e}")
            await self.disconnect()
            return None
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            await self.disconnect()
            return None

    async def move_servo(self, id: int, position: int, time: int, speed: int) -> dict[str, Any] | None:
        params = {"id": id, "position": position, "time": time, "speed": speed}
        return await self._send_command("Move", params)

    async def set_mode(self, id: int, mode: ServoMode) -> dict[str, Any] | None:
        params = {"id": id, "mode": mode.value}
        return await self._send_command("SetMode", params)

    async def set_speed(self, id: int, speed: int, direction: ServoDirection) -> dict[str, Any] | None:
        params = {"id": id, "speed": speed, "direction": direction.value}
        return await self._send_command("SetSpeed", params)

    async def read_info(self, id: int) -> dict[str, Any] | None:
        params = {"id": id}
        return await self._send_command("ReadInfo", params)

    async def read_pid(self, id: int) -> dict[str, Any] | None:
        params = {"id": id}
        return await self._send_command("ReadPID", params)

    async def set_pid(self, id: int, p: int, i: int, d: int) -> dict[str, Any] | None:
        params = {"id": id, "p": p, "i": i, "d": d}
        return await self._send_command("SetPID", params)

    async def set_memory_lock(self, id: int, state: MemoryLockState) -> dict[str, Any] | None:
        params = {"id": id, "state": state.value}
        return await self._send_command("SetMemoryLock", params)

    async def read_angle_limits(self, id: int) -> dict[str, Any] | None:
        params = {"id": id}
        return await self._send_command("ReadAngleLimits", params)

    async def set_torque_mode(self, id: int, mode: TorqueMode) -> dict[str, Any] | None:
        params = {"id": id, "mode": mode.value}
        return await self._send_command("SetTorqueMode", params)

    async def scan(self, id: int) -> dict[str, Any] | None:
        params = {"id": id}
        return await self._send_command("Scan", params)

    async def write_multiple(self, command: WriteMultipleCommand) -> dict[str, Any] | None:
        params = {"cmd": command.dict()}
        return await self._send_command("WriteMultiple", params)

    async def read_continuous(self) -> ContinuousReadResponse | None:
        data = await self._send_command("ReadContinuous", None)
        if data:
            return ContinuousReadResponse(data)
        return None


async def main() -> None:
    client = ServoClient()

    odd = True
    move_timer = 0
    target_interval = 1 / 50  # 50Hz
    try:
        while True:
            loop_start = asyncio.get_event_loop().time()

            # Read continuous data
            response = await client.read_continuous()
            if response:
                print("Read continuous response:", response.servo_data[8])  # Print data for servo 9 (index 8)

            # Move servo once per second
            if move_timer >= 50:  # 50 iterations at 50Hz = 1 second
                await client.write_multiple(
                    WriteMultipleCommand(
                        ids=list(range(1, 17)),
                        positions=[3500] * 16 if odd else [3000] * 16,
                        times=[0] * 16,
                        speeds=[0] * 16,
                        only_write_positions=1,
                    )
                )
                odd = not odd
                move_timer = 0
            else:
                move_timer += 1

            # Calculate remaining time and sleep if possible
            elapsed_time = asyncio.get_event_loop().time() - loop_start
            remaining_time = target_interval - elapsed_time

            if remaining_time > 0:
                await asyncio.sleep(remaining_time)
            else:
                print(f"Warning: Loop running late by {-remaining_time:.6f} seconds")

    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
