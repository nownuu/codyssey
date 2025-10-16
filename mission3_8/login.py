from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def login_naver():
    # 크롬 드라이버 경로 지정
    driver = webdriver.Chrome(executable_path='/path/to/chromedriver')

    # 네이버 로그인 페이지 열기
    driver.get('https://nid.naver.com/nidlogin.login')

    # 로그인 정보 입력
    id_box = driver.find_element_by_id('id')
    pw_box = driver.find_element_by_id('pw')

    # 네이버 아이디와 비밀번호 입력 (실제 아이디와 비밀번호로 대체 필요)
    id_box.send_keys('your_naver_id')
    pw_box.send_keys('your_naver_password')

    # 로그인 버튼 클릭
    pw_box.send_keys(Keys.RETURN)

    # 페이지 로딩 시간 대기
    time.sleep(3)

    # 로그인 후 메인 페이지로 이동 (로그인 후 이동할 페이지 확인)
    driver.get('https://www.naver.com')

    return driver


def crawl_after_login(driver):
    # 예시: 로그인 후 보이는 뉴스 기사 제목들을 크롤링 (수정 필요)
    news_titles = driver.find_elements_by_css_selector('.news_title_class')  # 적절한 셀렉터로 수정
    news_titles_list = [title.text for title in news_titles]

def main():
    driver = login_naver()
    news_titles = crawl_after_login(driver)

    # 크롤링한 뉴스 제목 출력
    for idx, title in enumerate(news_titles, 1):
        print(f'{idx}. {title}')

    # 크롤링이 끝난 후, 드라이버 종료
    driver.quit()

if __name__ == '__main__':
    main()
    return news_titles_list

def save_results(news_titles):
    with open('crawling_KBS.py', 'w', encoding='utf-8') as f:
        f.write('news_titles = [\n')
        for title in news_titles:
            f.write(f"    '{title}',\n")
        f.write(']\n')

def main():
    driver = login_naver()
    news_titles = crawl_after_login(driver)
    
    # 결과를 파일로 저장
    save_results(news_titles)
    
    # 크롤링한 뉴스 제목 출력
    for idx, title in enumerate(news_titles, 1):
        print(f'{idx}. {title}')

    # 드라이버 종료
    driver.quit()

