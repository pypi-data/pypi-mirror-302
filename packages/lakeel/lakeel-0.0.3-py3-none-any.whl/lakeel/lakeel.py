import platform
import subprocess
import sys
import importlib.util
import os

# pip로 패키지 설치 함수
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# 패키지가 설치되어 있는지 확인하는 함수
def is_installed(package_name):
    package_spec = importlib.util.find_spec(package_name)
    return package_spec is not None

# 운영체제에 맞는 폰트 설정 함수
def sfo():
    current_os = platform.system()

    # matplotlib이 설치되어 있는지 확인
    if not is_installed('matplotlib'):
        print("matplotlib가 설치되어 있지 않습니다.")
        install('matplotlib')
    else:
        print("matplotlib가 이미 설치되어 있습니다 :)")

    import matplotlib.pyplot as plt
    from matplotlib import rc

    if current_os == 'Darwin':  # macOS
        print("폰트가 AppleGothic font로 설정되었습니다.")
        rc('font', family='AppleGothic')
        
    elif current_os == 'Windows':  # Windows
        print("폰트가 Malgun Gothic font로 설정되었습니다.")
        rc('font', family='Malgun Gothic')
        
    else:
        print(f"Unknown OS: {current_os}. Please set the font manually.")

    # 음수 부호 깨짐 방지
    plt.rcParams['axes.unicode_minus'] = False
    print("Font setup is complete.")

# 1. 현재 파이썬 코드가 실행되는 경로를 반환하는 함수
def dir():
    return os.getcwd()

# 2. 설치된 pip 패키지 목록을 알파벳 순서대로 출력하는 함수
def pip():
    # pip list 명령 실행
    result = subprocess.run([sys.executable, "-m", "pip", "list"], capture_output=True, text=True)
    
    # 결과를 줄 단위로 분리
    lines = result.stdout.splitlines()

    # 첫 두 줄은 헤더이므로 제외하고, 나머지 줄을 알파벳 순서대로 정렬
    package_list = lines[2:]  # 첫 두 줄을 제거
    sorted_list = sorted(package_list)

    # 정렬된 패키지 목록을 한 줄씩 출력
    for package in sorted_list:
        print(package)