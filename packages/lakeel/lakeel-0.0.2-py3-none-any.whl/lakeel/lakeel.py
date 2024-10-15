import platform
import subprocess
import sys
import importlib.util

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
        print("matplotlib 가 설치되어 있지 않습니다")
        install('matplotlib')
    else:
        print(":)")

    import matplotlib.pyplot as plt
    from matplotlib import rc

    if current_os == 'Darwin':  # macOS
        print("폰트가 AppleGothic font 로 설정되었습니다.")
        rc('font', family='AppleGothic')
        
    elif current_os == 'Windows':  # Windows
        print("폰트카 Malgun Gothic font 로 설정되었습니다.")
        rc('font', family='Malgun Gothic')
        
    else:
        print(f"Unknown OS: {current_os}. Please set the font manually.")

    # 음수 부호 깨짐 방지
    plt.rcParams['axes.unicode_minus'] = False
    print("Font setup is complete.")

# 폰트 설정 실행
sfo()
