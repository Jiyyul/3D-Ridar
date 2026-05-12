# Robotics Workspace Collection

이 저장소는 자율주행 로봇 실험과 SLAM, 센서 연동, 경로 계획을 위한 여러 ROS 워크스페이스와 외부 라이브러리를 한 곳에 모아둔 작업공간입니다.

GitHub에서 이 저장소를 처음 열었을 때, 각 하위 프로젝트가 어떤 역할을 하는지 빠르게 확인하고 원하는 워크스페이스로 바로 진입할 수 있도록 정리한 루트 README입니다.

## 포함된 구성

- `forza_ws/race_stack`: ForzaETH 기반 ROS 2 레이스 스택
- `realsense_ws/src/realsense-ros`: Intel RealSense ROS 연동
- `rtabmap_ws/src`: RTAB-Map 기반 SLAM 및 맵핑 작업공간
- `g2o`: 그래프 최적화 라이브러리
- `Documents/librealsense2/presets`: RealSense 프리셋 및 설정 파일
- `shared_dir`: 맵, 파라미터, 모델, 공유 리소스

## 목적

- 자율주행 및 실내/실외 로봇 실험 환경 구성
- 라이다, 카메라, IMU 등 센서 데이터 처리
- SLAM, 상태추정, 상태기계, 경로계획, 제어 모듈 통합
- 시뮬레이션과 실차 환경을 동일한 구조로 관리

## 주요 워크스페이스

### `forza_ws/race_stack`
ROS 2 기반 레이스 스택입니다. 상태기계, 상태추정, 계획기, 제어기, 인지 모듈이 포함되어 있으며 시뮬레이션과 실차 운영을 함께 다루는 구조입니다.

자세한 실행 방법은 해당 폴더의 README를 확인하세요.

### `rtabmap_ws`
RTAB-Map 기반 SLAM 테스트와 관련된 워크스페이스입니다. 지도를 만들거나 로컬라이제이션을 확인할 때 사용합니다.

### `realsense_ws`
Intel RealSense 카메라와 ROS 드라이버를 연동하는 워크스페이스입니다. 센서 입력과 캘리브레이션, 파이프라인 확인에 사용합니다.

### `g2o`
그래프 최적화에 사용하는 외부 라이브러리입니다. SLAM, pose graph optimization, bundle adjustment 계열 작업에서 사용됩니다.

## 권장 환경

- Ubuntu 22.04
- ROS 2 Humble
- `colcon` 빌드 도구
- `git`
- 필요한 경우 `docker` 및 `docker compose`

## 시작 방법

각 워크스페이스는 독립적으로 관리하는 것을 권장합니다.

```bash
source /opt/ros/humble/setup.bash
cd ~/forza_ws/race_stack
colcon build --symlink-install
```

RealSense, RTAB-Map, g2o도 각각 해당 디렉터리에서 동일한 방식으로 빌드하거나, 저장소에 포함된 안내 문서를 따라 설정하세요.

## 참고

- 각 패키지별 실행 방법은 하위 README를 우선 확인하세요.
- `build`, `install`, `log` 디렉터리는 빌드 산출물입니다.
- 공유 자원은 `shared_dir`에 모아 두는 구성을 권장합니다.

## License

이 저장소는 여러 외부 프로젝트와 패키지를 포함할 수 있습니다. 각 하위 디렉터리의 라이선스를 우선 확인하세요.
