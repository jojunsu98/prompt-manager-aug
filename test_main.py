import copy
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

    def assert_category_query(self, category):
        results, output = self.capture_output(main.show_by_category, category)
        self.assertTrue(results)
        self.assertTrue(all(prompt["category"] == category for prompt in results))
        self.assertIn(category, output)

    # 기본 데이터와 자료구조
    def test_01_original_three_prompts_are_preserved(self):
        expected = {
            "아침 이슈 브리핑": "자동화",
            "AI 기술 뉴스 3줄 요약": "텍스트 생성",
            "개인 지출 자동 분류": "자동화",
        }
        actual = {prompt["title"]: prompt["category"] for prompt in main.prompts}
        self.assertGreaterEqual(len(main.prompts), 3)
        for title, category in expected.items():
            self.assertEqual(actual.get(title), category)

    def test_02_default_prompts_are_at_least_seven(self):
        self.assertGreaterEqual(len(main.prompts), 7)

    def test_03_every_prompt_is_dictionary(self):
        self.assertTrue(all(isinstance(prompt, dict) for prompt in main.prompts))

    def test_04_every_prompt_has_title_field(self):
        self.assertTrue(
            all(
                isinstance(prompt.get("title"), str) and prompt["title"].strip()
                for prompt in main.prompts
            )
        )

    def test_05_every_prompt_has_content_field(self):
        self.assertTrue(
            all(
                isinstance(prompt.get("content"), str) and prompt["content"].strip()
                for prompt in main.prompts
            )
        )

    def test_06_every_prompt_has_category_field(self):
        self.assertTrue(
            all(
                isinstance(prompt.get("category"), str)
                and prompt["category"].strip()
                for prompt in main.prompts
            )
        )

    def test_07_every_prompt_has_favorite_field(self):
        self.assertTrue(
            all(isinstance(prompt.get("favorite"), bool) for prompt in main.prompts)
        )

    def test_08_six_default_categories_exist_in_required_order(self):
        self.assertEqual(
            main.categories[:6],
            ["텍스트 생성", "이미지 생성", "영상 생성", "페르소나", "자동화", "기타"],
        )

    def test_09_every_default_category_has_real_prompt(self):
        prompt_categories = {prompt["category"] for prompt in main.prompts}
        for category in DEFAULT_CATEGORIES:
            self.assertIn(category, prompt_categories)

    def test_10_initial_favorite_exists(self):
        favorites = [prompt for prompt in main.prompts if prompt["favorite"]]
        self.assertTrue(favorites)
        self.assertEqual(favorites[0]["title"], "아침 이슈 브리핑")

    # 프롬프트 추가와 입력 검증
    def test_11_new_prompt_favorite_defaults_to_false(self):
        self.call_with_inputs(main.add_prompt, ["새 제목", "새 내용", "1"])
        self.assertFalse(main.prompts[-1]["favorite"])

    def test_12_empty_title_is_requested_again(self):
        _, output = self.call_with_inputs(
            main.add_prompt, ["", "정상 제목", "정상 내용", "1"]
        )
        self.assertIn("제목은 비워둘 수 없습니다.", output)
        self.assertEqual(main.prompts[-1]["title"], "정상 제목")

    def test_13_empty_content_is_requested_again(self):
        _, output = self.call_with_inputs(
            main.add_prompt, ["정상 제목", "", "정상 내용", "1"]
        )
        self.assertIn("내용은 비워둘 수 없습니다.", output)
        self.assertEqual(main.prompts[-1]["content"], "정상 내용")

    def test_14_existing_category_number_is_used(self):
        self.call_with_inputs(main.add_prompt, ["새 제목", "새 내용", "2"])
        self.assertEqual(main.prompts[-1]["category"], "이미지 생성")

    def test_15_custom_category_is_used_by_new_prompt(self):
        self.call_with_inputs(main.add_prompt, ["새 제목", "새 내용", "코딩 실습"])
        self.assertEqual(main.prompts[-1]["category"], "코딩 실습")

    def test_16_custom_category_is_added_to_categories(self):
        self.call_with_inputs(main.add_prompt, ["새 제목", "새 내용", "코딩 실습"])
        self.assertIn("코딩 실습", main.categories)

    # 목록과 카테고리 조회
    def test_17_show_list_outputs_number_category_title_favorite_and_total(self):
        _, output = self.capture_output(main.show_list)
        self.assertIn("1. [자동화] 아침 이슈 브리핑 [즐겨찾기]", output)
        self.assertIn("2. [텍스트 생성] AI 기술 뉴스 3줄 요약 [일반]", output)
        self.assertIn(f"총 {len(main.prompts)}개의 프롬프트", output)
        output.encode("cp949")

    def test_18_show_list_handles_empty_prompts(self):
        main.prompts.clear()
        result, output = self.capture_output(main.show_list)
        self.assertEqual(result, [])
        self.assertIn("저장된 프롬프트가 없습니다.", output)

    def test_19_category_query_filters_only_matches(self):
        results, output = self.capture_output(main.show_by_category, "자동화")
        self.assertTrue(results)
        self.assertTrue(all(prompt["category"] == "자동화" for prompt in results))
        self.assertIn("아침 이슈 브리핑", output)
        self.assertNotIn("제품 썸네일 이미지 생성", output)

    def test_20_category_query_handles_no_result(self):
        main.categories.append("빈 카테고리")
        result, output = self.capture_output(main.show_by_category, "빈 카테고리")
        self.assertEqual(result, [])
        self.assertIn("카테고리의 프롬프트가 없습니다.", output)

    def test_21_text_category_query_has_result(self):
        self.assert_category_query("텍스트 생성")

    def test_22_image_category_query_has_result(self):
        self.assert_category_query("이미지 생성")

    def test_23_video_category_query_has_result(self):
        self.assert_category_query("영상 생성")

    def test_24_persona_category_query_has_result(self):
        self.assert_category_query("페르소나")

    def test_25_automation_category_query_has_result(self):
        self.assert_category_query("자동화")

    def test_26_other_category_query_has_result(self):
        self.assert_category_query("기타")

    # 검색
    def test_27_search_finds_title(self):
        results, output = self.capture_output(main.search_prompt, "제품 썸네일")
        self.assertEqual(results[0]["title"], "제품 썸네일 이미지 생성")
        self.assertIn("제품 썸네일 이미지 생성", output)

    def test_28_search_finds_content(self):
        results, output = self.capture_output(main.search_prompt, "해결 방법")
        self.assertEqual(results[0]["title"], "친절한 고객 상담가 페르소나")
        self.assertIn("친절한 고객 상담가 페르소나", output)

    def test_29_search_supports_partial_match(self):
        results, _ = self.capture_output(main.search_prompt, "썸네일")
        self.assertIn("제품 썸네일 이미지 생성", [prompt["title"] for prompt in results])

    def test_30_search_is_case_insensitive_for_english(self):
        results, _ = self.capture_output(main.search_prompt, "ai 기술")
        self.assertIn("AI 기술 뉴스 3줄 요약", [prompt["title"] for prompt in results])

    def test_31_search_handles_no_result(self):
        result, output = self.capture_output(main.search_prompt, "존재하지않는검색어")
        self.assertEqual(result, [])
        self.assertIn("검색 결과가 없습니다.", output)

    def test_32_search_rejects_empty_keyword(self):
        result, output = self.capture_output(main.search_prompt, "   ")
        self.assertEqual(result, [])
        self.assertIn("검색어를 입력해 주세요.", output)

    # 상세 보기와 즐겨찾기
    def test_33_show_detail_outputs_all_fields(self):
        prompt, output = self.capture_output(main.show_detail, 1)
        self.assertIs(prompt, main.prompts[0])
        self.assertIn("제목: 아침 이슈 브리핑", output)
        self.assertIn("카테고리: 자동화", output)
        self.assertIn("즐겨찾기: O", output)
        self.assertIn(main.prompts[0]["content"], output)

    def test_34_show_detail_reprompts_all_invalid_number_types(self):
        prompt, output = self.call_with_inputs(
            main.show_detail, ["문자", "0", "-1", "99", "1"]
        )
        self.assertIs(prompt, main.prompts[0])
        self.assertEqual(output.count("올바른 번호를 입력해 주세요."), 4)

    def test_35_toggle_favorite_adds_favorite(self):
        self.assertFalse(main.prompts[1]["favorite"])
        prompt, output = self.capture_output(main.toggle_favorite, 2)
        self.assertTrue(prompt["favorite"])
        self.assertIn("즐겨찾기에 추가했습니다!", output)

    def test_36_toggle_favorite_removes_favorite(self):
        self.assertTrue(main.prompts[0]["favorite"])
        prompt, output = self.capture_output(main.toggle_favorite, 1)
        self.assertFalse(prompt["favorite"])
        self.assertIn("즐겨찾기에서 해제했습니다!", output)

    def test_37_show_favorites_outputs_only_favorites(self):
        favorites, output = self.capture_output(main.show_favorites)
        self.assertTrue(favorites)
        self.assertTrue(all(prompt["favorite"] for prompt in favorites))
        self.assertIn("아침 이슈 브리핑 [즐겨찾기]", output)
        self.assertNotIn("제품 썸네일 이미지 생성", output)

    def test_38_show_favorites_handles_empty_favorites(self):
        for prompt in main.prompts:
            prompt["favorite"] = False
        result, output = self.capture_output(main.show_favorites)
        self.assertEqual(result, [])
        self.assertIn("즐겨찾기한 프롬프트가 없습니다.", output)

    def test_39_favorite_change_is_reflected_immediately(self):
        self.capture_output(main.toggle_favorite, 2)
        favorites, output = self.capture_output(main.show_favorites)
        self.assertIn(main.prompts[1], favorites)
        self.assertIn("AI 기술 뉴스 3줄 요약", output)
        self.capture_output(main.toggle_favorite, 2)
        favorites, output = self.capture_output(main.show_favorites)
        self.assertNotIn(main.prompts[1], favorites)
        self.assertNotIn("AI 기술 뉴스 3줄 요약", output)

    # 메인 메뉴와 종료
    def test_40_main_rejects_alphabetic_menu(self):
        _, output = self.call_with_inputs(main.main, ["abc", "0"])
        self.assertIn("올바른 메뉴 번호를 입력해 주세요.", output)

    def test_41_main_rejects_negative_menu(self):
        _, output = self.call_with_inputs(main.main, ["-1", "0"])
        self.assertIn("올바른 메뉴 번호를 입력해 주세요.", output)

    def test_42_main_rejects_out_of_range_menu(self):
        _, output = self.call_with_inputs(main.main, ["99", "0"])
        self.assertIn("올바른 메뉴 번호를 입력해 주세요.", output)

    def test_43_main_zero_exits_and_menu_has_required_title(self):
        _, output = self.call_with_inputs(main.main, ["0"])
        self.assertIn("코디세이 AI 학습 프롬프트 관리함", output)
        self.assertIn("0. 종료", output)
        self.assertNotIn("9. 종료", output)
        self.assertIn("프로그램을 종료합니다.", output)

    def test_44_import_does_not_run_main(self):
        with patch("builtins.input", side_effect=AssertionError("input called")):
            namespace = runpy.run_path("main.py", run_name="prompt_manager_import_test")
        self.assertTrue(callable(namespace["main"]))

    # 평가용 전체 기능 데모
    def test_45_evaluation_demo_needs_no_input(self):
        with patch("builtins.input", side_effect=AssertionError("input called")):
            _, output = self.capture_output(main.run_evaluation_demo)
        self.assertIn("평가용 기능 데모가 완료되었습니다.", output)

    def test_46_evaluation_demo_has_six_steps_in_order(self):
        _, output = self.capture_output(main.run_evaluation_demo)
        expected = [
            "[데모 1/6] 전체 프롬프트 목록",
            "[데모 2/6] 카테고리별 조회",
            "[데모 3/6] 프롬프트 검색",
            "[데모 4/6] 프롬프트 상세 보기",
            "[데모 5/6] 즐겨찾기 변경",
            "[데모 6/6] 즐겨찾기 목록",
        ]
        positions = [output.index(step) for step in expected]
        self.assertEqual(positions, sorted(positions))

    def test_47_evaluation_demo_uses_current_data_and_real_functions(self):
        main.prompts[:] = [
            {
                "title": "현재 데이터 고유 제목",
                "content": "현재 데이터 고유 내용",
                "category": "기타",
                "favorite": False,
            }
        ]
        with (
            patch.object(main, "show_list", wraps=main.show_list) as show_list,
            patch.object(
                main, "show_by_category", wraps=main.show_by_category
            ) as show_by_category,
            patch.object(
                main, "search_prompt", wraps=main.search_prompt
            ) as search_prompt,
            patch.object(main, "show_detail", wraps=main.show_detail) as show_detail,
            patch.object(
                main, "toggle_favorite", wraps=main.toggle_favorite
            ) as toggle_favorite,
            patch.object(
                main, "show_favorites", wraps=main.show_favorites
            ) as show_favorites,
        ):
            _, output = self.capture_output(main.run_evaluation_demo)
        for function_mock in (
            show_list,
            show_by_category,
            search_prompt,
            show_detail,
            toggle_favorite,
            show_favorites,
        ):
            self.assertTrue(function_mock.called)
        self.assertIn("현재 데이터 고유 제목", output)
        self.assertIn("현재 데이터 고유 내용", output)

    def test_48_evaluation_demo_restores_favorite_states(self):
        favorites_before = [prompt["favorite"] for prompt in main.prompts]
        self.capture_output(main.run_evaluation_demo)
        self.assertEqual(
            [prompt["favorite"] for prompt in main.prompts], favorites_before
        )

    def test_49_evaluation_demo_restores_all_data(self):
        prompts_before = copy.deepcopy(main.prompts)
        categories_before = list(main.categories)
        self.capture_output(main.run_evaluation_demo)
        self.assertEqual(main.prompts, prompts_before)
        self.assertEqual(main.categories, categories_before)

    def test_50_changes_persist_during_same_program_run(self):
        _, output = self.call_with_inputs(
            main.main,
            [
                "1",
                "실행 중 추가",
                "유지 확인",
                "코딩 실습",
                "6",
                str(len(DEFAULT_PROMPTS) + 1),
                "2",
                "3",
                str(len(DEFAULT_CATEGORIES) + 1),
                "0",
            ],
        )
        self.assertEqual(main.prompts[-1]["title"], "실행 중 추가")
        self.assertTrue(main.prompts[-1]["favorite"])
        self.assertIn("코딩 실습", main.categories)
        self.assertGreaterEqual(output.count("실행 중 추가"), 3)
        self.assertIn("[코딩 실습] 실행 중 추가 [즐겨찾기]", output)


if __name__ == "__main__":
    unittest.main()
