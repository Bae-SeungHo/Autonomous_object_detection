2021 자율주행영상 객체 검출 경진대회 
==============================


들어가기에 앞서
----------
안녕하세요 여러분!

저는 영남대학교 정보통신공학과 3학년에 학부연구생으로 공부하고 있는 배승호입니다. 

컴퓨터 비전 분야는 제가 가장 좋아하는 학술 분야이며, 해당 경진대회의 본선에 참여할 수 있다는 것은 저에게 매우 의미있는 경험입니다.

이 경진대회에서 다루는 자율주행영상을 통하여 도로 위의 객체를 탐지하는 모델을 ***파이썬***과 ***YOLOv5*** 를 통해서 구현해보겠습니다.

저의 팀 명은 ***Doge AI*** 입니다! 


### 1. 개발 환경
---
이 경진대회에서 저는 Windows 10 환경에서 pytorch 기반 YOLOv5 모델을 사용하고자 합니다. 

그에 따라 아나콘다로 가상 환경을 새로 만들었고, 폴더의 requirements.txt 의 패키지를 통해 필수 라이브러리를 설치합니다.

![가상환경](https://user-images.githubusercontent.com/77887166/146162056-7ad3f243-29c2-426b-b596-188b60bb07cc.PNG) 가상환경 생성 (아나콘다)

![requirements](https://user-images.githubusercontent.com/77887166/146162774-8b646757-6586-4f59-b41f-e5cc3f3b65e4.PNG) 

경로에 이동하여 requirements.txt 의 패키지를 설치합니다.

```cmd
pip install -r requirements.txt
```



### 2. 전처리 (preprocess.py)
---

전처리 단계를 거치는 이유는 크게 두 가지입니다.

첫번째로는 학습 이미지의 해상도가 매우 크고 (Full HD) , 개수 또한 방대하기 때문에

저의 컴퓨팅 자원(GTX 1660으로 학습하기 한계가 있기 때문에

이미지의 크기를 축소하기 위해 사용합니다. (필자의 경우 640 X 480 으로 설정하였고, preprocess.py 의 인자로 변경할 수 있습니다.)
 
두번째는, YOLO에서 사용하는 라벨링 포멧과 제공되는 라벨 데이터의 포멧이 다르기 때문에 

포멧을 일치시키기 위해 사용합니다.

preprocess.py 의 인자는 다음과 같습니다.

![preprocess](https://user-images.githubusercontent.com/77887166/146164381-94cdd36d-5a47-4c87-9bcb-885eb3c75aaf.PNG)

   1. -raw : 학습 이미지와 라벨 데이터가 있는 폴더 경로입니다 (기본 : Datasets/raw) * 변경할경우 YOLO/data.yaml 파일도 수정해야 함
   2. -img : 변경할 이미지 사이즈입니다. (기본 : 640)
   3. -path : 변경된 이미지와 라벨 데이터가 저장될 경로입니다. (기본 : Datasets/train)
   4. -mode : 학습 또는 검증 데이터 종류입니다. (기본 : train)


기본적으로 아무 인자를 변경하지 않고 실행할 수 있습니다. (단. Datasets/raw 폴더 내에 학습데이터가 위치하여야 함)

```cmd
python preprocess.py 
```
![preprocess-done](https://user-images.githubusercontent.com/77887166/146165285-7f0a1f6c-7bfc-450e-a50c-9c63ea5b0714.PNG) 

재연을 위해 327개의 이미지/라벨 데이터만 사용하였고, 정상적으로 작동하면 Datasets/train 폴더 내에 images , labels 폴더와 전처리된 파일들이 생성됩니다.



### 3. 학습 (train.py)
---

학습에는 제한된 컴퓨팅 자원으로 인해 yolov5 모델 중 가벼운 모델인 Yolov5s 모델을 사용하였습니다. 

train.py 의 인자는 다음과 같습니다.

![train](https://user-images.githubusercontent.com/77887166/146165918-7785a404-9ffe-45cb-8c12-85141405cb3b.PNG)

   1. -weights : 학습 가중치 파일의 경로입니다. 기존 모델을 추가로 학습하는 경우 입력이 필요합니다. (기본 : YOLO/yolov5s.pt) 
   2. -epochs : 학습 반복 횟수입니다. (기본 : 10)
   3. -batch : 학습 배치 사이즈입니다. (기본 : 4)
   4. -img : preprocess 에서 리사이즈 한 이미지 크기입니다 (기본 : 640)

필자의 컴퓨터에서는 (5 Epochs + 4 Batch size) * 6회 반복했을 때 100시간 가량 소모되었습니다.

```cmd
python train.py 
```

![image](https://user-images.githubusercontent.com/77887166/146167569-1ea3d9e4-45fb-4b04-8197-68f07620a9b8.png)


학습이 완료되면 최상위 폴더 중 Model 폴더에 "model.pt"  이름으로 저장됩니다.



### 4. 예측 (inference.py)
---

학습이 완료된 후 생성된 모델을 통해 예측할 수 있습니다.

예측하고자 하는 데이터를 Datasets/test 폴더 내에 옮기고 inference.py 를 실행하면 예측이 진행됩니다.

![inference](https://user-images.githubusercontent.com/77887166/146168053-e98c1c2d-2502-4035-a3dd-d1130339ae66.PNG)

   1. -model : 학습된 모델의 경로입니다. (기본 : Model/)
   2. -img : preprocess 에서 리사이즈 한 이미지 크기입니다 (기본 : 640)
   3. -conf : 예측한 확률의 임계값을 조절합니다. (기본 : 0.6)
   4. -path : 예측된 라벨 데이터가 저장되는 경로입니다. (기본 : Datasets/test)
   5. -source : 예측할 이미지 경로입니다. (기본 : Datasets/test)
   6. -name : 저장될 폴더 이름입니다. (기본 : result)

인자는 수정할 수 있지만 경로에 관련된 인자는 기본값을 사용하는것을 권장합니다.

```cmd
python inference.py
```

실행하면 test 폴더 내에 Result 폴더가 각 폴더별로 생성되며, 예측한 객체 위치를 txt파일로 저장됩니다.

![inference-done](https://user-images.githubusercontent.com/77887166/146171972-89e5c360-eedc-43a1-bcf5-801773a81c63.PNG)


### 5. 후처리 (postprocess.py)
---

예측한 뒤, 마지막으로 라벨 데이터를 txt 파일에서 기존 포멧에 맞게 변경해야 합니다.

postprocess.py 의 인자는 다음과 같습니다.

![postprocess](https://user-images.githubusercontent.com/77887166/146172341-378340e8-c168-40e1-bc50-7e4d79db692e.PNG)

   1. -path : 후처리될 라벨 데이터의 경로입니다. (기본 : Datasets/test)
   2. -width : 원본 이미지의 너비 입니다. (기본 : 1920)
   3. -height : 원본 이미지의 높이 입니다. (기본 : 1080)

```cmd
python postprocess.py
```


![postprocess-done](https://user-images.githubusercontent.com/77887166/146172891-35cc7dd5-0272-497e-a353-92758a551e3f.PNG)

postprocess.py 를 실행하면 기존 포맷에 맞게 좌표값 형태와 파일 형식이 변경되며, 기존 txt파일은 삭제됩니다.




### 5. 마치며
---

이로써, 전처리부터 테스트 데이터 예측까지의 모든 과정이 끝났습니다.

객체 검출 모델은 많은 클래스 중 Vehicle (차량) , Pedestarian (보행자) , TrafficLight (신호등) , TrafficSign (표지판) 을 분류합니다.

경연을 진행하면서 학습 데이터가 방대하여 높은 정확도의 모델을 만들 수 있어 매우 흥미로웠고,

경연 주제는 네개의 클래스만을 분류하는 것이 목표이지만,

표지판 , 신호등 중에서도 적색불 , 청색불 , 멈춤 표지판 , 주행제한 표지판 등을 추가로 분류해보고 싶을 정도로

흥미로운 경연이였습니다 ! 



