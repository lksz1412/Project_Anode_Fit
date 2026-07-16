# P4 경쟁 저작 브리프 — Ch1 §15.1 「왜 흑연에는 없고 LCO 에는 있는가」 보강 + MIT 배경 bgbox (N=4 독립 초안)

## 역할·경계 (하드)
- 독립 초안 작성 sub-agent. 무통신. **지정 산출 파일 1개만 write.** 허위 문헌·수치 창작 절대 금지.

## 목표
`/home/user/Project_Anode_Fit/Claude/docs/v1.0.20/_sections/ch1_sec15_lcoelec.tex` 의 **소절 §15.1 전체**(L12 `\subsection{왜 흑연에는 없고 LCO 에는 있는가 --- MIT 의 물리}\label{sec:lco-why}` 부터 L20 끝 — L22 `\subsection{Fermi--Dirac 에서...` 직전)를 다음 구조의 **대체 블록**으로 재작성:

1. **[본문]** 기존 내용(config/vib/electronic 세 자유도·흑연은 g(E_F) 변화 미미·LCO 는 x=1 절연체→탈리튬화로 금속·게이트 국소화) **전량 보존**하되, 다음 두 가지를 정밀화:
   - x=1 LiCoO₂ 가 절연체인 이유를 **밴드 그림**으로 정확히: Co³⁺ t₂g⁶ low-spin 닫힌 껍질 = **가득 찬 띠**(밴드 절연체) — "전기 절연체"라는 현 서술을 물리 부류까지 명시.
   - 탈리튬화 MIT 가 **단순 밴드 채움 논리로는 설명되지 않음**(정공이 생기면 곧바로 금속이어야 하나 실측은 x≈0.94–0.75 의 1차 전이·2상 공존)을 1–2문장으로 제기 → 그 해소는 bgbox 로 전달.
2. **[배경 bgbox]** `\begin{bgbox}\textbf{금속--절연체 전이와 Mott 물리 ---}` 로 시작하는 자족 블록(8–12문장):
   - 절연체의 두 부류: **밴드 절연체**(단일입자 띠 그림 — 띠가 가득 참) vs **Mott 절연체**(띠 그림으로는 금속이어야 하나 전자간 Coulomb 반발 U 가 이동적분 t 를 눌러 전자가 자리에 국재 — 상관 효과)\cite{mott1968,imada1998}. 금속--절연체 전이(MIT)는 채움(도핑)·띠폭(압력)·상관의 경쟁으로 일어난다\cite{imada1998}.
   - LiCoO₂ 적용: x=1 은 t₂g⁶ **밴드 절연체**(Mott 절연체가 아님 — 오독 금지)\cite{menetrier1999}. 탈리튬화 정공은 밴드 그림이면 즉시 금속화를 예상시키나, 실측 MIT 는 x≈0.94–0.75 2상역의 **1차 전이**다\cite{menetrier1999,reimers1992,motohashi2009}.
   - 해소(최첨단 다리): Marianetti–Kotliar–Ceder 는 정공이 Li 빈자리에 속박된 **불순물 준위**를 만들고 그 불순물 띠가 임계 농도에서 비국재화하는 **불순물 Mott 전이**로 이 1차 MIT 를 설명했다\cite{marianetti2004} — "상관 물리가 host 띠가 아니라 불순물 준위에서 일한다".
   - 본 문건 다리: 이 미시 기작 전체를 forward 모델은 조성축 게이트 g(E_F,x) 하나로 현상학화한다 — 게이트 중심 x_MIT=전이 조성(실측 2상역 중앙), 폭 Δx_MIT=발현 조성의 결함 분산(§15.4 의 정당화와 접속). 미시 기작과 현상학 게이트의 관계(전자는 왜, 후자는 어떻게)를 1문장으로.
   - **자족 요건**: bgbox 만 떼어 다른 곳(부록)에 옮겨도 성립(본문 지시대명사 금지). 본문은 bgbox 없이도 읽히게.
3. **[마무리 다리]** 소절 끝 1문장: 다음 소절(§15.2 유도)로 전달(기존 "게이트는 MIT 의 직접 결과다" 취지 보존).

## 검증된 인용 (이 6키만 사용 — bib 등재는 master 가 처리하므로 키 실재 걱정 불요)
- mott1968: N. F. Mott, "Metal-Insulator Transition," Rev. Mod. Phys. 40, 677–683 (1968).
- imada1998: M. Imada, A. Fujimori, Y. Tokura, "Metal-insulator transitions," Rev. Mod. Phys. 70, 1039–1263 (1998).
- marianetti2004: C. A. Marianetti, G. Kotliar, G. Ceder, "A first-order Mott transition in LixCoO2," Nature Materials 3, 627–631 (2004). [DFT 대형 초격자 계산 — 불순물 Mott 기작; x<0.75 금속·x>0.95 절연]
- menetrier1999·reimers1992·motohashi2009: 기존 bib 그대로.

## 물리 정확성 하드 가드 (위반 = 실격)
- LiCoO₂(x=1)를 "Mott 절연체"로 서술 금지(밴드 절연체가 맞다 — Marianetti 의 Mott 물리는 **불순물 준위** 소관).
- Marianetti 결과의 과대 해석 금지(그들의 주장 = 불순물 준위의 Mott 전이가 1차 MIT·2상 공존을 설명; "확정된 유일 기작"처럼 쓰지 말고 "설명했다/제시했다" 수준).
- 기존 §15.1 의 물리 문장·인용(menetrier1999·motohashi2009) 유실 금지.
- 수식·라벨 신설 없음(산문+bgbox 만).

## 문체
`results/V1020_STYLE_RUBRIC.md` 전문 정독 후 준수(A1 완결 문장·A2 D1/D2·C1 병기 형식·D3′ 다리 양식). 분량: 본문 소절 10–16행 + bgbox 12–20행 내외.

## 필독(전문)
1. `_sections/ch1_sec15_lcoelec.tex` 전문(특히 §15.1 과 §15.4 게이트 정당화 — bgbox 가 §15.4 와 중복되지 않게 역할 분담: bgbox=왜(기작), §15.4=게이트 형태의 정당화) 2. `_sections/ch1_sec13_lcohys.tex` L130–149(T1 슬롯 분리 — 모순 금지) 3. rubric 전문.
(경로는 `/home/user/Project_Anode_Fit/Claude/docs/v1.0.20/` 기준.)

## 산출 형식
지정 파일에:
```
% ==== P4 draft <ID> — §15.1 대체 블록 ====
\subsection{왜 흑연에는 없고 LCO 에는 있는가 --- MIT 의 물리}\label{sec:lco-why}
... (재작성 본문 + bgbox) ...
% ==== 블록 끝 ====
% NOTE: Read Coverage / 보존 확인(기존 문장·인용 유지 목록) / 자체검수(물리 가드 3항 점검 결과)
```
