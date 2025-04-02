import random



class DummySensor:
    log_counter = 1  # 로그 순서 기록용 변수

    def __init__(self):
        self.env_values = {
            "mars_base_internal_temperature": 0,
            "mars_base_external_temperature": 0,
            "mars_base_internal_humidity": 0,
            "mars_base_external_illuminance": 0,
            "mars_base_internal_co2": 0,
            "mars_base_internal_oxygen": 0
        }

    def set_env(self):
        self.env_values["mars_base_internal_temperature"] = random.uniform(18, 30)
        self.env_values["mars_base_external_temperature"] = random.uniform(0, 21)
        self.env_values["mars_base_internal_humidity"] = random.uniform(50, 60)
        self.env_values["mars_base_external_illuminance"] = random.uniform(500, 715)
        self.env_values["mars_base_internal_co2"] = random.uniform(0.02, 0.1)
        self.env_values["mars_base_internal_oxygen"] = random.uniform(4, 7)

    def get_env(self):
        # 로그 순서 번호를 문자열로 변환
        log_index = str(DummySensor.log_counter)

        # 로그 메시지 생성
        log_message = f"{log_index}, {self.env_values['mars_base_internal_temperature']:.2f}, " \
                      f"{self.env_values['mars_base_external_temperature']:.2f}, " \
                      f"{self.env_values['mars_base_internal_humidity']:.2f}, " \
                      f"{self.env_values['mars_base_external_illuminance']:.2f}, " \
                      f"{self.env_values['mars_base_internal_co2']:.4f}, " \
                      f"{self.env_values['mars_base_internal_oxygen']:.2f}\n"

        # 로그 파일에 기록
        with open("data/mars_sensor_log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(log_message)

        # 로그 순서 증가
        DummySensor.log_counter += 1

        return self.env_values

# 인스턴스 생성
ds = DummySensor()

# 환경 값 설정
ds.set_env()

# 환경 값 가져오기 (로그 저장됨)
env_data = ds.get_env()

print(env_data)
