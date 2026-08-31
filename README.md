# Prompt Manager

## 현재 개선 버전 안내

이 프로그램은 자주 사용하는 AI 프롬프트를 추가하고, 목록·카테고리·검색·상세
보기·즐겨찾기로 관리하는 **Python 콘솔 기반 프롬프트 관리 프로그램**입니다.

이 프로그램은 프롬프트를 LLM API에 보내 실행하는 도구가 아닙니다. 프롬프트의
제목, 내용, 카테고리, 즐겨찾기 상태를 정리하고 찾아보는 관리 도구입니다.

### 기본 데이터

- 이전 미션에서 작성한 기존 프롬프트 3개를 포함하여 총 7개가 등록되어 있습니다.
- 텍스트 생성, 이미지 생성, 영상 생성, 페르소나, 자동화, 기타의 6개 기본
  카테고리에 각각 1개 이상의 데이터가 있습니다.
- 기본 데이터 중 1개 이상은 즐겨찾기 상태로 시작합니다.
- 새로 추가한 프롬프트의 즐겨찾기 기본값은 `False`입니다.

### 현재 메뉴

```text
1. 프롬프트 추가
2. 프롬프트 목록
3. 카테고리별 조회
4. 프롬프트 검색
5. 프롬프트 상세 보기
6. 즐겨찾기 관리
7. 즐겨찾기 목록
8. 평가용 전체 기능 데모
0. 종료
```

종료 메뉴는 `0`입니다. 메뉴 기능을 실행한 뒤에는 다시 메인 메뉴로 돌아옵니다.

### 실행 방법

프로젝트 폴더에서 다음 명령을 실행합니다.

```bash
python main.py
```

### 평가용 전체 기능 데모

메뉴에서 `8`을 입력하면 추가 입력 없이 다음 6단계를 자동으로 보여줍니다.

1. 전체 프롬프트 목록
2. 카테고리별 조회
3. 검색
4. 상세 보기
5. 즐겨찾기 변경
6. 즐겨찾기 목록

데모는 고정된 결과 문장을 출력하는 방식이 아니라 현재 `prompts` 데이터와 실제
목록·조회·검색·상세·즐겨찾기 함수를 사용합니다. 데모 중 변경한 즐겨찾기 상태는
종료 전에 원래 값으로 복원되므로 데모 전후 사용자 데이터가 같습니다.

### 테스트 방법

Python 표준 라이브러리 `unittest`와 `unittest.mock`으로 작성한 33개 테스트를
다음 명령으로 실행합니다.

```bash
python -m unittest -v
```

테스트는 기본 데이터, 입력 검증, 목록·카테고리·검색·상세 보기, 즐겨찾기,
잘못된 메뉴, 종료, import 안전성, 평가용 데모와 실행 중 데이터 유지를 확인합니다.

현재 프로젝트 파일은 다음과 같습니다.

```text
PROMPT-MANAGER-AUG/
├── main.py
├── test_main.py
├── README.md
└── .gitignore
```

### 데이터 유지 범위

데이터는 Python의 리스트와 딕셔너리에 저장되므로 **프로그램을 실행하는 동안만**
추가 내용과 즐겨찾기 변경이 유지됩니다. 프로그램을 종료하고 다시 실행하면 기본
프롬프트 7개와 기본 즐겨찾기 상태로 초기화됩니다.

### 평가 추천 시연 순서

1. `python main.py` 실행
2. `2`번에서 기본 프롬프트 7개 확인
3. `7`번에서 초기 즐겨찾기 확인
4. `4`번에서 검색 성공·실패·빈 검색어 확인
5. `6`번에서 즐겨찾기 추가·해제 후 `7`번에 즉시 반영되는지 확인
6. `1`번에서 빈 제목·내용 재입력과 새 카테고리 직접 입력 확인
7. `2`, `3`, `5`번에서 추가 데이터 유지·새 카테고리·상세 보기 확인
8. 문자, 음수, `99` 메뉴의 오류 안내 확인
9. `8`번에서 입력 없는 6단계 평가 데모 확인
10. `0`으로 종료한 뒤 다시 실행하여 기본 상태 초기화 확인

> 아래 기존 문서는 Git, clone, `feature/prompt-list` 브랜치와 merge 등 원본 과제의
> 실습 기록을 보존한 내용입니다. 현재 프로그램 사양은 위 개선 버전 안내를 우선합니다.

Python과 Git을 활용하여 만든 콘솔 기반 프롬프트 관리 프로그램입니다.

## 1. 프로젝트 소개

자주 사용하는 AI 프롬프트를 카테고리별로 관리할 수 있는 Python 프로그램입니다.

프로그램 실행 중 프롬프트를 추가하고, 목록 조회, 검색, 상세 보기, 즐겨찾기 등의 기능을 사용할 수 있습니다.

데이터는 프로그램이 실행되는 동안만 유지되며 프로그램을 종료하면 초기 상태로 돌아갑니다.

## 2. 개발 환경

- Python 3.10 이상
- Visual Studio Code
- Git
- GitHub

## 3. 실행 방법

터미널에서 프로젝트 폴더로 이동한 뒤 다음 명령어를 실행합니다.

```bash
python main.py
```

## 4. 주요 기능

1. 프롬프트 추가
2. 전체 프롬프트 목록 조회
3. 카테고리별 조회
4. 제목 또는 내용으로 프롬프트 검색
5. 프롬프트 상세 보기
6. 즐겨찾기 추가 및 해제
7. 즐겨찾기 목록 조회
8. 잘못된 메뉴 입력 처리

## 5. 카테고리

- 텍스트 생성
- 이미지 생성
- 영상 생성
- 페르소나
- 자동화
- 기타

## 6. 기본 프롬프트

이전 AI 활용 미션에서 사용한 프롬프트를 기본 데이터로 등록했습니다.

- 아침 이슈 브리핑
- AI 기술 뉴스 3줄 요약
- 개인 지출 자동 분류

## 7. Git / GitHub 실습

프로젝트 개발 과정에서 다음 Git 명령어를 사용했습니다.

- `git init`
- `git add`
- `git commit`
- `git push`
- `git pull`
- `git checkout`
- `git clone`
- `git merge`

`feature/prompt-list` 브랜치에서 프롬프트 목록 기능을 개발한 뒤 `main` 브랜치에 병합했습니다.

## 8. 프로젝트 파일

```text
PROMPT-MANAGER-AUG/
├── main.py
├── README.md
└── .gitignore
```

## 9. 데이터 저장 방식

프롬프트 데이터는 Python의 리스트와 딕셔너리를 사용하여 관리합니다.

프로그램 실행 중 새 프롬프트를 추가하거나 즐겨찾기 상태를 변경할 수 있습니다.

별도의 파일이나 데이터베이스에는 저장하지 않기 때문에 프로그램을 종료하면 실행 중 추가한 데이터와 즐겨찾기 변경 사항은 초기화됩니다.

## 10. Git 브랜치 작업

프롬프트 목록 기능은 별도의 `feature/prompt-list` 브랜치에서 개발했습니다.

기능 구현 후 `main` 브랜치로 이동하여 `git merge` 명령어로 병합했습니다.

이를 통해 기능별 브랜치 생성, 이동, 개발, 병합 과정을 실습했습니다.

## 11. 실제 개발 환경 확인

본 프로젝트는 다음 환경에서 직접 실행하고 확인하였습니다.

```text
Python 3.14.7
git version 2.55.0.windows.3
Git user.name: junsu
Git user.email: 설정 완료 (공개 저장소 개인정보 보호를 위해 README에서는 비공개)
Git default branch: main
```

Python 요구 버전인 3.10 이상을 만족하며, Visual Studio Code의 PowerShell 터미널에서 프로그램과 Git 명령어를 실행하였습니다.

---

## 12. GitHub 저장소

프로젝트 저장소:

```text
https://github.com/jojunsu98/prompt-manager-aug
```

최종 브랜치:

```text
main
```

최종 상태 확인:

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

이를 통해 로컬 저장소의 최종 변경사항이 GitHub의 `origin/main`에 반영되었음을 확인하였습니다.

---

## 13. Clone 실습

Git의 `clone` 명령을 익히기 위해 공개 샘플 저장소를 직접 복제하였습니다.

실행 명령:

```bash
git clone https://github.com/octocat/Hello-World.git
```

실행 결과:

```text
Cloning into 'Hello-World'...
remote: Enumerating objects: 13, done.
remote: Total 13 (delta 0), reused 0 (delta 0), pack-reused 13
Receiving objects: 100% (13/13), done.
```

클론 후 폴더 내부 확인:

```text
Hello-World/
└── README
```

커밋 기록 확인:

```text
7fd1a60 Merge pull request #6 from Spaceghost/patch-1
7629413 New line at end of file. --Signed off by Spaceghost
553c207 first commit
```

이를 통해 원격 저장소를 로컬 컴퓨터로 복제하고 내부 파일과 Git 기록을 확인하는 과정을 실습하였습니다.

---

## 14. 브랜치 생성과 병합 과정

프롬프트 목록 기능은 `main`에서 바로 개발하지 않고 별도의 기능 브랜치에서 구현하였습니다.

사용한 브랜치:

```text
feature/prompt-list
```

작업 흐름:

```bash
git checkout -b feature/prompt-list
git add .
git commit -m "feat: add prompt list feature"

git checkout main
git merge --no-ff feature/prompt-list -m "merge: add prompt list feature"
git push
```

병합 결과:

```text
Merge made by the 'ort' strategy.
main.py | 15 +++++++++++++++
```

최종 Git 그래프:

```text
* b3b9b57 fix: improve category and menu input handling
* 80556b2 docs: complete README
* fee81cc feat: add default prompts
* 6594a6c feat: add favorite management
* 612cb07 feat: add prompt detail feature
* ce5d0ee feat: add prompt search feature
* 23260fc feat: add category filter feature
*   367ac9a merge: add prompt list feature
|\
| * 62d345b feature/prompt-list: add prompt list feature
|/
* 01dad17 feat: add prompt creation feature
* 4b7384d feat: add prompt data structure
* c4e041e feat: add main menu
* afdfcda chore: initialize project structure
```

기능별 작업을 별도 브랜치에서 수행한 뒤 테스트 후 `main`에 병합하는 방식을 사용하였습니다.

---

## 15. 기능별 함수 구조

프로그램의 기능을 하나의 긴 코드로 작성하지 않고 함수별로 분리하였습니다.

| 함수 | 역할 |
|---|---|
| `add_prompt()` | 제목, 내용, 카테고리를 입력받아 새 프롬프트 추가 |
| `show_list()` | 저장된 전체 프롬프트 목록 출력 |
| `show_by_category()` | 선택한 카테고리에 해당하는 프롬프트만 조회 |
| `search_prompt()` | 제목 또는 내용에서 검색어 조회 |
| `show_detail()` | 선택한 프롬프트의 상세 정보 출력 |
| `toggle_favorite()` | 선택한 프롬프트의 즐겨찾기 상태 변경 |
| `show_favorites()` | 즐겨찾기된 프롬프트만 출력 |
| `show_menu()` | 메인 메뉴 출력 |

기능을 함수 단위로 분리하여 각 기능의 책임을 명확하게 하고 수정과 테스트가 쉽도록 구성하였습니다.

---

## 16. 리스트와 딕셔너리를 사용한 이유

여러 개의 프롬프트를 순서대로 관리해야 하기 때문에 전체 데이터는 Python의 `list`로 관리하였습니다.

각 프롬프트는 다음과 같이 여러 속성을 가지므로 `dict`를 사용하였습니다.

```python
{
    "title": "아침 이슈 브리핑",
    "content": "...",
    "category": "자동화",
    "favorite": False
}
```

### 리스트의 장점

- 여러 프롬프트를 순서대로 저장하기 쉽다.
- 반복문으로 전체 목록을 조회하기 쉽다.
- 새로운 데이터를 `append()`로 간단하게 추가할 수 있다.

### 리스트의 한계

- 데이터가 매우 많아지면 특정 항목 검색 속도가 느려질 수 있다.
- 프로그램을 종료하면 메모리의 데이터가 사라진다.

### 딕셔너리의 장점

- `title`, `content`, `category`, `favorite`처럼 각 값의 의미가 명확하다.
- 필요한 속성에 이름으로 접근할 수 있어 코드 가독성이 높다.

### 딕셔너리의 한계

- 필드 이름을 잘못 입력하면 오류가 발생할 수 있다.
- 데이터 구조가 복잡해지면 별도의 클래스나 데이터베이스 구조가 더 적합할 수 있다.

---

## 17. 입력값 검증

잘못된 입력 때문에 프로그램이 중단되지 않도록 기본 검증을 구현하였습니다.

### 제목

빈 문자열은 허용하지 않습니다.

```python
while not title:
    print("제목은 비워둘 수 없습니다.")
```

### 내용

내용도 빈 문자열을 허용하지 않습니다.

```python
while not content:
    print("내용은 비워둘 수 없습니다.")
```

### 메뉴

정해진 메뉴 번호 이외의 값이 입력되면 다음 안내를 출력합니다.

```text
올바른 메뉴 번호를 입력해주세요.
```

### 프롬프트 번호

존재하는 프롬프트 번호 범위 안의 숫자만 허용합니다.

이러한 검증을 통해 잘못된 입력으로 인한 프로그램 종료를 최소화하였습니다.

---

## 18. 메뉴 반복 구조

프로그램은 메인 메뉴를 계속 사용할 수 있도록 `while True` 반복문으로 구성하였습니다.

```python
while True:
    show_menu()
    choice = input("선택: ").strip()
```

사용자가 하나의 기능을 실행한 뒤 다시 메인 메뉴로 돌아갈 수 있도록 하기 위한 구조입니다.

사용자가 다음 값을 입력하면 반복문을 종료합니다.

```text
0
```

종료 시:

```text
프로그램을 종료합니다.
```

를 출력하고 `break`를 사용해 반복문을 끝냅니다.

---

## 19. 검색 구현 방식

검색어는 프롬프트의 제목과 내용 모두에서 확인합니다.

```python
if keyword.lower() in prompt["title"].lower()
or keyword.lower() in prompt["content"].lower()
```

`lower()`를 사용하여 영문 검색 시 대소문자의 영향을 줄였으며, `in` 연산자를 사용하여 전체 문장이 아니라 일부 단어만 일치해도 검색되도록 구현하였습니다.

예:

```text
검색어: 패션
검색 결과:
[이미지 생성] 패션 이미지 생성
```

---

## 20. 카테고리 처리 방식

기본 카테고리는 다음과 같습니다.

```text
텍스트 생성
이미지 생성
영상 생성
페르소나
자동화
기타
```

사용자는 번호로 기존 카테고리를 선택하거나 새로운 카테고리명을 직접 입력할 수 있습니다.

새로운 카테고리를 직접 입력하면 실행 중인 `categories` 리스트에 추가됩니다.

예:

```text
번호 선택 또는 카테고리 직접 입력: 코딩
```

결과:

```text
[코딩] 코딩 테스트
```

새 카테고리는 현재 프로그램 실행 중에만 유지되며 프로그램을 종료하면 초기 카테고리 목록으로 돌아갑니다.

---

## 21. 중복 제목 처리 정책

현재 버전에서는 동일한 제목의 프롬프트 입력을 허용합니다.

각 프롬프트는 목록 번호로 구분되므로 동일한 제목이 존재해도 별개의 데이터로 취급됩니다.

예:

```text
1. [텍스트 생성] 테스트
2. [자동화] 테스트
```

향후 기능을 확장한다면 제목 중복 여부를 검사한 뒤 사용자에게 추가 여부를 확인하거나 고유 ID를 부여하는 방식으로 개선할 수 있습니다.

---

## 22. 커밋 작성 기준

커밋은 가능한 한 하나의 기능 또는 하나의 변경 목적을 기준으로 나누었습니다.

예:

```text
feat: add main menu
feat: add prompt creation feature
feat: add prompt list feature
feat: add category filter feature
feat: add prompt search feature
feat: add prompt detail feature
feat: add favorite management
feat: add default prompts
docs: complete README
fix: improve category and menu input handling
```

`feat`, `fix`, `docs`, `chore` 등의 접두어를 사용하여 커밋의 목적을 쉽게 확인할 수 있도록 하였습니다.

---

## 23. 브랜치 분리 기준과 병합 시점

독립적으로 구현하고 검증할 수 있는 기능은 별도 브랜치로 분리할 수 있습니다.

이번 프로젝트에서는 과제에서 요구한 프롬프트 목록 기능을 다음 브랜치에서 개발하였습니다.

```text
feature/prompt-list
```

목록 기능 구현과 실행 테스트가 끝난 뒤 `main` 브랜치로 이동하여 병합하였습니다.

즉 작업 기준은 다음과 같습니다.

```text
기능 선택
→ 기능 브랜치 생성
→ 구현
→ 로컬 실행 테스트
→ 커밋
→ main checkout
→ merge
→ push
```

---

## 24. 병합 충돌 발생 시 처리 방법

이번 `feature/prompt-list` 병합에서는 실제 충돌이 발생하지 않았습니다.

향후 병합 충돌이 발생할 경우 다음 순서로 처리합니다.

1. `git status`로 충돌 파일을 확인한다.
2. 충돌 파일을 VSCode에서 연다.
3. `<<<<<<<`, `=======`, `>>>>>>>` 표시 사이의 코드를 비교한다.
4. 사용할 코드를 선택하거나 두 변경사항을 직접 통합한다.
5. 충돌 표시를 삭제하고 파일을 저장한다.
6. 프로그램을 다시 실행하여 정상 동작을 확인한다.
7. `git add`로 해결된 파일을 등록한다.
8. `git commit`으로 충돌 해결 결과를 기록한다.
9. `git status`로 작업 상태를 다시 확인한다.

충돌 해결에서는 단순히 표시를 제거하는 것이 아니라 프로그램 실행 검증까지 수행하는 것을 원칙으로 합니다.

---

## 25. 기존 프롬프트의 카테고리를 변경하는 방법

현재 프로그램에는 기존 프롬프트의 카테고리를 수정하는 별도 메뉴는 구현하지 않았습니다.

기본 프롬프트의 카테고리를 변경하려면 `main.py` 상단의 `prompts` 리스트에서 해당 프롬프트의 다음 필드를 수정합니다.

```python
"category": "자동화"
```

예를 들어:

```python
"category": "텍스트 생성"
```

으로 변경한 뒤 프로그램을 다시 실행하면 변경된 카테고리가 적용됩니다.

향후에는 `카테고리 수정` 메뉴를 추가하여 실행 중에도 기존 프롬프트의 카테고리를 변경할 수 있도록 확장할 수 있습니다.

---

## 26. 데이터 영속화에 대한 고려

현재 과제 요구사항에 따라 프로그램 실행 중에만 데이터를 유지하도록 구현하였습니다.

따라서 사용자가 새 프롬프트를 추가하거나 즐겨찾기를 변경해도 프로그램 종료 후에는 기본 데이터 상태로 초기화됩니다.

향후 데이터를 영구 저장해야 한다면 JSON 파일을 사용할 수 있습니다.

### JSON의 장점

- Python의 리스트와 딕셔너리 구조를 저장하기 쉽다.
- 사람이 내용을 읽고 수정할 수 있다.
- 별도의 데이터베이스가 필요하지 않다.

### JSON의 한계

- 데이터가 매우 많아지면 검색과 수정 효율이 낮아진다.
- 여러 사용자가 동시에 데이터를 수정하는 프로그램에는 적합하지 않다.

데이터 규모가 커질 경우 SQLite와 같은 데이터베이스 사용을 고려할 수 있습니다.
