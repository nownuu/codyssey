import requests


def get_kbs_headlines():
    """
    KBS 뉴스 홈페이지에서 주요 헤드라인을 추출하는 함수.
    BeautifulSoup 없이 문자열 처리로만 구현한다.
    """
    url = 'http://news.kbs.co.kr'
    response = requests.get(url)

    if response.status_code != 200:
        return []

    html = response.text

    # 개발자 도구로 확인해본 결과, 주요 뉴스 헤드라인은
    # <div class="headline"> 또는 <a class="tit"> 같은 태그 안에 존재함
    # 여기서는 간단히 'tit">' 와 '</a>' 사이의 텍스트를 추출하는 방식으로 구현
    headlines = []
    split_html = html.split('<a class="tit"')

    for part in split_html[1:]:
        start_index = part.find('>') + 1
        end_index = part.find('</a>')

        if start_index > 0 and end_index > start_index:
            title = part[start_index:end_index].strip()
            if title:
                headlines.append(title)

    return headlines


def main():
    headlines = get_kbs_headlines()
    print(headlines)


if __name__ == '__main__':
    main()
