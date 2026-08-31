categories = [
    "텍스트 생성",
    "이미지 생성",
    "영상 생성",
    "페르소나",
    "자동화",
    "기타",
]


prompts = [
    {
        "title": "아침 이슈 브리핑",
        "content": (
            "매일 오전 9시마다 지난 24시간의 사회복지, 정신건강, 청년정책, AI, "
            "창원 지역 이슈를 검색해서 출처와 함께 요약해 줘. 중요한 내용이 없는 "
            "분야는 생략하고 5분 안에 읽을 분량으로 작성해 줘."
        ),
        "category": "자동화",
        "favorite": False,
    },
    {
        "title": "AI 기술 뉴스 3줄 요약",
        "content": (
            "기사 제목과 RSS 요약문을 바탕으로 한국어로 작성해 줘. 전체 출력은 최대 "
            "3줄, 각 줄은 한 문장으로 작성하고 핵심 사실과 의미만 정리해 줘. 입력에 "
            "없는 정보는 추측하지 말고 정보가 부족하면 세부 내용 확인 필요라고 표시해 줘."
        ),
        "category": "텍스트 생성",
        "favorite": False,
    },
    {
        "title": "개인 지출 자동 분류",
        "content": (
            "Google Form으로 입력된 지출 기록을 확인하고 지출 금액이 50000원 이상이면 "
            "고액 지출로, 50000원 미만이면 일반 지출로 분류해 줘. 분류 결과를 각각의 "
            "Google Sheets에 저장하고 고액 지출이면 Gmail 알림을 보내도록 처리해 줘."
        ),
        "category": "자동화",
        "favorite": False,
    },
    {
        "title": "제품 썸네일 이미지 생성",
        "content": (
            "제품의 핵심 특징이 한눈에 보이는 정사각형 썸네일 이미지를 만들어 줘. "
            "배경은 단순하게 유지하고 제품명과 핵심 혜택을 읽기 쉽게 배치해 줘."
        ),
        "category": "이미지 생성",
        "favorite": True,
    },
    {
        "title": "15초 제품 광고 영상 구성",
        "content": (
            "제품의 문제 상황, 해결 장면, 핵심 장점, 행동 유도 문구가 포함된 15초 광고 "
            "영상의 장면 구성과 내레이션을 순서대로 작성해 줘."
        ),
        "category": "영상 생성",
        "favorite": False,
    },
    {
        "title": "친절한 고객 상담가 페르소나",
        "content": (
            "당신은 복잡한 내용을 쉬운 말로 설명하는 친절한 고객 상담가입니다. 고객의 "
            "질문을 먼저 요약하고 해결 방법을 단계별로 안내해 주세요."
        ),
        "category": "페르소나",
        "favorite": False,
    },
    {
        "title": "회의 준비 체크리스트",
        "content": (
            "회의 목적, 참석자, 사전 자료, 결정할 사항, 후속 작업을 확인할 수 있는 짧은 "
            "체크리스트를 작성해 줘."
        ),
        "category": "기타",
        "favorite": False,
    },
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
    for index, category_name in enumerate(categories, start=1):
        print(f"{index}) {category_name}")

    while True:
        choice = input("번호 선택 또는 새 카테고리 직접 입력: ").strip()

        if choice.isdigit():
            category_number = int(choice)
            if 1 <= category_number <= len(categories):
                category = categories[category_number - 1]
                break

            print("올바른 카테고리 번호를 입력해 주세요.")
            continue

        if choice.lstrip("+-").isdigit():
            print("올바른 카테고리 번호를 입력해 주세요.")
            continue

        if choice:
            category = choice
            if category not in categories:
                categories.append(category)
            break

        print("카테고리를 입력해 주세요.")

    prompts.append(
        {
            "title": title,
            "content": content,
            "category": category,
            "favorite": False,
        }
    )
    print("\n프롬프트가 추가되었습니다!")


def show_list():
    print("\n=== 프롬프트 목록 ===")

    if not prompts:
        print("저장된 프롬프트가 없습니다.")
        return

    for index, prompt in enumerate(prompts, start=1):
        star = " ⭐" if prompt["favorite"] else ""
        print(f"{index}. [{prompt['category']}] {prompt['title']}{star}")

    print(f"\n총 {len(prompts)}개의 프롬프트")


def show_by_category():
    print("\n=== 카테고리별 조회 ===")

    for index, category_name in enumerate(categories, start=1):
        print(f"{index}) {category_name}")

    while True:
        choice = input("선택: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            selected_category = categories[int(choice) - 1]
            break
        print("올바른 번호를 입력해 주세요.")

    results = [
        prompt for prompt in prompts if prompt["category"] == selected_category
    ]

    if not results:
        print(f"\n[{selected_category}] 카테고리의 프롬프트가 없습니다.")
        return

    print(f"\n[{selected_category}] 카테고리 프롬프트:")
    for index, prompt in enumerate(results, start=1):
        star = " ⭐" if prompt["favorite"] else ""
        print(f"{index}. {prompt['title']}{star}")

    print(f"\n총 {len(results)}개의 프롬프트")


def search_prompt():
    print("\n=== 프롬프트 검색 ===")
    keyword = input("검색어: ").strip()

    if not keyword:
        print("검색어를 입력해 주세요.")
        return

    results = [
        prompt
        for prompt in prompts
        if keyword.lower() in prompt["title"].lower()
        or keyword.lower() in prompt["content"].lower()
    ]

    if not results:
        print("검색 결과가 없습니다.")
        return

    print("\n검색 결과:")
    for index, prompt in enumerate(results, start=1):
        star = " ⭐" if prompt["favorite"] else ""
        print(f"{index}. [{prompt['category']}] {prompt['title']}{star}")

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
        print("올바른 번호를 입력해 주세요.")

    favorite = "⭐" if prompt["favorite"] else "X"
    print("\n" + "─" * 30)
    print(f"제목: {prompt['title']}")
    print(f"카테고리: {prompt['category']}")
    print(f"즐겨찾기: {favorite}")
    print("─" * 30)
    print("내용:")
    print(prompt["content"])
    print("─" * 30)


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
        print("올바른 번호를 입력해 주세요.")

    prompt["favorite"] = not prompt["favorite"]
    if prompt["favorite"]:
        print(f"'{prompt['title']}' 프롬프트를 즐겨찾기에 추가했습니다!")
    else:
        print(f"'{prompt['title']}' 프롬프트를 즐겨찾기에서 해제했습니다!")


def show_favorites():
    print("\n=== 즐겨찾기 목록 ===")

    favorites = [prompt for prompt in prompts if prompt["favorite"]]
    if not favorites:
        print("즐겨찾기한 프롬프트가 없습니다.")
        return

    for index, prompt in enumerate(favorites, start=1):
        print(f"{index}. [{prompt['category']}] {prompt['title']} ⭐")

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


def main():
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
            print("올바른 메뉴 번호를 입력해 주세요.")


if __name__ == "__main__":
    main()
