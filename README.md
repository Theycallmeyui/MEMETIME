# MEME-TIME!

## 1. 프로젝트 소개
Meme-Time!는 사용자의 표정, 손동작 및 자세를 실시간으로 인식하여 이에 대응하는 짤(Meme)을 추천해주는 컴퓨터 비전 프로젝트이다.본 프로젝트는 OpenCV와 MediaPipe Holistic을 활용하여 웹캠 영상으로부터 얼굴(Face), 손(Hand), 자세(Pose) 랜드마크를 추출하고,각 랜드마크의 위치 관계를 분석하여 사용자의 행동을 분류한다.분류된 행동에 따라 적절한 짤 이미지를 화면에 출력하여 사용자와 상호작용하는 재미있는 프로그램을 구현하였다.

---

## 2. 개발 목표

- 실시간 웹캠 입력 처리
- 사람의 포즈 검출
- 포즈 분류
- 포즈에 맞는 짤 이미지 표시

---

## 3. 개발 환경

Python 3.x
OpenCV
MediaPipe Holistic
NumPy
Webcam

---

## 4. 데이터셋
본 프로젝트는 다음과 같은 표정을 인식한다.

4.1 No Pose - 사용자가 특별한 행동을 하지 않을 경우 기본 상태로 인식한다.

출력 이미지:
![No Pose](memes/no_pose/confused_math.jpg)

4.2 Peace Sign - 검지와 중지를 펴고 나머지 손가락을 접은 상태를 인식한다.

출력 이미지:
![Peace](memes/peace/peace_hamster.jpg)

4.3 Finger Heart -  손가락 하트를 인식한다.

출력 이미지:
![Finger Heart](memes/finger_heart/monkey.jpg)

4.4 Thumbs Up - 엄지가 위를 향하고 나머지 손가락이 접힌 상태를 인식한다.

출력 이미지:
![Finger Heart](memes/thumbs_up/hamster.jpg)

4.5 Hold On - 손바닥을 펼친 상태를 인식한다.

출력 이미지:
![stop_hand](memes/stop_hand/hold_on_please.jpg)

4.6 Big Smile - 입의 가로 길이와 세로 길이 비율을 이용하여 웃는 표정을 인식한다.

출력 이미지:
![Smile](memes/smile/Hamster.jpg)

4.7 Mouth Open - 입을 크게 벌린 상태를 인식한다.
출력 이미지:
![Questioning](memes/questioning/questioning.jpg)

4.8 Smirk - 좌우 입꼬리 높이 차이를 이용하여 비웃는 표정을 인식한다.

출력 이미지:
![Smirk](memes/smirk/smirk.jpg)

4.9 Me? - 사용자가 자신의 가슴을 손가락으로 가리키는 동작을 인식한다.

출력 이미지:
![Me](memes/me/me.jpg)

4.10 Finger Bite - 손가락이 입 근처에 위치하는 경우를 인식한다.

출력 이미지:
![Finger Bite](memes/finger_bite/finger_bite.jpg)

4.11 Stressed - 손이 이마에 가까이 위치하는 경우를 인식한다.

출력 이미지:
![Stressed](memes/stressed/stressed.jpg)

---

## 5. 프로젝트 결과
MediaPipe Holistic을 활용하여 얼굴, 손, 자세 정보를 동시에 추출할 수 있었으며, 이를 이용하여 다양한 표정과 포즈를 실시간으로 인식할 수 있었다.특히 Peace Sign, Finger Heart, Thumbs Up, Hold On, Big Smile은 비교적 안정적으로 동작하였다. 일부 복합 동작(Finger Bite, Me?, Stressed)은 사용자 자세와 카메라 각도에 따라 인식률 차이가 발생할 수 있었다. 전체적으로 사용자의 행동에 따라 적절한 짤을 추천하는 실시간 시스템을 성공적으로 구현하였다.

---

## 6. 실행 방법
terminal 에서 pip install -r requirements.txt, python main.py.
ESC 키를 누르면 프로그램이 종료된다.

---

## 7. 실행 결과

프로젝트 실행 결과는 screenshots 폴더의 이미지들을 통해 확인할 수 있다.

---

## 8. 참고 자료 (References)

Technical References - OpenCV Documentation https://docs.opencv.org/ , MediaPipe Holistic Documentation https://developers.google.com/mediapipe

Idea References - TikTok 콘텐츠

지원 도구 - ChatGPT

---
