# PMS Slamless PCD Generator

자세한 레퍼런스 : https://velog.io/@pddj21/CarlaAutoware-PCD-Map-Generation-in-Carla-Using-ROS-Bag-and-TF-Transformations-without-slam

ROS 2 기반 환경에서 TF 정보를 활용하여 `/carla/hero/semantic_lidar` PointCloud2 토픽을 누적하고 `.pcd` 형식으로 저장하는 슬램리스(SLAM-less) 포인트클라우드 생성 유틸리티입니다.

## 🔍 소개

`slamless-pcd-generator`는 다음과 같은 기능을 수행합니다:

- 지정된 PointCloud2 토픽 구독
- `tf2_ros`를 이용한 `map` 프레임 기준 좌표 변환
- Open3D를 활용한 포인트 누적 및 저장
- Carla 시뮬레이터 등 시뮬레이션 환경에서 사용 가능

> ✅ SLAM을 사용하지 않고, TF 정보만으로 정합된 누적 PCD를 생성할 수 있습니다.

## 🧱 주요 구성 파일

| 파일명              | 설명 |
|-------------------|------|
| `BagProcessor.py` | 핵심 노드. PointCloud2를 TF 기반으로 누적 |
| `pcd_downsample.py` | PCD 파일을 다운샘플링 |
| `pcd_viewer.py`     | Open3D를 이용한 PCD 시각화 |
| `binary_to_ascii.py`| 이진 → ASCII 포맷 변환 도구 |
| `.gitignore`       | Git 관리 제외 설정 |

## ⚙️ 사용 방법

### 1. 환경 설정

- ROS 2 (Humble 이상)
- `open3d`, `transforms3d` 설치 필요

```bash
pip install open3d transforms3d
```

