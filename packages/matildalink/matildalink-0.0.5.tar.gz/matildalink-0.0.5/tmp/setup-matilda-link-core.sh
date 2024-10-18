#!/bin/bash

###
### - matilda-link-core "개발" 환경 셋업 - shell 포맷으로 정리
### - 사무실 GPU 서버 10.100.7.87을 개발환경으로 가정
### - 로컬이나 10.100.7.87에서 바로 동작하지는 않고, matilda-link-core 또
###   workload 배포 containerization 시 참고가 되는 목적으로만 작성됨
### - 거의 동일하나, 좀 더 자세한 내용은: https://www.notion.so/Matilda-Link-381162a934174585812e2b9e4f21b8d7?p=dc6303014be64c3aa4fdfb9416a4fb9c&pm=s
###

###
### 0. Python 버전
### 
python --version # Python 3.10.14 // conda 환경에서 진행중 (아래 SkyPilot 설치과정 참고)

###
### 1. GPU 서버 새 새용자 추가
###

# 일단 matilda 사용자로 접속
ssh matilda@10.100.7.87
# 서버에서 새 사용자 생성 및 sudo 권한 부여
sudo adduser [your-user-name]
sudo usermod -aG sudo [your-user-name]
# 이후 새 사용자로 접속
ssh [your-user-name]@10.100.7.87

###
### 2. Conda (Miniconda) 설치
###

# Miniconda 설치
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh

# Miniconda 초기화
~/miniconda3/bin/conda init bash
# 서버 재접속 후 아래와 같이 확인
conda --version # conda 24.7.1

### 
### 3. SkyPilot 설치 (latest release)
###

# Conda 환경 셋업
conda create -y -n [your-conda-env] python=3.10
conda activate [your-conda-env]

# SkyPilot 설치
pip install "skypilot[all]"

###
### 4. SkyPilot에 연동할 AWS IAM IC 셋업
###   - SkyPilot 설치 과정에서는 기본적으로 AWS CLI v1을 설치함
###   - AWS IAM IC 사용을 위해서는 AWS CLI v2를 아래와 같이 별도 설치해줘야 함
###

##
## 4-1. AWS CLI v2 설치
##

# SkyPilot 설치 과정에서 설치된 AWS CLI v1 삭제
pip3 uninstall awscli
# AWS CLI v2 설치
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
# 아래와 같이 확인
aws --version # aws-cli/2.17.41 Python/3.11.9 Linux/5.15.0-122-generic exe/x86_64.ubuntu.20

##
## 4-2. AWS CLI에 IAM IC 인증 셋업
##

# 아래 두 가지 필요 정보 기록
# - 위치: AWS access portal -> PowerUserAccess -> Access keys 창 열기
[SSO Start URL]
[SSO Region]

# aws configure sso 통해 (interactive하게) 프로필 세팅
aws configure sso
'SSO session name (Recommended):' [your-session-name] # 원하는 세션 이름 입력
'SSO start URL [None]:' [SSO Start URL] # 앞서 기록한 SSO Start URL
'SSO region [None]:' [SSO Region] # 앞서 기록한 SSO Region
'SSO registration scopes [sso:account:access]:' # 엔터키

# 출력되는 URL(SSO authorization page)에 들어가서 함께 출력된 code 입력 후 인증
PowerUserAccess Role # 이것 선택
'CLI default client Region [None]:' us-east-1 # 우리 클러스터 리전
'CLI default output [None]:' json
'CLI profile name [PowerUserAccess-890742610607]:' [your-profile-name] # 원하는 프로필 이름 입력

# IAM IC 세션에 log in
aws sso login --profile [your-profile-name]

# 출력되는 URL(SSO authorization page)에 들어가서 함께 출력된 code 입력하여 인증

# 확인 (여기까지 동작하면 IAM IC 세팅 준비됨)
aws sts get-caller-identity --profile [your-profile-name]

##
## 4-3. 환경변수 설정
##

vim ~/.bashrc
export AWS_DEFAULT_PROFILE=[your-profile-name] # 맨 마지막에 이렇게 한 줄 추가

# Shell 종료 후 서버 재접속

##
## 4-4. SkyPilot with AWS 동작 확인
##

conda activate [your-conda-env]
sky check aws

# 아래와 같이 메시지 나오면 잘 세팅 됨
'
Checking credentials to enable clouds for SkyPilot.
  AWS: enabled
  ...
  Enabled clouds
  - AWS
'

# Detectron2 workload 대상 SkyPilot dryrun 실제 테스트 가능
cd ~/matilda-link/brain/skytest
python3 run.py

###
### 5. 로컬 src/로부터 matildalink 패키지 설치 (개발용, editable installation)
###

# matildalink 패키지 개발하면서 실제 스스로를 numpy처럼 외부 패키지인 양 import 화면서 개발/테스트 가능
# - 예: import matildalink.predictor
conda activate sky
cd ~/matilda-link
python3 -m pip install --editable .

# 실제 동작에서는 PyPI에 배포된 버전을 사용
