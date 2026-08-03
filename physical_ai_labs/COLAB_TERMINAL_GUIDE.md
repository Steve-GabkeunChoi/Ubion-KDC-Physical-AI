# Colab 터미널 실행 가이드

1. Colab에서 **터미널**을 연다.
2. 왼쪽 파일 패널의 업로드 기능으로 ZIP을 `/content`에 올린다.
3. 터미널에서 압축을 풀고 실행한다.

```bash
cd /content
unzip physical_ai_colab_labs_bundle.zip
cd physical_ai_labs
chmod +x verify_all.sh
bash verify_all.sh
```

개별 실습에서는 코드셀을 사용하지 않고 `nano`, `python3`, `bash`, `cat`, `head`, `ls`만 사용한다.
