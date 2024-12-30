# Medibook Project
<div align="center" margin="20px 0">
  <br/><br/>
    <img alt="image" src="https://github.com/hyeonji423/project_front/blob/main/src/assets/medi_logo.png?raw=true">
  <br/><br/>
</div>


# Medibook Web Page v1.0
> **코드랩 아카데미 AICC 4기 2팀** <br/> **개발기간: 2024. 11. 20 ~ 2024. 12. 19**<br/>
## 배포 주소
> **백엔드 서버** : [https://back.aicc4hyeonji.site](https://back.aicc4hyeonji.site)<br>
> **데이터베이스** : [AWS-postgresql](https://107.21.20.220)<br>


## 웹개발팀 소개
> **김용주**, **유인규**, **이경욱**, **이영선**, **황현지**


## 프로젝트 소개
코로나 이후 건강에 대한 관심이 올라가게 되면서, 스스로 처방을 내리고 구매 및 복용을 하는 <셀프 메디케이션>에 관심이 커지고 있습니다. 이에 따라 손쉽게 구매및 복용이 가능한 일반의약품, 건강기능식품에 대한 약물 오남용이 우려되는 상황이 발생하게 되었습니다.

저희는 이런 상황을 개선하기 위해 약물의 효능, 성분, 부작용을 잘 파악하여 안전한 셀프 메디케이션을 할 수 있도록 돕는 가정용 약물 정보 및 관리 사이트 **메디북**을 개발하였습니다.


## 시작 가이드
### Requirements
For building and running the application you need:
- [Node.js v20.18.0](https://nodejs.org/ko/download/package-manager)
- [Npm 10.8.2](https://www.npmjs.com/package/npm/v/9.2.0)
- [Python 3.12.7](https://www.python.org/downloads/windows/)
### Installation
> **Backend**
``` backend
$ git clone https://github.com/hyeonji423/team2backprod.git
$ cd team2backprod
```
```
$ npm install
$ npm run start
```

---
## Stacks💊
### Environment
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-007ACC?style=for-the-badge&logo=Visual%20Studio%20Code&logoColor=white)
![Cursor](https://img.shields.io/badge/Cursor-000000?style=for-the-badge&logo=Cursor&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white)
![Github](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=white)
![Postgresql](https://img.shields.io/badge/Postgresql-4169E1?style=for-the-badge&logo=Postgresql&logoColor=white)

### Config
![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=Node.js&logoColor=white)
![npm](https://img.shields.io/badge/npm-CB3837?style=for-the-badge&logo=npm&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white)
![pip](https://img.shields.io/badge/pip-3776AB?style=for-the-badge&logo=pip&logoColor=white)
![Swagger](https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=Swagger&logoColor=white)
![Express](https://img.shields.io/badge/Express-000000?style=for-the-badge&logo=Express&logoColor=white)

### Communication
![Slack](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=Slack&logoColor=white)
![GoogleDrive](https://img.shields.io/badge/GoogleDrive-4285F4?style=for-the-badge&logo=GoogleDrive&logoColor=white)


---
## 아키텍쳐
### 디렉토리 구조
```bash
│
└── back : 백엔드
    │
    ├── README.md
    │
    ├── database : 데이터베이스 관련 정보 폴더
    │   ├── database.js : 기본 개발 환경(NODE_ENV = development)에서 database 설정 파일
    │   └─── db.sql
    │ 
    ├── controllers
    │   ├── AuthCtrl : post, update, delete (회원가입, 로그인, 비밀번호 변경, 회원탈퇴)
    │   ├── MyMediCtrl : post, get, update, delete (약품 등록, 수정, 삭제, 목록)
    │   ├── getMediInfoCtrl.js : 일반의약품 정보/검색
    │   └── emailCtril.js : 이메일 인증/알림/건의사항 수신
    │
    ├── routes
    │   ├── authRoutes.js
    │   ├── myPageRoutes.js
    │   ├── searchRoutes.js
    │   └── emailRoutes.js
    │
    ├── vector_cache
    │   ├── index.faiss
    │   └── index.pkl
    │
    ├── data.json
    ├── chat1.py
    │
    ├── index.js
    │
    ├── requirement.txt
    │
    ├── package.json
    │
    └── .env : 환경변수 파일(데이터베이스, 이메일, 오픈API 관련 정보)



