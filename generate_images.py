import requests, os, time
from urllib.parse import unquote

API_KEY = "sk-cp-ia--VDcwqsvwd9sPhSKC4RQrecU_ISvjcefqUkSR7J82ZbiBx-Hq5gtBeSoqknu_RWjHTPaGk7uvi6xbviBZ_qBu6dkUUBc14Z-vrvcbQwgHnzWzU_UgKfU"
URL = "https://api.minimaxi.com/v1/image_generation"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

chapters = [
    (1, "chapter01_山村少年.md", "苍茫大山深处，清溪村，清晨薄雾缭绕，百年老槐树，树下少年陈墨砍柴归来，小麦色皮肤，憨厚笑容"),
    (2, "chapter02_灵根觉醒.md", "觉醒仪式，测灵台，青铜古鼎上方金色光芒冲天而起，少年陈墨站在台上，万众瞩目，璀璨耀眼，测灵师震惊后退"),
    (3, "chapter03_离去.md",     "山谷幽静之处，青色飞舟即将启程，少年陈墨与周长风告别，爷爷陈老实在村口老槐树下遥望，月光下古玉泛着淡青荧光"),
    (4, "chapter04_宗门大选.md", "清晨云海之上，青色飞舟翱翔，远处青雲峰巍峨耸立，云雾缭绕，殿宇楼阁若隐若现，气势恢宏，少年陈墨立于船头心驰神往"),
    (5, "chapter05_宗门生活.md", "青雲宗清晨，晨曦金光洒在亭台楼阁，少年陈墨在小院空地吐纳修炼，周围仙鹤飞翔，仙气缭绕，古朴典雅的仙门建筑"),
    (6, "chapter06_传承试炼.md", "深夜，青雲宗核心区域，黑影刺客逼近小院，陈墨胸前古玉爆发出璀璨青色光芒护体，光芒如烈日，照亮整个夜空"),
    (7, "chapter07_血脉初现.md", "无尽深渊混沌之中，白衣先祖陈玄现身，长髯如瀑，周身散发金色光芒，与少年陈墨对视，传承之力觉醒，天地共鸣"),
    (8, "chapter08_内门争斗.md", "青雲宗执法堂内，气氛凝重，三名黑衣人尸体陈列，执法长老赵无极厉声审问，嫌疑人韩成冷笑相对，少年陈墨神色平静"),
    (9, "chapter09_崭露头角.md", "青雲宗比武广场，人山人海，少年陈墨与金色身影赵天骄在比武台上激烈对决，灵力激荡，光芒四射，众弟子围观惊呼"),
    (10, "chapter10_宗门危机.md", "青雲宗大殿议事，宗主青雲子端坐主位，众长老神色凝重，情报长老报告魔修大军压境，天边血色红云翻涌，大战将至"),
]

def generate_image(scene_desc, output_path, chapter_num):
    prompt = f"古风玄幻小说插画，{scene_desc}，水墨风格，高质量，细节丰富，电影感，氛围感强"
    payload = {
        "model": "image-01",
        "prompt": prompt,
        "aspect_ratio": "3:2",
        "response_format": "url"
    }
    print(f"[第{chapter_num}章] 调用API...")
    try:
        resp = requests.post(URL, headers=HEADERS, json=payload, timeout=120)
        print(f"[第{chapter_num}章] 状态码: {resp.status_code}")
        data = resp.json()
        
        # 尝试提取URL
        img_url = None
        
        # 格式1: data[0].url (常见)
        if "data" in data and isinstance(data["data"], list) and len(data["data"]) > 0:
            img_url = data["data"][0].get("url")
        
        # 格式2: data.image_urls[0] (MiniMax实际返回)
        if not img_url and "data" in data and isinstance(data["data"], dict):
            urls = data["data"].get("image_urls")
            if urls and len(urls) > 0:
                img_url = urls[0]
        
        if not img_url:
            print(f"[第{chapter_num}章] ❌ 无法解析URL: {str(data)[:300]}")
            return False
        
        print(f"[第{chapter_num}章] 下载图片: {img_url[:80]}...")
        
        # 下载图片
        img_resp = requests.get(img_url, timeout=60, headers={"User-Agent": "Mozilla/5.0"})
        print(f"[第{chapter_num}章] 下载状态: {img_resp.status_code}, 大小: {len(img_resp.content)} bytes")
        
        with open(output_path, "wb") as f:
            f.write(img_resp.content)
        
        print(f"[第{chapter_num}章] ✅ 保存成功: {output_path}")
        return True
        
    except Exception as e:
        print(f"[第{chapter_num}章] ❌ 异常: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

for num, fname, scene in chapters:
    img_path = f"D:\\workspace\\novel\\images\\chapter{num:02d}.jpg"
    ok = generate_image(scene, img_path, num)
    if not ok:
        print(f"[第{num}章] ⚠️ 生成失败，跳过")
    time.sleep(5)

print("\n全部完成！")
