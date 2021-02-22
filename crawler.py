from bs4 import BeautifulSoup
import requests
import os

APPLY_USERNAME = os.environ['APPLY_USERNAME']
APPLY_PASSWORD = os.environ['APPLY_PASSWORD']
LOGIN_URL = 'https://apply.likelion.org/accounts/login/'
APPLY_URL = 'https://apply.likelion.org/apply/'
HEADERS = {
    'referer': 'https://apply.likelion.org/accounts/login/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
}
COOKIES = {
    'sessionid': ''
}


def getCSRFToken():
    request = requests.get(LOGIN_URL)
    cookies = request.cookies.get_dict()
    soup = BeautifulSoup(request.text, 'html.parser')
    csrfmiddlewaretoken = soup.find("input", {"name": "csrfmiddlewaretoken"})['value']
    token = {
        'csrftoken': cookies['csrftoken'],
        'csrfmiddlewaretoken': csrfmiddlewaretoken
    }
    print('CSRF 토큰 가져옴')
    return token


def getSessionId():
    token = getCSRFToken()
    data = {
        'csrfmiddlewaretoken': token['csrfmiddlewaretoken'],
        'username': APPLY_USERNAME,
        'password': APPLY_PASSWORD
    }
    cookies = {
        'csrftoken': token['csrftoken']
    }
    request = requests.post(LOGIN_URL, data=data, cookies=cookies, headers=HEADERS, allow_redirects=False)
    cookies = request.cookies.get_dict()
    COOKIES['sessionid'] = cookies['sessionid']
    print('세션 ID 가져옴 (로그인 성공)')


def getApplyListURL():
    getSessionId()
    request = requests.get(APPLY_URL, cookies=COOKIES)
    soup = BeautifulSoup(request.text, 'html.parser')
    list_location = soup.find('div', {'id': 'likelion_num'}).find('a')['href']
    print('지원서 페이지 URL 가져옴')
    return list_location


def getApplicantList():
    url = f"https://apply.likelion.org{getApplyListURL()}"
    request = requests.get(url, cookies=COOKIES)
    soup = BeautifulSoup(request.text, 'html.parser')
    applicant_list_a = soup.find('div', {'class': 'applicant_page'}).find_all('a')
    applicant_list_urls = []
    for a in applicant_list_a:
        applicant_list_urls.append(a['href'])
    print('지원자 리스트 작성 성공')
    return applicant_list_urls


def getApplicantInfo(applicant_url):
    url = f"https://apply.likelion.org{applicant_url}"
    request = requests.get(url, cookies=COOKIES)
    soup = BeautifulSoup(request.text, 'html.parser')
    name = soup.find('h3').text
    user_info = soup.find_all('div', {'class': ['col-md-6 col-xs-12', 'user_information']})
    year = user_info[0].find_all('p')[0].text
    major = user_info[0].find_all('p')[2].text
    phone = user_info[0].find_all('p')[3].text
    email = user_info[0].find_all('p')[5].text
    try:
        github = user_info[1].find('a')['href']
    except:
        github = 'Not Provided'
    try:
        attachment = user_info[2].find('a')['href']
    except:
        attachment = 'Not Provided'
    answers = soup.find_all('div', {'class': 'answer-font'})
    answer1 = answers[0].text
    answer2 = answers[1].text
    answer3 = answers[2].text
    answer4 = answers[3].text
    answer5 = answers[4].text
    data = {
        'name': name,
        'year': year,
        'major': major,
        'phone': phone,
        'email': email,
        'github': github,
        'attachment': attachment,
        'answer1': answer1,
        'answer2': answer2,
        'answer3': answer3,
        'answer4': answer4,
        'answer5': answer5
    }
    print(f"{name} 지원자 정보 읽음")
    return data


def getApplicants():
    applicantList = getApplicantList()
    applicantData = []
    for applicant in applicantList:
        applicantInfo = getApplicantInfo(applicant)
        applicantData.append(applicantInfo)
    return applicantData
