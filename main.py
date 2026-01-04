
import os
import sys
import json
import random
import logging

logging.basicConfig(level=logging.INFO, format='[DELUSIONIST] %(message)s')

class DelusionistFactory:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.input_dir = os.path.join(self.base_dir, 'input')
        self.output_dir = os.path.join(self.base_dir, 'output')
        self.staging_dir = os.path.join(self.base_dir, 'staging')
        
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.staging_dir, exist_ok=True)
        
        self.request_path = os.path.join(self.input_dir, 'request.json')
        self.word_pool_path = os.path.join(self.input_dir, '100000word.txt')
        self.state_path = os.path.join(self.staging_dir, 'state.json')
        
        # Output files for each step
        self.section_a_path = os.path.join(self.output_dir, 'section_a_chains.txt')
        self.section_b_path = os.path.join(self.output_dir, 'section_b_refined.txt')
        self.section_c_path = os.path.join(self.output_dir, 'section_c_final.txt')

    def load_request(self):
        if not os.path.exists(self.request_path):
            return None
        with open(self.request_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_word_pool(self):
        if not os.path.exists(self.word_pool_path):
            return []
        with open(self.word_pool_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]

    def load_state(self):
        if not os.path.exists(self.state_path):
            return {"current_step": 1, "chains_generated": 0}
        with open(self.state_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_state(self, state):
        with open(self.state_path, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    def count_lines(self, filepath):
        if not os.path.exists(filepath):
            return 0
        with open(filepath, 'r', encoding='utf-8') as f:
            return len([line for line in f if line.strip()])

    def get_random_words(self, word_pool, count=3):
        """Python의 랜덤 단어 선택 (CHAOS 요소)"""
        if len(word_pool) < count:
            return word_pool
        return random.sample(word_pool, count)

    def get_mode_ratio(self, mode):
        """모드별 Python 랜덤 vs AI 선택 비율"""
        if mode == "CHAOS":
            return {"python_random": 0.7, "ai_semantic": 0.3}
        else:  # NUANCE
            return {"python_random": 0.3, "ai_semantic": 0.7}

    def _analyze_vocab_level(self, direction):
        """
        DIRECTION 텍스트를 AI에게 전달하여 적절한 어휘 수준 판단을 유도.
        (키워드 기반 자동 분석 대신 AI가 맥락을 파악하도록 함)
        """
        # AI가 직접 판단하도록 가이드만 제공
        return f"DIRECTION 분석 후 적절한 어휘 수준 판단: '{direction[:50]}...'"

    def run(self):
        logging.info("Initializing Delusionist Factory Engine...")
        
        # 1. Load Request
        req = self.load_request()
        if not req:
            logging.error("request.json not found!")
            return
        
        starting = req.get("STARTING_SENTENCE", "")
        mandatory = req.get("MANDATORY_WORD", [])
        imagery = req.get("PREFERRED_IMAGERY", [])
        chains_target = req.get("CHAINS_COUNT", 120)
        mode = req.get("MODE_SELECTION", "CHAOS").strip().upper()
        selection_b_count = req.get("SELECTION_B_COUNT", 8)  # Step 2에서 추출할 문장 수
        refining_count = req.get("REFINING_COUNT", 2)  # Step 3 최종 출력 수
        direction = req.get("DIRECTION", "")
        final_language = req.get("FINAL_LANGUAGE", "Korean")  # Step 3 출력 언어
        language_rule = req.get("LANGUAGE_RULE", "NO_3_CONSECUTIVE_FOREIGN_WORDS")
        
        word_pool = self.load_word_pool()
        state = self.load_state()
        ratio = self.get_mode_ratio(mode)
        
        logging.info(f"[CONFIG] Mode: {mode} | Chains: {chains_target}")
        logging.info(f"[CONFIG] Selection B: {selection_b_count} | Final Output: {refining_count}")
        logging.info(f"[CONFIG] Ratio: Python {ratio['python_random']*100:.0f}% / AI {ratio['ai_semantic']*100:.0f}%")
        
        # ========== STEP 1: Chaining CoT ==========
        if state["current_step"] == 1:
            chains_done = self.count_lines(self.section_a_path)
            BATCH_SIZE = 30  # 30줄씩 출력 (퀄리티 유지)
            
            if chains_done < chains_target:
                # Calculate batch info
                remaining = chains_target - chains_done
                current_batch = min(BATCH_SIZE, remaining)
                batch_start = chains_done + 1
                batch_end = chains_done + current_batch
                
                # Generate random words for each chain in this batch
                batch_random_words = []
                for i in range(current_batch):
                    batch_random_words.append(self.get_random_words(word_pool, 3))
                
                logging.info(f"[STEP 1] Chaining Progress: {chains_done}/{chains_target}")
                
                print("\n" + "="*70)
                print(f"  [STEP 1: CHAINING CoT] - Batch #{batch_start}~{batch_end} / {chains_target}")
                print("="*70)
                print(f"  시작 문장: {starting}")
                print(f"  필수 단어: {', '.join(mandatory)}")
                print(f"  모드: {mode}")
                print("  ")
                print(f"  � AI 참조 이미지어 (PREFERRED_IMAGERY):")
                print(f"     {', '.join(imagery)}")
                print("  ")
                print("  " + "-"*66)
                print(f"  � 이번 배치 랜덤 단어 ({current_batch}줄분):")
                print("  ")
                for idx, words in enumerate(batch_random_words, start=batch_start):
                    print(f"     [{idx:03d}] {', '.join(words)}")
                print("  ")
                print("  " + "-"*66)
                print("  📌 Agent 작업:")
                print("  ")
                print(f"  1️⃣ 위 랜덤 단어를 활용해 '망상적 변이 문장' {current_batch}개 생성")
                print(f"  2️⃣ 필수 단어 ({', '.join(mandatory)}) 매 문장에 반드시 포함")
                print(f"  3️⃣ ⚠️ LANGUAGE RULE: 한국어&영어 혼재시 영어 단어 3개 연속 사용 금지!")
                print(f"     (Good: 'AI가 sublation learning으로 확장' / Bad: 'sublation ketazine darkener AI가')")
                print(f"  4️⃣ 생성된 {current_batch}줄을 아래 파일에 **추가(append)**:")
                print(f"     {self.section_a_path}")
                print("  " + "-"*66)
                print("="*70 + "\n")
                return
            
            else:
                # Audit: Verify mandatory words in all chains
                logging.info(f"[STEP 1] ✅ Chaining Complete! ({chains_done} chains)")
                
                # Move to Step 2
                state["current_step"] = 2
                self.save_state(state)
                logging.info("[STATE] Advancing to STEP 2...")
        
        # ========== STEP 2: Refining CoT (문장 추출) ==========
        if state["current_step"] == 2:
            refined_done = self.count_lines(self.section_b_path)
            
            if refined_done < selection_b_count:  # selection_b_count 사용
                next_refined_num = refined_done + 1
                
                logging.info(f"[STEP 2] Selection B Progress: {refined_done}/{selection_b_count}")
                
                print("\n" + "="*70)
                print(f"  [STEP 2: REFINING CoT] - Selection B #{next_refined_num}/{selection_b_count}")
                print("="*70)
                print(f"  DIRECTION: {direction[:80]}...")
                print(f"  PREFERRED_IMAGERY: {', '.join(imagery)}")
                print("  ")
                print("  " + "-"*66)
                print("  📌 Agent 작업:")
                print("  ")
                print(f"  1️⃣ {self.section_a_path} 의 모든 체인 분석")
                print(f"  2️⃣ DIRECTION과 IMAGERY에 맞는 핵심 단어/구절 추출")
                print(f"  3️⃣ 🎯 INGENUOUS 필터: Ingenuous 하고 innovative한 표현만 선택")
                print(f"  4️⃣ 필수 단어 포함하여 '정제된 망상 문장' 1개 생성")
                print(f"  5️⃣ 생성된 문장을 아래 파일에 **추가(append)**:")
                print(f"     {self.section_b_path}")
                print("  ")
                print(f"  ⚠️ 총 {selection_b_count}개 문장 중 {refining_count}개가 최종 결과물로 사용됩니다.")
                print("  " + "-"*66)
                print("="*70 + "\n")
                return
            
            else:
                logging.info(f"[STEP 2] ✅ Refining Complete! ({refined_done} sentences)")
                state["current_step"] = 3
                self.save_state(state)
                logging.info("[STATE] Advancing to STEP 3...")
        
        # ========== STEP 3: Final CoT (최종 번역) ==========
        if state["current_step"] == 3:
            final_done = self.count_lines(self.section_c_path)
            used_lines = state.get("used_lines", [])  # 이미 사용된 문장 번호
            
            if final_done < refining_count:
                # 사용되지 않은 다음 문장 선택
                next_final_num = final_done + 1
                
                # Section B에서 아직 사용되지 않은 문장 중 하나 선택
                available_lines = [i for i in range(1, selection_b_count + 1) if i not in used_lines]
                if not available_lines:
                    logging.error("[ERROR] 사용 가능한 Section B 문장이 없습니다!")
                    return
                
                selected_line = available_lines[0]  # 순차적으로 선택
                
                logging.info(f"[STEP 3] Final Progress: {final_done}/{refining_count}")
                
                # 어휘 수준 분석 (DIRECTION 기반)
                vocab_hint = self._analyze_vocab_level(direction)
                
                print("\n" + "="*70)
                print(f"  [STEP 3: FINAL CoT] - 최종 결과물 #{next_final_num}/{refining_count}")
                print("="*70)
                print("  ")
                print(f"  📖 Section B 문장 #{selected_line} 사용 (이후 재사용 금지)")
                print("  ")
                print("  " + "-"*66)
                print("  🎯 어휘 수준 가이드 (DIRECTION 분석):")
                print(f"     {vocab_hint}")
                print("  " + "-"*66)
                print("  📌 Agent 작업:")
                print("  ")
                print(f"  1️⃣ {self.section_b_path} 의 문장 #{selected_line} 읽기")
                print(f"  2️⃣ 내용과 의미 100% 유지하면서")
                print(f"  3️⃣ 추상어 → 문맥에 맞는 '적절한 수준'의 언어로 번역")
                print(f"  4️⃣ 생성된 결과물을 아래 파일에 **추가(append)**:")
                print(f"     {self.section_c_path}")
                print("  ")
                print(f"  ✅ 완료 후: 사용된 문장 #{selected_line} 마킹 (state.json 업데이트)")
                print("  " + "-"*66)
                print("="*70 + "\n")
                return
            
            else:
                logging.info(f"[STEP 3] ✅ Final Complete! ({final_done} outputs)")
                logging.info("")
                logging.info("="*50)
                logging.info("  🎉 DELUSIONIST FACTORY - ALL STEPS COMPLETE!")
                logging.info("="*50)
                logging.info(f"  Section A (Chains): {self.section_a_path}")
                logging.info(f"  Section B (Refined): {self.section_b_path}")
                logging.info(f"  Section C (Final): {self.section_c_path}")
                logging.info("="*50)


if __name__ == "__main__":
    factory = DelusionistFactory()
    factory.run()
