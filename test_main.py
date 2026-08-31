import io
import runpy
import unittest
from unittest.mock import patch

import main


DEFAULT_CATEGORIES = list(main.categories)
DEFAULT_PROMPTS = [prompt.copy() for prompt in main.prompts]


class PromptManagerTests(unittest.TestCase):
    def setUp(self):
        main.categories[:] = DEFAULT_CATEGORIES
        main.prompts[:] = [prompt.copy() for prompt in DEFAULT_PROMPTS]

    def tearDown(self):
        main.categories[:] = DEFAULT_CATEGORIES
        main.prompts[:] = [prompt.copy() for prompt in DEFAULT_PROMPTS]

    def call_with_inputs(self, function, inputs):
        with patch("builtins.input", side_effect=inputs):
            with patch("sys.stdout", new_callable=io.StringIO) as output:
                result = function()
        return result, output.getvalue()

    def capture_output(self, function, *args):
        with patch("sys.stdout", new_callable=io.StringIO) as output:
            result = function(*args)
        return result, output.getvalue()

    # 기본 데이터
    def test_01_default_prompts_keep_original_three_and_total_seven(self):
        original_titles = {
            "아침 이슈 브리핑",
            "AI 기술 뉴스 3줄 요약",
            "개인 지출 자동 분류",
        }
        self.assertEqual(len(main.prompts), 7)
        self.assertTrue(original_titles.issubset({p["title"] for p in main.prompts}))

    def test_02_every_prompt_has_required_fields(self):
        required_fields = {"title", "content", "category", "favorite"}
        for prompt in main.prompts:
            self.assertEqual(set(prompt), required_fields)

    def test_03_all_six_categories_have_data(self):
        prompt_categories = {prompt["category"] for prompt in main.prompts}
        self.assertEqual(prompt_categories, set(DEFAULT_CATEGORIES))

    def test_04_initial_favorite_exists(self):
        self.assertTrue(any(prompt["favorite"] for prompt in main.prompts))

    # 프롬프트 추가와 입력 검증
    def test_05_new_prompt_favorite_defaults_to_false(self):
        self.call_with_inputs(main.add_prompt, ["새 제목", "새 내용", "1"])
        self.assertFalse(main.prompts[-1]["favorite"])

    def test_06_empty_title_is_requested_again(self):
        _, output = self.call_with_inputs(
            main.add_prompt, ["", "정상 제목", "정상 내용", "1"]
        )
        self.assertIn("제목은 비워둘 수 없습니다.", output)
        self.assertEqual(main.prompts[-1]["title"], "정상 제목")

    def test_07_empty_content_is_requested_again(self):
        _, output = self.call_with_inputs(
            main.add_prompt, ["정상 제목", "", "정상 내용", "1"]
        )
        self.assertIn("내용은 비워둘 수 없습니다.", output)
        self.assertEqual(main.prompts[-1]["content"], "정상 내용")

    def test_08_existing_category_number_is_used(self):
        self.call_with_inputs(main.add_prompt, ["새 제목", "새 내용", "2"])
        self.assertEqual(main.prompts[-1]["category"], "이미지 생성")

    def test_09_custom_category_is_added_and_used(self):
        self.call_with_inputs(main.add_prompt, ["새 제목", "새 내용", "학습"])
        self.assertEqual(main.prompts[-1]["category"], "학습")
        self.assertIn("학습", main.categories)

    # 목록과 카테고리 조회
    def test_10_show_list_outputs_entries_and_total(self):
        _, output = self.capture_output(main.show_list)
        self.assertIn("1. [자동화] 아침 이슈 브리핑", output)
        self.assertIn("총 7개의 프롬프트", output)

    def test_11_show_list_handles_empty_prompts(self):
        main.prompts.clear()
        result, output = self.capture_output(main.show_list)
        self.assertEqual(result, [])
        self.assertIn("저장된 프롬프트가 없습니다.", output)

    def test_12_category_query_outputs_only_matches(self):
        results, output = self.capture_output(main.show_by_category, "자동화")
        self.assertTrue(results)
        self.assertTrue(all(prompt["category"] == "자동화" for prompt in results))
        self.assertIn("아침 이슈 브리핑", output)
        self.assertNotIn("제품 썸네일 이미지 생성", output)

    def test_13_category_query_handles_no_result(self):
        main.prompts[:] = [
            {
                "title": "텍스트 전용",
                "content": "내용",
                "category": "텍스트 생성",
                "favorite": False,
            }
        ]
        result, output = self.capture_output(main.show_by_category, "이미지 생성")
        self.assertEqual(result, [])
        self.assertIn("카테고리의 프롬프트가 없습니다.", output)

    # 검색
    def test_14_search_finds_title(self):
        results, output = self.capture_output(
            main.search_prompt, "제품 썸네일 이미지 생성"
        )
        self.assertEqual(len(results), 1)
        self.assertIn("제품 썸네일 이미지 생성", output)

    def test_15_search_finds_content(self):
        results, output = self.capture_output(main.search_prompt, "해결 방법")
        self.assertEqual(results[0]["title"], "친절한 고객 상담가 페르소나")
        self.assertIn("친절한 고객 상담가 페르소나", output)

    def test_16_search_supports_partial_case_insensitive_match(self):
        results, _ = self.capture_output(main.search_prompt, "aI 기")
        self.assertIn("AI 기술 뉴스 3줄 요약", [prompt["title"] for prompt in results])

    def test_17_search_handles_no_result(self):
        result, output = self.capture_output(main.search_prompt, "존재하지않는검색어")
        self.assertEqual(result, [])
        self.assertIn("검색 결과가 없습니다.", output)

    def test_18_search_rejects_empty_keyword(self):
        result, output = self.capture_output(main.search_prompt, "   ")
        self.assertEqual(result, [])
        self.assertIn("검색어를 입력해 주세요.", output)

    # 상세 보기와 즐겨찾기
    def test_19_show_detail_outputs_all_fields(self):
        prompt, output = self.capture_output(main.show_detail, 1)
        self.assertIs(prompt, main.prompts[0])
        self.assertIn("제목: 아침 이슈 브리핑", output)
        self.assertIn("카테고리: 자동화", output)
        self.assertIn(main.prompts[0]["content"], output)

    def test_20_show_detail_reprompts_invalid_number(self):
        prompt, output = self.call_with_inputs(main.show_detail, ["99", "1"])
        self.assertIs(prompt, main.prompts[0])
        self.assertIn("올바른 번호를 입력해 주세요.", output)

    def test_21_toggle_favorite_adds_favorite(self):
        self.assertFalse(main.prompts[0]["favorite"])
        prompt, output = self.capture_output(main.toggle_favorite, 1)
        self.assertTrue(prompt["favorite"])
        self.assertIn("즐겨찾기에 추가했습니다!", output)

    def test_22_toggle_favorite_removes_favorite(self):
        main.prompts[0]["favorite"] = True
        prompt, output = self.capture_output(main.toggle_favorite, 1)
        self.assertFalse(prompt["favorite"])
        self.assertIn("즐겨찾기에서 해제했습니다!", output)

    def test_23_show_favorites_outputs_only_favorites(self):
        favorites, output = self.capture_output(main.show_favorites)
        self.assertTrue(favorites)
        self.assertTrue(all(prompt["favorite"] for prompt in favorites))
        self.assertIn("제품 썸네일 이미지 생성", output)
        self.assertNotIn("아침 이슈 브리핑", output)

    def test_24_show_favorites_handles_empty_favorites(self):
        for prompt in main.prompts:
            prompt["favorite"] = False
        result, output = self.capture_output(main.show_favorites)
        self.assertEqual(result, [])
        self.assertIn("즐겨찾기한 프롬프트가 없습니다.", output)

    # 메인 메뉴
    def test_25_main_rejects_alphabetic_menu(self):
        _, output = self.call_with_inputs(main.main, ["abc", "0"])
        self.assertIn("올바른 메뉴 번호를 입력해 주세요.", output)

    def test_26_main_rejects_negative_menu(self):
        _, output = self.call_with_inputs(main.main, ["-1", "0"])
        self.assertIn("올바른 메뉴 번호를 입력해 주세요.", output)

    def test_27_main_rejects_out_of_range_menu(self):
        _, output = self.call_with_inputs(main.main, ["99", "0"])
        self.assertIn("올바른 메뉴 번호를 입력해 주세요.", output)

    def test_28_main_zero_exits_normally(self):
        _, output = self.call_with_inputs(main.main, ["0"])
        self.assertIn("프로그램을 종료합니다.", output)

    def test_29_import_does_not_run_main(self):
        with patch("builtins.input", side_effect=AssertionError("input called")):
            namespace = runpy.run_path("main.py", run_name="prompt_manager_import_test")
        self.assertTrue(callable(namespace["main"]))

    # 평가용 전체 기능 데모
    def test_30_evaluation_demo_needs_no_input(self):
        with patch("builtins.input", side_effect=AssertionError("input called")):
            _, output = self.capture_output(main.run_evaluation_demo)
        for step in range(1, 7):
            self.assertIn(f"[데모 {step}/6]", output)
        self.assertIn("평가용 기능 데모가 완료되었습니다.", output)

    def test_31_evaluation_demo_uses_current_prompt_data(self):
        main.prompts[:] = [
            {
                "title": "현재 데이터 고유 제목",
                "content": "현재 데이터 고유 내용",
                "category": "기타",
                "favorite": False,
            }
        ]
        _, output = self.capture_output(main.run_evaluation_demo)
        self.assertIn("현재 데이터 고유 제목", output)
        self.assertIn("현재 데이터 고유 내용", output)

    def test_32_evaluation_demo_restores_all_data_and_favorites(self):
        prompts_before = [prompt.copy() for prompt in main.prompts]
        categories_before = list(main.categories)
        self.capture_output(main.run_evaluation_demo)
        self.assertEqual(main.prompts, prompts_before)
        self.assertEqual(main.categories, categories_before)

    def test_33_changes_persist_during_same_program_run(self):
        self.call_with_inputs(main.add_prompt, ["실행 중 추가", "유지 확인", "기타"])
        added_number = len(main.prompts)
        self.capture_output(main.toggle_favorite, added_number)
        _, output = self.capture_output(main.show_list)
        self.assertEqual(main.prompts[-1]["title"], "실행 중 추가")
        self.assertTrue(main.prompts[-1]["favorite"])
        self.assertIn("[기타] 실행 중 추가 ⭐", output)


if __name__ == "__main__":
    unittest.main()
