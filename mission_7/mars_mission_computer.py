import random
import time

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
            "mars_base_internal_temperature": None,
            "mars_base_external_temperature": None,
            "mars_base_internal_humidity": None,
            "mars_base_external_illuminance": None,
            "mars_base_internal_co2": None,
            "mars_base_internal_oxygen": None
        }
        self.data_log = {key: [] for key in self.env_values}
        self.ds = DummySensor()
        self.running = True
        
    def get_sensor_data(self):
        start_time = time.time()
        while self.running:
            self.env_values["mars_base_internal_temperature"] = self.ds.get_internal_temperature()
            self.env_values["mars_base_external_temperature"] = self.ds.get_external_temperature()
            self.env_values["mars_base_internal_humidity"] = self.ds.get_humidity()
            self.env_values["mars_base_external_illuminance"] = self.ds.get_illuminance()
            self.env_values["mars_base_internal_co2"] = self.ds.get_co2()
            self.env_values["mars_base_internal_oxygen"] = self.ds.get_oxygen()
            
            for key in self.env_values:
                self.data_log[key].append(self.env_values[key])

            print("화성 기지 환경 값 :")
            for key, value in self.env_values.items():
                print(f"{key}: {value}")
            print("-" * 50)
            
            if time.time() - start_time >= 300:
                print(">> 5분 평균 값:")
                for key, values in self.data_log.items():
                    avg_value = sum(values) / len(values) if values else 0
                    print(f"{key}: {round(avg_value, 2)}")
                print("=" * 50)
                self.data_log = {key: [] for key in self.env_values}
                start_time = time.time()
            
            time.sleep(3)
        
        print("STOP......")

    def stop(self):
        self.running = False


# 생성 및 실행
if __name__ == "__main__":
    RunComputer = MissionComputer()
    
    while True:
        RunComputer.get_sensor_data()
        user_input = input("정지(q) : ")
        if user_input.lower() == 'q':
            RunComputer.stop()
            break