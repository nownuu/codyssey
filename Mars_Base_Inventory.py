import csv

def read_csv(file_path):
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
        return data
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return []
    except Exception as e: #read
        print(f"Error reading file: {e}")
        return []

def sort_by_flammability(data):
    return sorted(data, key=lambda x: float(x['Flammability']), reverse=True)

def filter_high_flammability(data, threshold=0.7):
    return [row for row in data if float(row['Flammability']) >= threshold]

def save_to_csv(file_path, data):
    try:
        with open(file_path, mode='w', encoding='utf-8', newline='') as file:
            if not data:
                print("No data to save.")
                return
            fieldnames = data[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        print(f"Error saving file: {e}")

def save_to_binary(file_path, data):
    try:
        with open(file_path, mode='wb') as file:
            for row in data:
                file.write(str(row).encode('utf-8') + b'\n')
    except Exception as e:
        print(f"Error saving binary file: {e}")

def read_binary(file_path):
    try:
        with open(file_path, mode='rb') as file:
            content = file.readlines()
            for line in content:
                print(line.decode('utf-8').strip())
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
    except Exception as e:  #read
        print(f"Error binary file: {e}")

# 파일 경로 설정
input_file = "data/Mars_Base_Inventory_List.csv"
output_file = "data/Mars_Base_Inventory_danger.csv"
binary_file = "data/Mars_Base_Inventory_List.bin"

# CSV 파일 읽기
inventory_list = read_csv(input_file)

if inventory_list:
    # 인화성 기준으로 정렬
    sorted_inventory = sort_by_flammability(inventory_list)

    # 인화성이 0.7 이상인 항목 필터링
    dangerous_items = filter_high_flammability(sorted_inventory)

    # 결과 출력
    # print("정렬 목록 (인화성이 높은 순):")
    # for item in sorted_inventory:
    #     print(item)

    # print("\n인화성 0.7 이상인 목록:")
    # for item in dangerous_items:
    #     print(item)
 
    # 위험 물질 목록 저장
    save_to_csv(output_file, dangerous_items)
    print(f"위험 물질 목록 {output_file} 저장")

    # 정렬된 리스트 저장
    save_to_binary(binary_file, sorted_inventory)
    print(f"정렬된 목록(이진파일) {binary_file} 저장")

    # 이진 파일 읽기
    print("\n정렬 목록 출력:")
    read_binary(binary_file)
