categories = [
    "텍스트 생성",
    "이미지 생성",
    "영상 생성",
    "페르소나",
    "자동화",
    "기타"
]

prompts = []
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
        choice = input("선택: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            category = categories[int(choice) - 1]
            break

        print("올바른 번호를 입력해주세요.")

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
        print("아직 구현되지 않은 기능입니다.")