import grpc
from . import hal_pb_pb2
from . import hal_pb_pb2_grpc
from typing import List, Tuple

class Servo:
    def __init__(self, host='localhost', port=50051):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = hal_pb_pb2_grpc.ServoControlStub(self.channel)

    def get_positions(self):
        response = self.stub.GetPositions(hal_pb_pb2.Empty())
        return [(pos.id, pos.position) for pos in response.positions]

    def set_positions(self, positions: List[Tuple[int, float]]):
        joint_positions = [
            hal_pb_pb2.JointPosition(id=id, position=position)
            for id, position in positions
        ]
        request = hal_pb_pb2.JointPositions(positions=joint_positions)
        self.stub.SetPositions(request)

    def set_wifi_info(self, ssid, password):
        request = hal_pb_pb2.WifiCredentials(ssid=ssid, password=password)
        self.stub.SetWifiInfo(request)

    def get_servo_info(self, servo_id):
        request = hal_pb_pb2.ServoId(id=servo_id)
        response = self.stub.GetServoInfo(request)
        if response.HasField('info'):
            info = response.info
            return {
                'id': info.id,
                'temperature': info.temperature,
                'current': info.current,
                'voltage': round(info.voltage, 2),
                'speed': info.speed,
                'current_position': info.current_position
            }
        else:
            raise Exception(f"Error: {response.error.message} (Code: {response.error.code})")

    def scan(self):
        response = self.stub.Scan(hal_pb_pb2.Empty())
        return response.ids

    def change_id(self, old_id, new_id):
        request = hal_pb_pb2.IdChange(old_id=old_id, new_id=new_id)
        response = self.stub.ChangeId(request)
        if response.HasField('success'):
            return response.success
        else:
            raise Exception(f"Error: {response.error.message} (Code: {response.error.code})")

    def close(self):
        self.channel.close()

# Usage example
if __name__ == '__main__':
    client = Servo('192.168.42.1')

    try:
        # Get positions
        positions = client.get_positions()
        print("Current positions:", positions)

        # Set positions
        client.set_positions([(9, 45.0)])
        print("Positions set")

        # Set WiFi info
        client.set_wifi_info("MyNetwork", "MyPassword")
        print("WiFi info set")

        # Get servo info
        servo_info = client.get_servo_info(9)
        print("Servo 9 info:", servo_info)

        servo_positions = client.get_positions()
        print("Current positions:", servo_positions)

        # Scan for servos
        servo_ids = client.scan()
        print("Found servo IDs:", servo_ids)

        # Change servo ID
        success = client.change_id(1, 10)
        print("ID change success:", success)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        client.close()