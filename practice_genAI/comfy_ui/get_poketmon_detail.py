import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
from io import BytesIO
from PIL import Image

# 기본 URL
BASE_URL = "https://pokemondb.net"
TARGET_URL = f"{BASE_URL}/pokedex/game/scarlet-violet"

# 저장 폴더
SAVE_DIR = "./practice_genAI/comfy_ui_tutorial/pokemon_highres_jpg"
os.makedirs(SAVE_DIR, exist_ok=True)

# User-Agent 설정
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# 1. 포켓몬 목록 페이지 파싱
resp = requests.get(TARGET_URL, headers=headers)
soup = BeautifulSoup(resp.text, "html.parser")

pokemon_blocks = soup.select(".infocard")

print(f"총 {len(pokemon_blocks)}마리의 포켓몬을 찾았습니다.")

for block in tqdm(pokemon_blocks):
    name_tag = block.select_one(".ent-name")
    name = name_tag.text.strip()
    pokemon_url = BASE_URL + name_tag['href']

    try:
        detail_resp = requests.get(pokemon_url, headers=headers)
        detail_soup = BeautifulSoup(detail_resp.text, "html.parser")

        # 고화질 일러스트 이미지 추출
        img_tag = detail_soup.select_one(".grid-col.span-md-6.text-center img")
        if img_tag and "src" in img_tag.attrs:
            img_url = img_tag["src"]
            if img_url.startswith("//"):
                img_url = "https:" + img_url

            # 이미지 다운로드
            img_response = requests.get(img_url)
            image = Image.open(BytesIO(img_response.content)).convert("RGB")

            # 저장 (JPG 형식)
            filepath = os.path.join(SAVE_DIR, f"{name}.jpg")
            image.save(filepath, format="JPEG", quality=95)

            print(f"[✓] 저장 완료: {name}")
        else:
            print(f"[!] 이미지 없음: {name}")

        time.sleep(0.5)  # 서버 과부하 방지

    except Exception as e:
        print(f"[X] 오류 발생 ({name}): {e}")
