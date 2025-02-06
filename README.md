### 필요한 라이브러리 설치
```
pip install websockets
```

```
pip install python-dotenv
```

혹은
```
pip install -r requirements.txt
```

### 로컬 구동을 위한 env 설정
루트의 .env 파일
```
AWS_ACCESS_KEY=your_aws_access_key
AWS_SECRET_KEY=your_aws_secret_key
```

### 배포를 위한 env secret 설정
필요시 yml 파일 수정
```
AWS_ACCESS_KEY
AWS_SECRET_KEY
```

### 서버 실행
```
python server.py
```