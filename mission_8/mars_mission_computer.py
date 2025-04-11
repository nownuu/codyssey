import time
import random
import os
import platform
import psutil

class DummySensor:
    def get_internal_temperature(self):
        return round(random.uniform(15, 25), 2)

    def get_external_temperature(self):
        return round(random.uniform(-80, 0), 2)

    def get_humidity(self):
        return round(random.uniform(0, 100), 2)

    def get_illuminance(self):
        return round(random.uniform(0, 1000), 2)

    def get_co2(self):
        return round(random.uniform(300, 5000), 2)

    def get_oxygen(self):
        return round(random.uniform(19, 23), 2)


class MissionComputer:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': None,
            'mars_base_external_temperature': None,
            'mars_base_internal_humidity': None,
            'mars_base_external_illuminance': None,
            'mars_base_internal_co2': None,
            'mars_base_internal_oxygen': None
        }
        self.data_log = {key: [] for key in self.env_values}
        self.ds = DummySensor()
        self.running = True

    def get_sensor_data(self):
        start_time = time.time()
        while self.running:
            self.env_values['mars_base_internal_temperature'] = self.ds.get_internal_temperature()
            self.env_values['mars_base_external_temperature'] = self.ds.get_external_temperature()
            self.env_values['mars_base_internal_humidity'] = self.ds.get_humidity()
            self.env_values['mars_base_external_illuminance'] = self.ds.get_illuminance()
            self.env_values['mars_base_internal_co2'] = self.ds.get_co2()
            self.env_values['mars_base_internal_oxygen'] = self.ds.get_oxygen()

            for key in self.env_values:
                self.data_log[key].append(self.env_values[key])

            print('화성 기지 환경 값 :')
            print('{')
            for key, value in self.env_values.items():
                print(f"  '{key}': {value},")
            print('}')
            print('-' * 50)

            if time.time() - start_time >= 300:
                print('>> 5분 평균 값:')
                for key, values in self.data_log.items():
                    avg_value = sum(values) / len(values) if values else 0
                    print(f"  '{key}': {round(avg_value, 2)},")
                print('=' * 50)
                self.data_log = {key: [] for key in self.env_values}
                start_time = time.time()

            time.sleep(5)

        print('System Stop')

    def stop(self):
        self.running = False

    def get_mission_computer_info(self):
        try:
            info = {
                'operating_system': platform.system(),
                'os_version': platform.version(),
                'cpu_type': platform.processor(),
                'cpu_core_count': os.cpu_count(),
                'memory_size': round(psutil.virtual_memory().total / (1024 ** 3), 2)  # GB
            }
            print('Mission Computer System Info:')
            print('{')
            for key, value in info.items():
                print(f"  '{key}': '{value}',")
            print('}')
        except Exception as e:
            print('Error retrieving system information:', e)

    def get_mission_computer_load(self):
        try:
            load = {
                'cpu_usage_percent': psutil.cpu_percent(interval=1),
                'memory_usage_percent': psutil.virtual_memory().percent
            }
            print('Mission Computer Load Info:')
            print('{')
            for key, value in load.items():
                print(f"  '{key}': {value},")
            print('}')
        except Exception as e:
            print('Error system load information:', e)

if __name__ == '__main__':
    runComputer = MissionComputer()
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()

    while True:
        try:
            runComputer.get_sensor_data()
        except KeyboardInterrupt:
            runComputer.stop()
            break
