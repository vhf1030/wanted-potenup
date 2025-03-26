import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# 크롤링 대상 URL
BASE_URL = "https://pokemondb.net"
TARGET_URL = "https://pokemondb.net/pokedex/game/scarlet-violet"

# 저장 폴더
SAVE_DIR = "./practice_genAI/comfy_ui_tutorial/pokemon_images_120"
os.makedirs(SAVE_DIR, exist_ok=True)

# HTML 요청
response = requests.get(TARGET_URL)
soup = BeautifulSoup(response.text, 'html.parser')

# 모든 포켓몬 블록 추출
pokemon_blocks = soup.select(".infocard")

print(f"총 {len(pokemon_blocks)}마리의 포켓몬을 찾았습니다.")

for block in tqdm(pokemon_blocks):
    # 포켓몬 이름 추출
    name_tag = block.select_one(".ent-name")
    name = name_tag.text if name_tag else "unknown"

    # 이미지 URL 추출
    img_tag = block.select_one("img")
    if img_tag and "src" in img_tag.attrs:
        img_url = img_tag["src"]
        if img_url.startswith("//"):
            img_url = "https:" + img_url

        # 이미지 저장
        img_data = requests.get(img_url).content
        filename = f"{name}.png"
        filepath = os.path.join(SAVE_DIR, filename)
        

        with open(filepath, "wb") as f:
            f.write(img_data)

print("✅ 모든 이미지 저장 완료!")
