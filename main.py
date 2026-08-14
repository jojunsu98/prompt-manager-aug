categories = [
    "텍스트 생성",
    "이미지 생성",
    "영상 생성",
    "페르소나",
    "자동화",
    "기타"
]

prompts = [
    {
        "title": "아침 이슈 브리핑",
        "content": "매일 오전 9시마다 지난 24시간의 사회복지, 정신건강, 청년정책, AI, 창원 지역 이슈를 검색해서 출처와 함께 요약해 줘. 중요한 내용이 없는 분야는 생략하고 5분 안에 읽을 분량으로 작성해 줘.",
        "category": "자동화",
        "favorite": False
    },
    {
        "title": "AI 기술 뉴스 3줄 요약",
        "content": "기사 제목과 RSS 요약문을 바탕으로 한국어로 작성해 줘. 전체 출력은 최대 3줄, 각 줄은 한 문장으로 작성하고 핵심 사실과 의미만 정리해 줘. 입력에 없는 정보는 추측하지 말고 정보가 부족하면 세부 내용 확인 필요라고 표시해 줘.",
        "category": "텍스트 생성",
        "favorite": False
    },
    {
        "title": "개인 지출 자동 분류",
        "content": "Google Form으로 입력된 지출 기록을 확인하고 지출 금액이 50000원 이상이면 고액 지출로, 50000원 미만이면 일반 지출로 분류해 줘. 분류 결과를 각각의 Google Sheets에 저장하고 고액 지출이면 Gmail 알림을 보내도록 처리해 줘.",
        "category": "자동화",
        "favorite": False
    }
]

def add_prompt():
    print("\n=== 프롬프트 추가 ===")

    title = input("제목: ").strip()
    while not title:
        print("제목은 비워둘 수 없습니다.")
        title = input("제목: ").strip()

    content = input("내용: ").strip()
    while not content:
        print("내용은 비워둘 수 없습니다.")
        content = input("내용: ").strip()

    print("\n카테고리 선택:")
    for i, category in enumerate(categories, start=1):
        print(f"{i}) {category}")

    while True:
        choice = input("번호 선택 또는 카테고리 직접 입력: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            category = categories[int(choice) - 1]
            break

        if choice:
            category = choice

            if category not in categories:
                categories.append(category)

            break

        print("카테고리를 입력해주세요.")

    new_prompt = {
        "title": title,
        "content": content,
        "category": category,
        "favorite": False
    }

    prompts.append(new_prompt)
    print("\n프롬프트가 추가되었습니다!")

def show_list():
    print("\n=== 프롬프트 목록 ===")

    if not prompts:
        print("저장된 프롬프트가 없습니다.")
        return

    for i, prompt in enumerate(prompts, start=1):
        star = " ⭐" if prompt["favorite"] else ""
        print(f"{i}. [{prompt['category']}] {prompt['title']}{star}")

    print(f"\n총 {len(prompts)}개의 프롬프트")

def show_by_category():
    print("\n=== 카테고리별 조회 ===")

    for i, category in enumerate(categories, start=1):
        print(f"{i}) {category}")

    while True:
        choice = input("선택: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            selected_category = categories[int(choice) - 1]
            break

        print("올바른 번호를 입력해주세요.")

    results = [
        prompt for prompt in prompts
        if prompt["category"] == selected_category
    ]

    if not results:
        print(f"\n[{selected_category}] 카테고리에 프롬프트가 없습니다.")
        return

    print(f"\n[{selected_category}] 카테고리 프롬프트:")

    for i, prompt in enumerate(results, start=1):
        star = " ⭐" if prompt["favorite"] else ""
        print(f"{i}. {prompt['title']}{star}")

    print(f"\n총 {len(results)}개의 프롬프트")

def search_prompt():
    print("\n=== 프롬프트 검색 ===")

    keyword = input("검색어: ").strip()

    if not keyword:
        print("검색어를 입력해주세요.")
        return

    results = [
        prompt for prompt in prompts
        if keyword.lower() in prompt["title"].lower()
        or keyword.lower() in prompt["content"].lower()
    ]

    if not results:
        print("검색 결과가 없습니다.")
        return

    print("\n검색 결과:")

    for i, prompt in enumerate(results, start=1):
        star = " ⭐" if prompt["favorite"] else ""
        print(f"{i}. [{prompt['category']}] {prompt['title']}{star}")

    print(f"\n{len(results)}개의 프롬프트를 찾았습니다.")

def show_detail():
    print("\n=== 프롬프트 상세 보기 ===")

    if not prompts:
        print("저장된 프롬프트가 없습니다.")
        return

    show_list()

    while True:
        choice = input("\n프롬프트 번호 입력: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(prompts):
            prompt = prompts[int(choice) - 1]
            break

        print("올바른 번호를 입력해주세요.")

    favorite = "⭐" if prompt["favorite"] else "X"

    print("\n────────────────────────────")
    print(f"제목: {prompt['title']}")
    print(f"카테고리: {prompt['category']}")
    print(f"즐겨찾기: {favorite}")
    print("────────────────────────────")
    print("내용:")
    print(prompt["content"])
    print("────────────────────────────")

def toggle_favorite():
    print("\n=== 즐겨찾기 관리 ===")

    if not prompts:
        print("저장된 프롬프트가 없습니다.")
        return

    show_list()

    while True:
        choice = input("\n프롬프트 번호 입력: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(prompts):
            prompt = prompts[int(choice) - 1]
            break

        print("올바른 번호를 입력해주세요.")

    prompt["favorite"] = not prompt["favorite"]

    if prompt["favorite"]:
        print(f"'{prompt['title']}' 프롬프트를 즐겨찾기에 추가했습니다!")
    else:
        print(f"'{prompt['title']}' 프롬프트를 즐겨찾기에서 해제했습니다!")


def show_favorites():
    print("\n=== 즐겨찾기 목록 ===")

    favorites = [
        prompt for prompt in prompts
        if prompt["favorite"]
    ]

    if not favorites:
        print("즐겨찾기된 프롬프트가 없습니다.")
        return

    for i, prompt in enumerate(favorites, start=1):
        print(f"{i}. [{prompt['category']}] {prompt['title']} ⭐")

    print(f"\n총 {len(favorites)}개의 즐겨찾기")

def show_menu():
    print("\n=== 나만의 프롬프트 관리 ===")
    print("1. 프롬프트 추가")
    print("2. 프롬프트 목록")
    print("3. 카테고리별 조회")
    print("4. 프롬프트 검색")
    print("5. 프롬프트 상세 보기")
    print("6. 즐겨찾기 관리")
    print("7. 즐겨찾기 목록")
    print("0. 종료")


while True:
    show_menu()
    choice = input("선택: ").strip()

    if choice == "1":
        add_prompt()
    elif choice == "2":
        show_list()
    elif choice == "3":
        show_by_category()
    elif choice == "4":
        search_prompt()    
    elif choice == "5":
        show_detail()
    elif choice == "6":
        toggle_favorite()
    elif choice == "7":
        show_favorites() 
    elif choice == "0":
        print("프로그램을 종료합니다.")
        break
    else:
        print("올바른 메뉴 번호를 입력해주세요.")