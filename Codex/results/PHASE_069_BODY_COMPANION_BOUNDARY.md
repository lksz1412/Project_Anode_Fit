# Phase069 Step101 — 학술 본문·구현 부록·Companion 경계

## Summary / 권위

상태: CONTENT_VERIFIED_AWAITING_PUSH; PASS_P069_STEP101_BODY_COMPANION_BOUNDARY. 이 문건은 내용 배치와 후속 수정의 기준이지 기존 원고의 수정·본문 순도 PASS가 아니다.
활성 master와 Phase069 detailed plan의 Step101, Step100 요구 P069-REQ-022–030 및032를 따른다.
직전 Step100은227384f3437b0a83eb691b68b8e71d5e8daca288로 결과 포함 commit/push/live/clean이 확인됐다.
정확한8개 입력의 원천 identity와 검독 범위는 PHASE_069_STEP_101_BODY_COMPANION_RESULT.md에 기록한다.
원고 구조·파일명·실제 chapter 순서·최종 model family는 여기서 확정하지 않는다.

지정 implementation appendix OR separate companion 예외를 보존한다.
본문에서 구현 설명을 일반 section으로 허용하거나, 모든 부록을 자동으로 code-allowed 영역으로 만들지 않는다.
기존의 separate companion 계획은 유지하지만 사용자에게 허용된 지정 구현 부록 선택을 삭제하지 않는다.
실제 source tree/부록 배치와 명시적 code-allowed 경계는 Phase073/083에서 정하고 이후 검증한다.

## Surface별 내용 계약

| 영역 | 허용 내용 | 금지·제한 | 후속 책임 |
|---|---|---|---|
| 학술 본문 | 화학 반응, 정의·가정·보존·열역학·kinetics·transport·재료·관측·추론의 수식과 유도, 실제 문헌·데이터·한계 | 코드/함수/class/key/API/file/test·branch/commit/phase/step 작업사, 구현 지침 및 방어적 자기평가 | 074–081 작성,087 조립,088 검독 |
| 본문 caption·footnote·visible heading·표/그림 내부 글자 | 물리량·기호·단위·실험 조건·검증된 source 및 수식 해석 | 본문에서 뺀 구현 설명이나 code identifier를 이곳으로 우회 | 087–089 |
| 순수 유도 부록 | 긴 중간식, 단위/부호/극한/보존 검산, 근거 있는 수학적·화학적 유도 | 프로그램 listing/pseudocode·API·실행 지침; 부록이라는 이유만으로 구현 허용 안 됨 | 073,082,087 |
| 명시적으로 지정한 구현 부록 | 채택식→가정·unit/domain/limit→implementation contract, 필요한 코드/구현 설명 | 근거 없는 새 물리·code-only knob/default·미검증식의 채택; 예외의 본문 확산 | 073,083,087,088 |
| 별도 Implementation Companion | 같은 이론–구현 연결, interface/state/shape/오류 계약, 수치 오차·재현·시험의 기술적 설명 | code가 이론 선택을 역으로 지배하는 설명, empirical/internal test를 physical validity로 승격 | 083–088 |
| evidence registry·작업 결과·handover | source/blob/원문 anchor/수용 조건/검수·실행 증거, 계획·Step·commit/push 및 변경 계보 | 작업 기록을 학술 본문의 주제나 과학 증거로 대신 사용 | Codex/results 및 plans |

실제 구현 파일과 실행 도구는 source package/Codex-owned 구현 tree에 있으며, 본문에 붙여 넣지 않는다.
일반 문건·코드·LaTeX의 단순 변경 이력을 인라인 주석으로 적지 않는다.
명시 구현 예외에도 작업사 나열을 넣기 위한 필요는 없으며 날짜·Step·audit·commit 변경 이력은 results/ledger에 남긴다.
재현에 필요한 기계 정보와 과학적 데이터 provenance는 해당 companion/evidence manifest로 연결한다.

## 본문에 반드시 남길 이론

1. 정의·좌표·단위·부호·독립변수·domain, chemical reaction 및 charge/mass/capacity conservation.
2. 가정과 출발식에서 중간 연산을 거쳐 결과·극한·경계까지 이어지는 유도. 구현 문구 삭제를 이유로 유도 다리를 삭제하지 않는다.
3. equilibrium/metastability/kinetics/transport/열/측정 연산 및 graphite/LCO/Si/SiOx/Si–C/blend의 공통점과 차이.
4. 관측 Q(V), dQ/dV, dV/dQ·peak/valley/면적/background와 uncertainty·identifiability·held-out 검증의 물리적 해석.
5. verified primary source와 정확한 인용, competing model의 가정/한계, 데이터 부족과 conditional conclusion.
6. numerical analysis가 이론 이해에 필요한 경우 수학적 식·오차·수렴·가정으로 설명하되 프로그램 실행 순서/자료구조/API 안내로 바꾸지 않는다.

프로그램으로 계산한 결과라는 이유만으로 정당한 수식·과학적 그림을 본문에서 제외하지 않는다.
반대로 계산을 수행했다는 사실만으로 physical mechanism, material constant, 원문 support가 확보된 것도 아니다.
내부식/외부자료/실제 원문 근거의 권위는 Step102 및후속071/082/086/088의 기준을 그대로 따른다.

## 구현 영역으로 분리할 내용

- 함수/class/module/file/key/API 이름, call graph, loader/default 설정, shape·dtype·serialization·error contract.
- code listing, executable pseudocode, 실행/설치 명령, import/dependency/runtime/environment 안내.
- 채택 Equation ID에서 implementation consumer와 test로 가는 대응, tolerance·convergence implementation 계약.
- golden/bit-exact/internal conformance test와 실제 물리적 검증의 구분, 실패·보류한 구현 조건의 기술적 설명.
- numerical stabilization/regularization의 구현 방법. 그 방법의 물리 영향·bias·제거 극한 자체는 필요한 수학적 형태로 이론에 남긴다.

이동만으로 구현 적합성 또는 원고 순도 의무를 닫지 않는다.
외부 구현 계약은 모든 채택 계산식·가정·단위·domain·limit·필수자료를 보존하고 physical branch를 역추적해야 한다.
미구현 채택식을 THEORY_ONLY로 숨겨 acceptance에 포함하거나, 원래 empirical 결과를 버리고 새 물리 PASS로 바꾸지 않는다.
실제 오류 수정·equation traceability·test execution은 각 source-native owner와 Phase083–088의 작업으로 남는다.

## 의미 검독과 단어 검색의 역할

검색은 후보 발견용이며 의미 검독을 대체하지 않는다.
물리적 phase, 수학적 함수 f, 재료 class의 분류 의미처럼 진짜 과학 개념은 같은 영어 단어가 있다는 이유로 삭제하지 않는다.
반대로 표기만 수학 기호로 바꾼 API/file/key 설명이나 구현 지침은 본문에서 허용하지 않는다.
화학식/수식의 합법적인 기호 및 사용자 명명 관례를 코드 순도라는 이유로 임의 변경하지 않는다.

그림/표는 축·단위·legend·annotation·caption을 함께 확인하고, 코드 경로나 실행 로그가 보이면 같은 배치 규칙을 적용한다.
문헌의 실제 제목·DOI·서지 정보는 검색 경고를 없애기 위해 변조하지 않는다.
구현용 참고문헌은 구현 영역의 bibliography로 분리하며, load-bearing 과학 인용의 support와 원문 정확성을 훼손하지 않는다.
서지 내용과 엄격한 본문 경계가 실제로 충돌하는 사례는 숨기지 않고 해당 source의 범위·배치를 판단해야 한다.
목차·running heading·표/그림 목록도 코드 고유 식별자나 작업사를 노출하는 우회 통로가 되어서는 안 된다.

## 혼합된 기존 내용의 후속 처리

| 기존 내용 | 보존할 핵심 | 후속 처리 | 완료 증거 |
|---|---|---|---|
| 유도와 함수/file 설명이 섞인 문단 | 검증 가능한 유도·가정·도메인·물리적 한계 | Codex-owned 본문에서는 과학 내용만 증분 재구성; 구현 부분은 지정 구현 영역으로 연결 | 두 부분 모두 원 source anchor·claim 관계 보존 |
| 코드 기준으로 설명된 결과식 | 식의 실제 물리적 주장과 정확한 가정 | 원전·독립 유도와 대조 전에는 채택하지 않음; 구현과의 불일치는 별도 의무 유지 | 071/082 식 근거,083/088 conformance |
| 과거 PASS/GREEN·fit 성공 또는 작업사 | 실제 관측/실행 범위와 미확인 한계 | 작업사와 machine receipt는 results/evidence, 과학적으로 지지되는 내용만 본문 | 실제 source/data/실행 증거별 authority 분리 |
| stale PDF·source 불일치 또는 clipping | 원천과 이미지/식/표의 정확한 대응 | frozen 원본을 덮어쓰지 않고 후속 canonical source에서 재빌드·검독 | 089 전체 PDF/source/시각 QA |
| empirical 분해와 phase identity 혼동 | 경험적 예측 가치 및 데이터 범위 | empirical layer로 보존하고 기전 주장은 근거 없으면 보류 | 102 hierarchy,081 식별성,086 외부 검증 |

실제 수정 시 원래 claim/asset, 이유와 대체 위치를 기록한다.
완료된 역사 문건·Claude source·보호 branch를 덮어쓰거나 파일 통째 채택/삭제하는 행위는 Step101 범위 밖이다.

## Current Carry Linkage — 원문 조건 보존

선정42개=상속18+신규24, 연결 disposition69개다. 원문 registry316/655에서 해당 부분만
본문 순도·구현 배치·stale 문건·source/PDF 관계의 의미로 선정했다. 모든 항목은 OPEN_CARRY 그대로다.
나머지274개는 기존 불변 carry pointer로 보존되며 이 단계에서 제외됐다고 종료·기각되지 않는다.
아래 JSON은 source/carry 검토자의 실제 선정 기록이다. selector는 명시한 불변 blob의 정확한 배열 위치이며,
shared_fields의 acceptance alias는 해당 원문 문자열로 치환한다. 각 완전한 원행은 selector와 record hash로
계속 접근할 수 있다. disposition69개는 target_id의 유일한 행과 정렬된 [ID,index,rowSHA] 묶음으로 고정한다.
긴 원행을 다시 전사하지 않았다는 이유로 source acceptance, origin evidence, relation_links가 사라지지 않는다.

| 범위 | 내용 배치 / 뒤의 실제 수용 조건 |
|---|---|
| 상속18개 | version-bound companion와 v1.0.24 deltas, main-body topology·rendered prose purity, code-map/구현 각주 분리, stale guide/archive/build 상태, clipping/한글 glyph 및 source/PDF 검증을 각 원 owner에게 유지 |
| 신규0020 | 후보28페이지/13 header collision 및 긴 U13 각주 증거는089 재빌드·전페이지 QA 입력; 이번에 repaired PDF라 부르지 않음 |
| 신규0030/0031 | 과학 장·모든 재료의 역할은073, 물리계약/empirical 재현 산출물 분리는083; 목차나 model의 통째 채택 아님 |
| 신규0063/0064 | 같은 inputs.tex의 서로 다른 blob 두 건 모두 보존; 물리적 입력 정의는 본문, code/API/default/status는 지정 구현 영역 |
| 신규0068–0083 | driver/유도·가정·구현 부록/common/경험적·재료 장의 각 source-specific reconstruction 조건 유지. 순수 유도 부록과 구현 부록을 구분하며 linked scientific repair도 원 owner에게 그대로 유지 |
| 신규0084/0095 | conformance README와 test/dependency README는 구현·release 증거; 본문으로 전용하지 않고083/090 실제 계약·실행 조건 유지 |
| 신규0096 | 선택된 후속 preprocessing driver의 header/실제 pipeline 대응 조건; 미선택이면 원 mismatch 보존. P066-OBL-0124와 같은 owner라는 이유로 합치지 않음 |

INTENT-PROV-0350/-0376/-0383은 각각의 상속 ID로 연결하며 source occurrence의 비유일성을 숨기지 않는다.
D74-038과 purity 관련 여러 target은 many-to-many 관계이며 하나로 합쳐서 수용 조건을 줄이지 않는다.
C03/C06은 원래 별도 source predicates이며 Step105의 명시적 연결 대상으로 보존한다.
이 문건은 새 obligation ID 또는318개 독립 의무를 만들지 않는다.
검토자의 마지막 unknown은 실제 부록/companion source 배치가073/083에서 정해질 것이라는 뜻이다.
현재 계약은 지정 구현 부록 OR 별도 companion을 허용하며, 이를 새로운 사용자 승인 대기로 만들지 않는다.

```json
{
  "schema": "phase069.step101.body_carry_independent_review.v1",
  "reviewer": "phase044_source_freeze",
  "review_base": "227384f3437b0a83eb691b68b8e71d5e8daca288",
  "authority": "Read-only carry selection for the Step101 scholarly-body/implementation-appendix-or-companion boundary. No source repair, closure, re-owner, scientific approval, PDF/source replay, or new obligation ID.",
  "read_coverage": [
    {"path":"Codex/plans/2026-09-08-phase069-canonical-audit-launch-detailed-plan.md","blob":"81620a8b58948d4823dc47e5058a65195bab9e77","bytes":18273,"physical_lines":245,"sha256":"8316e3287e093259841d33213fed7ac63481e6c42d0e9791828f102e114f2f3d","read":"FRESH_FULL_1_EOF"},
    {"path":"Codex/results/PHASE_069_STEP_100_USER_REQUIREMENTS_RESULT.md","blob":"4b9eb19de3a0ac33a7941e855b3a12a6f44720c6","bytes":5070,"physical_lines":64,"sha256":"51b8a37da195a8cccbdc13433137f02c81969368ff3e58bf7d6f17bb0343552d","read":"FRESH_FULL_1_EOF"},
    {"path":"Codex/AGENTS.md","blob":"68218ce741a9a85b75323853f1d6f3ac3dc102e7","bytes":13866,"read":"EXACT_IDENTITY_REUSE_OF_PRIOR_FULL_1_EOF_READ; not freshly reread in Step101"},
    {"path":"Codex/results/PHASE_069_USER_REQUIREMENTS.md","blob":"ece7f4b56acf0fcf9084ef5397a13d54435529c1","bytes":45408,"physical_lines":480,"sha256":"1d817b5f195e7cb023ad0119d2c142dc7654275460f48ea2dee360567c897bd3","read":"FRESH_TARGETED_RANGES_285_340,390_435,460_480; NOT_FULL_READ"},
    {"path":"Codex/results/PHASE_069_USER_REQUIREMENTS.json","blob":"bc76d7c23032b1961ee4c9d99cf038d931310f0e","bytes":174137,"physical_lines":4261,"sha256":"16e4df4c626d0d5e8417e5397c2024914809d6a87139efa68c15b1156e382f87","read":"FRESH_SELECTED_FULL_RECORDS requirements[23],[24],[29],[31]; NOT_FULL_RAW_READ"},
    {"path":"Codex/results/PHASE_068_CARRY_FORWARD_DELTA.json","blob":"7d41aca4984c15bdb6161059994bdf3586ecdd76","bytes":503096,"physical_lines":12740,"sha256":"768026e729c946cd0785883c8a80cb760941f7ed4e932cd7b8f889ebae806e03","read":"EXACT_IDENTITY_REUSE of Step97 full inherited222/current identity check plus FRESH selected42 full-field and target-route inspection; NOT a fresh full316 read"},
    {"path":"Codex/results/PHASE_068_FORK_DISPOSITION_REGISTER.json","blob":"70d20f2b02679a7b3fb4cf29ce98902dae839ef7","bytes":1596173,"physical_lines":21000,"sha256":"79cfc14cb4839d0a8dd2134eeeeab14f7a27784e9a4878a57a8767ecceb088cc","read":"EXACT_IDENTITY_REUSE of Step97 full registry read plus FRESH selected69 target-row identity/source-field inspection; NOT a fresh full655 read"},
    {"path":"Codex/results/PHASE_057_PROVISIONAL_FINDING_LEDGER.json","blob":"e4000c331979a1f550d099a06712225829fafd32","bytes":565508,"physical_lines":6496,"sha256":"e55b20c6c207e905c63db3cc8fe2ba3c6b83a31a48256d21d2d404af20299877","read":"FRESH selected origin records only; NOT_FULL_RAW_READ"},
    {"path":"Codex/results/PHASE_057AT_V1025_HANDOVER_INDEX_OBSERVATIONS.md","blob":"b6fee4e7a83f78ecca4bcede1c09cd3489a404be","bytes":6757,"physical_lines":173,"sha256":"8118a355473ff1c6d4ba065179969c2957b2c2535baf334a0dabc86a434027de","read":"FRESH_FULL_1_EOF"},
    {"path":"Codex/results/PHASE_066_SOURCE_PROCESS_DELTA.json","blob":"381105cf481447d86ebb54f9e99f924b9db675af","bytes":799558,"physical_lines":21570,"sha256":"e24462702966dfb679953c6726b20b923eb7cf9591a24ba5297e7b20308f4d2b","read":"FRESH selected observed_defects[0:2] only; NOT_FULL_RAW_READ"}
  ],
  "boundary_ground": [
    {"id":"P069-REQ-024","selector":"requirements[23]","record_sha256":"3f93d0d52d520edf8fb945420ca6863100fb537d4c8506a7ad025d017092ebd6","meaning":"Body/captions/footnotes/visible headings exclude code/API/file/test/work-history; designated implementation appendix OR separate companion is the exception; derivation appendix is not a hidden implementation escape."},
    {"id":"P069-REQ-025","selector":"requirements[24]","record_sha256":"415c10d992872a177e74ab06da2396e1f2321065a34356b922d7d43ae85ad708","meaning":"Theory is upstream; implementation companion/code is downstream; equation/data/consumer mappings remain traceable without code-only knobs in theory."},
    {"id":"P069-REQ-030","selector":"requirements[29]","record_sha256":"ad6713028f1729eadaa92fed1538ad4651ab3a1ede3505d722885a9466e9e576","meaning":"Canonical LaTeX source to PDF preserves pure-body/derivation-appendix/implementation-exception boundary; build/render/page/hash gates remain later work."},
    {"id":"P069-REQ-032","selector":"requirements[31]","record_sha256":"ee30365128645efaf5dbf11be8f6c35abc468a85a727ec15d9be6f876bb78c5a","meaning":"Preserve 316 active carry, original owner/acceptance and zero inherited closure; no 318 or new IDs."}
  ],
  "carry_invariants": {"inherited":222,"new":94,"total_active":316,"closed_inherited":0,"register_rows":655,"atomic_scientific_denominator_claimed":false,"C03_C06":"unchanged source-native owner/acceptance; Step105 route; not selected as separate Step101/318 obligations"},
  "shared_fields": {
    "A87":"PHASE-087-CANONICAL-SOURCE-SYNTHESIS must resolve or explicitly bound this exact observation before canonical release without backward projection.",
    "A89":"PHASE-089-LATEX-PDF-RELEASE-QA must resolve or explicitly bound this exact observation before canonical release without backward projection.",
    "A89D":"PHASE-089-LATEX-PDF-RELEASE-QA must resolve or explicitly bound this observation before canonical release.",
    "PINH":"Preserve exact inherited source predicate, state, owner, acceptance and relation links; no closure or re-owner.",
    "PFILE":"Exact source/path-specific assembly acceptance, not a duplicate scientific repair. Satisfy linked repair obligations plus this file's stated reconstruction/support prerequisites.",
    "AMAN":"Reconstruct from explicit derivations and verified sources; resolve every linked scope defect, preserve material alternatives and separate designated implementation appendix/companion."
  },
  "selected_inherited": [
    {"id":"P065-OBL-0066","type":"INHERITED_OBLIGATION","selector":"inherited_active[65]","sha":"d834b74b1dfce064fb4072e75db0a3defbeeb10fe4123073014d940ace236e38","topic":"D74-015","owner":"PHASE-087-MANUSCRIPT-ASSEMBLY","phase":87,"state":"OPEN_CARRY","acceptance":"Issue a version-bound companion or explicitly state the preserved older procedure and enumerate v1.0.24 deltas.","predicate":"PINH","relations":["P065-S70-F43"]},
    {"id":"P065-OBL-0085","type":"INHERITED_OBLIGATION","selector":"inherited_active[84]","sha":"5053e6c8cba2fe66759a312101042ab235801eb3d0402e18c55c6802d688babc","topic":"D74-038","owner":"PHASE-087-MANUSCRIPT-ASSEMBLY","phase":87,"state":"OPEN_CARRY","acceptance":"Preserve the full-read main-body topology manifest; reduce rendered pre-appendix prose and captions containing implementation identifiers/defaults/override/fallback/toggle/placeholder warnings/bit-exact/regression/backward-compatibility/current implementation status to zero; keep mathematical limits, numerical checks and physical uncertainty as code-independent science; move implementation detail to the designated appendix or guide; verify rendered prose rather than raw grep comments or label keys.","predicate":"PINH","relations":[],"linked_targets":["C92-03","C92-12","C92-16","C92-30","C95-11","F92-P1-01","FILE97-010","FILE97-011","FILE97-051","FILE97-061","FILE97-063","H44-ARCH-008","H44-GOV-007","H44-PURE-001","H44-PURE-002","H44-PURE-003","PHY-031"]},
    {"id":"P066-OBL-0007","type":"INHERITED_OBLIGATION","selector":"inherited_active[100]","sha":"fda132275bd12c45eea2a3213d182ae02f977c3ac63435b22e5fb3ba2ef1b415","topic":"INTENT-PROV-0299","owner":"PHASE-089-LATEX-PDF-RELEASE-QA","phase":89,"state":"OPEN_CARRY","acceptance":"A89","predicate":"PINH","relations":[]},
    {"id":"P066-OBL-0021","type":"INHERITED_OBLIGATION","selector":"inherited_active[114]","sha":"4aa20b356eed86385c8a40f03c1d9db5cfcdcd1227d21d5492a0b7b3d7a4c4cf","topic":"INTENT-PROV-0315","owner":"PHASE-087-CANONICAL-SOURCE-SYNTHESIS","phase":87,"state":"OPEN_CARRY","acceptance":"A87","predicate":"PINH","relations":[],"linked_targets":["C95-11","F92-P1-01","FILE97-010","FILE97-011","FILE97-051","FILE97-061","FILE97-063"]},
    {"id":"P066-OBL-0029","type":"INHERITED_OBLIGATION","selector":"inherited_active[122]","sha":"a0238aba2abfe7bedd9d9c3dbfc651cf7c9d96b11e2802345646a8fde4275513","topic":"INTENT-PROV-0323","owner":"PHASE-089-LATEX-PDF-RELEASE-QA","phase":89,"state":"OPEN_CARRY","acceptance":"A89","predicate":"PINH","relations":[]},
    {"id":"P066-OBL-0030","type":"INHERITED_OBLIGATION","selector":"inherited_active[123]","sha":"3ffd1b8e8d1ccb212d493670057e06ab5cc5c9e5add920e333813c80487ac1b3","topic":"INTENT-PROV-0324","owner":"PHASE-089-LATEX-PDF-RELEASE-QA","phase":89,"state":"OPEN_CARRY","acceptance":"A89","predicate":"PINH","relations":[]},
    {"id":"P066-OBL-0033","type":"INHERITED_OBLIGATION","selector":"inherited_active[126]","sha":"d04d8a13645d4a86bc8e9f24ea462e6271432790df01a59ba1193d216edec4fc","topic":"INTENT-PROV-0329","owner":"PHASE-089-LATEX-PDF-RELEASE-QA","phase":89,"state":"OPEN_CARRY","acceptance":"A89","predicate":"PINH","relations":[]},
    {"id":"P066-OBL-0035","type":"INHERITED_OBLIGATION","selector":"inherited_active[128]","sha":"04ae021d9ec7b2bf89b30668489bd15196315884aae20984a736d34026b50cfd","topic":"INTENT-PROV-0331","owner":"PHASE-087-CANONICAL-SOURCE-SYNTHESIS","phase":87,"state":"OPEN_CARRY","acceptance":"A87","predicate":"PINH","relations":[],"linked_targets":["C95-11","F92-P1-01","FILE97-010","FILE97-011","FILE97-051","FILE97-061","FILE97-063"]},
    {"id":"P066-OBL-0037","type":"INHERITED_OBLIGATION","selector":"inherited_active[130]","sha":"f14d39e3b46803fd18cceaf7ee1208f7146bb4f8d60b6ae01ccf620e614070ee","topic":"INTENT-PROV-0333","owner":"PHASE-089-LATEX-PDF-RELEASE-QA","phase":89,"state":"OPEN_CARRY","acceptance":"A89","predicate":"PINH","relations":[]},
    {"id":"P066-OBL-0046","type":"INHERITED_OBLIGATION","selector":"inherited_active[139]","sha":"6ca994867dc0a698b24c09e229a8d1af40d93b46266a6c29ab5da5dec8cc7c4a","topic":"INTENT-PROV-0343","owner":"PHASE-087-CANONICAL-SOURCE-SYNTHESIS","phase":87,"state":"OPEN_CARRY","acceptance":"A87","predicate":"PINH","relations":[],"linked_targets":["C95-11","F92-P1-01","FILE97-010","FILE97-011","FILE97-051","FILE97-061","FILE97-063"]},
    {"id":"P066-OBL-0052","type":"INHERITED_OBLIGATION","selector":"inherited_active[145]","sha":"39cdda9c63cca2d0d487c3d6f2f66000bf4ae37735aa0f049829fd6ed554336d","topic":"INTENT-PROV-0350","owner":"PHASE-087-CANONICAL-SOURCE-SYNTHESIS","phase":87,"state":"OPEN_CARRY","acceptance":"A87","predicate":"PINH","relations":[]},
    {"id":"P066-OBL-0060","type":"INHERITED_OBLIGATION","selector":"inherited_active[153]","sha":"2357d5a816dbf2c9a50705a2af54787ee7b0f352b07b03346c2386a416c96f10","topic":"INTENT-PROV-0361","owner":"PHASE-089-LATEX-PDF-RELEASE-QA","phase":89,"state":"OPEN_CARRY","acceptance":"A89","predicate":"PINH","relations":[]},
    {"id":"P066-OBL-0070","type":"INHERITED_OBLIGATION","selector":"inherited_active[163]","sha":"c17361c60b2979e0c4f37678360d76712d3beae25650a292aeac12cec231ef24","topic":"INTENT-PROV-0372","owner":"PHASE-087-CANONICAL-SOURCE-SYNTHESIS","phase":87,"state":"OPEN_CARRY","acceptance":"A87","predicate":"PINH","relations":[],"linked_targets":["C95-11","F92-P1-01","FILE97-010","FILE97-011","FILE97-051","FILE97-061","FILE97-063"]},
    {"id":"P066-OBL-0074","type":"INHERITED_OBLIGATION","selector":"inherited_active[167]","sha":"52abfea07dbb7dca710c1ca13d02f16d2c625d83f056976aebdcb192249c4a89","topic":"INTENT-PROV-0376","owner":"PHASE-087-CANONICAL-SOURCE-SYNTHESIS","phase":87,"state":"OPEN_CARRY","acceptance":"A87","predicate":"PINH","relations":[]},
    {"id":"P066-OBL-0077","type":"INHERITED_OBLIGATION","selector":"inherited_active[170]","sha":"1a5e90874887f0a7bc16a0a9927ff91b08fcb430c081b7e6859c20d2378b9425","topic":"INTENT-PROV-0380","owner":"PHASE-087-CANONICAL-SOURCE-SYNTHESIS","phase":87,"state":"OPEN_CARRY","acceptance":"A87","predicate":"PINH","relations":[],"linked_targets":["C95-11","F92-P1-01","FILE97-010","FILE97-011","FILE97-051","FILE97-061","FILE97-063"]},
    {"id":"P066-OBL-0080","type":"INHERITED_OBLIGATION","selector":"inherited_active[173]","sha":"d2ae4a05f81a87a5c9eb715555a07eb6106a6863ab63015ed7640b67b39ffa30","topic":"INTENT-PROV-0383","owner":"PHASE-087-CANONICAL-SOURCE-SYNTHESIS","phase":87,"state":"OPEN_CARRY","acceptance":"A87","predicate":"PINH","relations":[]},
    {"id":"P066-OBL-0084","type":"INHERITED_OBLIGATION","selector":"inherited_active[177]","sha":"3464e5c773f7e0260fe4b391d472997ca09f1268e8fd33590c8c3c4f9b0694d9","topic":"P066-S76-DEFECT-001","owner":"PHASE-089-LATEX-PDF-RELEASE-QA","phase":89,"state":"OPEN_CARRY","acceptance":"A89D","predicate":"PINH","relations":[]},
    {"id":"P066-OBL-0085","type":"INHERITED_OBLIGATION","selector":"inherited_active[178]","sha":"06d7f7424b9593fa70aaaaac06fbb810953b7cb207bc198a354a8a759d2dcfa4","topic":"P066-S76-DEFECT-002","owner":"PHASE-089-LATEX-PDF-RELEASE-QA","phase":89,"state":"OPEN_CARRY","acceptance":"A89D","predicate":"PINH","relations":[]}
  ],
  "selected_new_unique": [
    {"id":"P068-OBL-0020","type":"NEW_SOURCE_SCOPED_OBLIGATION","selector":"new_obligations[18]","sha":"04407225fa1534877329b39ff8d928f144c6df4d779682d773a7c25ec6568bf9","topic":"CANDIDATE_PDF_HEADERS","owner":"PHASE-089-PDF-RELEASE-QA","phase":89,"state":"OPEN_CARRY","acceptance":"Build only authorized canonical LaTeX, clean3pass, inspect allpages and U13long-footnote/header regions; preserve exact28-page candidate/13collision evidence without claiming current rebuilt release.","predicate":"New explicit fork residual/source-scoped reconstruction; not inherited closure/replacement.","relations":["F92-P1-03","C92-28","C91-51","C91-60","C91-83","FILE97-095"],"source":"new_obligations[18].evidence"},
    {"id":"P068-OBL-0030","type":"NEW_SOURCE_SCOPED_OBLIGATION","selector":"new_obligations[28]","sha":"234b558ce04410d2d9fdaa273d1e9606e342dd920cbd09c5a7616f3914d5bf90","topic":"SCIENTIFIC_DOCUMENT_ARCHITECTURE","owner":"PHASE-073-THEORY-ARCHITECTURE","phase":73,"state":"OPEN_CARRY","acceptance":"At Phase073 retain all named scientific chapter/material roles and exact conditional content, map each source/EquationID and draft Codex-owned sections without wholechapter selection or loss of LCO/Si/blend.","predicate":"No final TOC/whole-chapter adoption; each linked H44-ARCH source acceptance keeps implementation/history outside body/captions/footnotes/headings.","relations":["H44-ARCH-001","H44-ARCH-002","H44-ARCH-003","H44-ARCH-004","H44-ARCH-005","H44-ARCH-006","H44-ARCH-009","H44-V-1020"],"source":"new_obligations[28].evidence"},
    {"id":"P068-OBL-0031","type":"NEW_SOURCE_SCOPED_OBLIGATION","selector":"new_obligations[29]","sha":"ba5017ab8cb9815f3f99b5f6a91c073227a716ef5e71333a559578fb51f827d2","topic":"REFERENCE_IMPLEMENTATION_PRODUCTS","owner":"PHASE-083-IMPLEMENTATION-CONTRACT","phase":83,"state":"OPEN_CARRY","acceptance":"Separate immutable empirical profile/reconstruction product from source-backed physical state/material contracts; preserve source-specific equations/domain/failure behavior and failed historical hashes.","predicate":"Reference implementation/product is downstream companion evidence, not scholarly-body authority.","relations":["H44-ARCH-007","H44-PROD-001","H44-PROD-002"],"linked_targets":["H44-V-1022"],"source":"new_obligations[29].evidence"},
    {"id":"P068-OBL-0063","type":"NEW_SOURCE_SCOPED_OBLIGATION","selector":"new_obligations[60]","sha":"20e15f55389714ce4d2d1572004b9241dd41201a919b706aa92af5ecd673f900","topic":"FILE_ACCEPTANCE_FILE97-010","owner":"PHASE-087-MANUSCRIPT-ASSEMBLY","phase":87,"state":"OPEN_CARRY","acceptance":"Separate physical input definitions from code/API/default/status details; verify semantic body purity.","predicate":"PFILE","relations":["FILE97-010"],"source":{"path":"Claude/docs/v1.0.25.2/_sections/ch1_sec18_inputs.tex","blob":"115ada92b09387a76b7f0d2385fcd077e326c1c6","record_sha256":"fdb3c6bf5bbd10a822bb8736744e1dbb83d941ee38f509ed85b796672cde7cc6"}},
    {"id":"P068-OBL-0064","type":"NEW_SOURCE_SCOPED_OBLIGATION","selector":"new_obligations[61]","sha":"0e952fc4dcaf9b036d01b8caa10ae6a2099a029b29d4c31ae54b8b86bf74fb49","topic":"FILE_ACCEPTANCE_FILE97-011","owner":"PHASE-087-MANUSCRIPT-ASSEMBLY","phase":87,"state":"OPEN_CARRY","acceptance":"Separate physical input definitions from code/API/default/status details; verify semantic body purity.","predicate":"PFILE","relations":["FILE97-011"],"source":{"path":"Claude/docs/v1.0.25.2/_sections/ch1_sec18_inputs.tex","blob":"614d63d0e18e5eb7939f2c0ec0bdb9ee4623d1ce","record_sha256":"fb760e21bc484a8b178338c1daa49924dbae7b38544338f3d754dd4e72a1e334"}},
    {"id":"P068-OBL-0084","type":"NEW_SOURCE_SCOPED_OBLIGATION","selector":"new_obligations[81]","sha":"8143633718697d340b7cb0ccc38edd8ba2e4e6dc204dc66f42aa24c0fc40497b","topic":"FILE_ACCEPTANCE_FILE97-067","owner":"PHASE-083-IMPLEMENTATION-CONTRACT","phase":83,"state":"OPEN_CARRY","acceptance":"Bind to later canonical equations, declare exact units/domain/failure behavior, address Step95 findings and test the authorized successor; preserve source originals.","predicate":"PFILE; route conformance README as companion/implementation evidence, not scholarly body.","relations":["FILE97-067"],"source":{"path":"Codex/work/v1025_2_physics_branch/conformance_model/README.md","blob":"62ec65b9f3d10c1271e0459fceafb514adbb1dc6","record_sha256":"ea08511d699669a5b0c2961115bd6f374eebeba8eafc93a429f30adddf88f728"}},
    {"id":"P068-OBL-0095","type":"NEW_SOURCE_SCOPED_OBLIGATION","selector":"new_obligations[92]","sha":"dcc09da391668e916215d89fad990ffd8e8ca3a4b072278668b4ddbf3da9ed34","topic":"FILE_ACCEPTANCE_FILE97-085","owner":"PHASE-090-CLEAN-CLONE-RELEASE","phase":90,"state":"OPEN_CARRY","acceptance":"Declare NumPy/Pandas/SciPy and all seven exact fixture requirements; execute clean bootstrap and report actual collection/execution.","predicate":"PFILE; test/dependency README remains companion/release evidence, never scholarly body.","relations":["FILE97-085"],"source":{"path":"Codex/work/v1025_2_physics_branch/tests/README.md","blob":"f52d7a51b856fcd02283c989a8be08e41c77a251","record_sha256":"0eaeebf062a1bd857e4738270aada6d9246a616183af2f2140c01e1ffd45cd0e"}},
    {"id":"P068-OBL-0096","type":"NEW_SOURCE_SCOPED_OBLIGATION","selector":"new_obligations[93]","sha":"1750ea37c6055daf306d5d8f774fa39ad389657497c56cde0c350076deb6e4e3","topic":"PREPROCESSING_DRIVER_HEADER_SCOPE","owner":"Phase 083 theory–implementation contract","phase":83,"state":"OPEN_CARRY","acceptance":"If the exact preprocessing driver is selected in an authorized successor, align its dMSMCD/wavelet header with the observed isotonic/rebin/SG pipeline and source identities. If not selected, retain the historical mismatch without claiming repaired frozen source. This is documentation/source-selection scope, not a scientific model obligation.","predicate":"Distinct source/predicate from P066-OBL-0124; no owner/predicate merge.","relations":["H44-FIT-003"],"source":{"path":"Codex/results/PHASE_068_FORK_CONFLICT_MATRIX.json","blob":"6d8da1b58832fa8ce55d3714b1eb591eb163dfa7","selector":"rows[166]","record_sha256":"4d764c434e88f5af7822cffff834aa573e0a08b29db38eba79b6def4f541e072"}}
  ],
  "selected_new_manuscript_group": {
    "type":"NEW_SOURCE_SCOPED_OBLIGATION","state":"OPEN_CARRY","acceptance":"AMAN","predicate":"PFILE",
    "rows":[
      ["P068-OBL-0068","new_obligations[65]","4c604aaf6b90c2d71e4075f0fb625ebd7bd270683d43b9d75e6e20660c948fae","FILE97-051","PHASE-087-MANUSCRIPT-ASSEMBLY",87,"Codex/results/v1025_2_physics_branch/manuscript/anode_physics_master.tex","439cbf2fbea260c91561ac3f1c298c64605ac250","fd0dd48530f09c9ea308d38fdd395dfd28c905d89f650e85e96cf1917f28a746"],
      ["P068-OBL-0069","new_obligations[66]","594b80db84cc72546e6a0afa5731fb9a56ebc74cc0c826a29d3a271ab18f5fd8","FILE97-052","PHASE-073-THEORY-ARCHITECTURE",73,"Codex/results/v1025_2_physics_branch/manuscript/appendices/assumption_register.tex","8c018772eeacbb7b92d94ed8c369b4503aa9e686","f4b5526560af795b2572ab70432644250d5b5eb9a0fc6b9bbe5f131339a0f883"],
      ["P068-OBL-0070","new_obligations[67]","d317c31e4c7164ec04ec371aa981a2723f5ed5313ff0adafd2c074cadb542830","FILE97-053","PHASE-082-EQUATION-FREEZE",82,"Codex/results/v1025_2_physics_branch/manuscript/appendices/derivation_checks.tex","5a90f2698ab81c4fe537d7322619f8f0b2a17179","80054eebd5827e51a08e90aab0b1eac7634583ec5dfd03b0f689eb55c7bcd2b0"],
      ["P068-OBL-0071","new_obligations[68]","27a073061aaf76e4cec6f6f0970b122451a211d7dc807ffec87c6dc7661b6079","FILE97-054","PHASE-083-IMPLEMENTATION-CONTRACT",83,"Codex/results/v1025_2_physics_branch/manuscript/appendices/implementation_interface.tex","867754ff009503bc9217eef803cfb64b26d18536","7002a8f20f03175bd96284d4bdce4626a950cc5022fc7ff409ea59f99c7ac03e"],
      ["P068-OBL-0072","new_obligations[69]","a0e504f48ee159d5f6f32cf7e8980207ab135e15b26bd4fe9bf455df329d0cdf","FILE97-055","PHASE-075-EQUILIBRIUM-PHASE",75,"Codex/results/v1025_2_physics_branch/manuscript/chapters/ch01_equilibrium_observation.tex","6564bb71bda2e0b927420400e8e9e670969ff8ef","c3df58da6e6efa0ce402b330e1a7d0b4517a3b64ce1bdf810ed41a1874d6e922"],
      ["P068-OBL-0073","new_obligations[70]","cf822a9422853f65f4d9dc07d287837c1835141e9bfcc38a58efcb943148a3dd","FILE97-056","PHASE-081-INFERENCE-UNCERTAINTY",81,"Codex/results/v1025_2_physics_branch/manuscript/chapters/ch02_thermodynamics_heat.tex","d2d0a3f3937552f38bf5d24ea5d21b8bece9c8c2","6ef49705c33a769dd6a0208d697928ec9024ce6ecadfe1718be249dc4d087946"],
      ["P068-OBL-0074","new_obligations[71]","f1547130e79609021027201a9d6443ab7dd155c2a8a610115ffac8dddda7030d","FILE97-057","PHASE-076-NONEQUILIBRIUM",76,"Codex/results/v1025_2_physics_branch/manuscript/chapters/ch03_kinetics.tex","1e286bac33584b12edb803d111c1e5325db625dc","91bf279f047e2542cc2fa03118ec513a29ab673ceb532dc761c4c72603cde1a8"],
      ["P068-OBL-0075","new_obligations[72]","e7125d680228bfea91c8d7d54b442848c90ec63b736c38f880a72ad6832ff7eb","FILE97-058","PHASE-081-INFERENCE-UNCERTAINTY",81,"Codex/results/v1025_2_physics_branch/manuscript/chapters/ch04_integrated_eos.tex","900a2f32d4e8ba0e590503181962e32f2dc9294b","b429aa6a4b0fb6b69a472dc2048cc14c756a6df1a85732c14b06903f63053afb"],
      ["P068-OBL-0076","new_obligations[73]","99cef4052e4efba0d9199c0d68b035bb58074570d4cbdaeb35f576bc7889e579","FILE97-059","PHASE-076-NONEQUILIBRIUM",76,"Codex/results/v1025_2_physics_branch/manuscript/chapters/ch05_hysteresis.tex","f7251fd1117ac72eb9f9925fbab1d0ca0e827ed2","ccc95e2191ca628108ff46c29edac734c9705bc3c6dadc47444e5ee03c5ac49e"],
      ["P068-OBL-0077","new_obligations[74]","a9a1f054813eac5b0702f900f49fa050e4c85e31b7565c8508c1b647e6059cce","FILE97-060","PHASE-074-FOUNDATION",74,"Codex/results/v1025_2_physics_branch/manuscript/common/conventions.tex","6a8d957f88fedc1096882019c361a7ee79888424","6b804ef368ab87900bb3a8ce87fd2f165dd43331698002f632c47c4ea226954f"],
      ["P068-OBL-0078","new_obligations[75]","570b45960ab9c30adbe0cdd54dd665d70e6793b31ea37ccd2b319f4f97abbea1","FILE97-061","PHASE-087-MANUSCRIPT-ASSEMBLY",87,"Codex/results/v1025_2_physics_branch/manuscript/common/evidence_grades.tex","fd147f69ab13dbe5b1bbd3b40e334f353fb6b329","e392ac3f5dbb451ac31d8c20d180e077f95e0ed6face26d57ce449e5b9e88bca"],
      ["P068-OBL-0079","new_obligations[76]","17282cada89a084f0e436bf80f62d4d53f8272a491e1ab544003bce33bad2678","FILE97-062","PHASE-074-FOUNDATION",74,"Codex/results/v1025_2_physics_branch/manuscript/common/notation.tex","83a0eda0d44a378c84e379f5919c0d2359d78450","d541434c2fd424392383dad2521b0b098838871b71fdc8f71028747219f46c4f"],
      ["P068-OBL-0080","new_obligations[77]","60bf9960600b91f1b96db6bb234fa3698334e0de44fd26362379f76d1c2a8473","FILE97-063","PHASE-087-MANUSCRIPT-ASSEMBLY",87,"Codex/results/v1025_2_physics_branch/manuscript/empirical/skew14_profile.tex","20107d8f8f69ab8e4f10c3ca233d32380e919523","29327023c67d8d3d1b32255c6c04530cac0557c5398c14584e0deefddb7000cb"],
      ["P068-OBL-0081","new_obligations[78]","2aa1d04e000553e72c5d35b65dc20bab2a82eaaf1d70168a06e0f7d9a3f9b9be","FILE97-064","PHASE-077-GRAPHITE-CLOSURE",77,"Codex/results/v1025_2_physics_branch/manuscript/materials/graphite_application.tex","bda7825d1dc6081634b4544cc43e0221b250a41f","c8957985094713eb56119472b0ad3f94f7579f62d1a7653fab39cb49f7c84a92"],
      ["P068-OBL-0082","new_obligations[79]","66edc4a5f9a3435a0bf7a7762b5596e020f04da5fd71022b0e1771031a945612","FILE97-065","PHASE-078-LCO-CLOSURE",78,"Codex/results/v1025_2_physics_branch/manuscript/materials/lco_application.tex","b23532f83353cf8a4ef37dd17116f3c4f5176013","d3cf4a02896c5c1088b744ff2f7c8bbea8d2a2543aaeba82c9119bc5ce31c352"],
      ["P068-OBL-0083","new_obligations[80]","7f69a46e33ee9d382ea7071fd31f4c72b9d117531470e8ceede58b14edd3706c","FILE97-066","PHASE-080-BLEND-CLOSURE",80,"Codex/results/v1025_2_physics_branch/manuscript/materials/si_blend_application.tex","8112e8c10c0170e67f2bec109df79343b3b02bac","e6efce58ed73185a48c113bf92ba405eb64828cb257a5f74ef672967e88d9b2b"]
    ],
    "row_columns":["id","selector","record_sha256","topic_and_relation_target","owner","target_phase","source_path","source_blob","source_record_sha256"]
  },
  "selected_origin_records": [
    ["INTENT-PROV-0299","records[298]","v1.0.25와 v1.0.25.1의 빌드 검증 시점은 다르다","Codex/results/PHASE_057AO_V1025_ARCHIVE_TOUCHUP_OBSERVATIONS.md",[106,117],"67d6b19b13e15999dfef66ac19530682a5c817b01a3265a724699311d8d8ddfa"],
    ["INTENT-PROV-0315","records[314]","이론 본문에 코드 이름과 gate를 삽입한 방식은 폐기한다","Codex/results/PHASE_057AQ_V1025_CASCADE_LEDGER_OBSERVATIONS.md",[34,48],"c959ee44cbb62060d3bd82a25a62d4859b8cbf78b672f8e400782a99bff2b990"],
    ["INTENT-PROV-0323","records[322]","검증 뒤 동시 편집이 계속되어 당시 PASS snapshot이 최종 source를 보증하지 않는다","Codex/results/PHASE_057AQ_V1025_CASCADE_LEDGER_OBSERVATIONS.md",[154,168],"6485a42b47a9c3eb84472752ce6e44beb812c3f120b71a3095e7110d390903c9"],
    ["INTENT-PROV-0324","records[323]","누락된 gate와 축소 편집 범위는 후속 모순 가능성을 남겼다","Codex/results/PHASE_057AQ_V1025_CASCADE_LEDGER_OBSERVATIONS.md",[169,180],"a11a57cfa43b30cdcab19a2785a1df6ead605efd2b06f4e848f47bb9270c8ee5"],
    ["INTENT-PROV-0329","records[328]","실행 보고서 자체도 이동 중인 source snapshot을 기록했다","Codex/results/PHASE_057AR_V1025_T13_T14_OBSERVATIONS.md",[60,74],"275bb4364eda93bc09de28f44574d4832b3934722b468e948c8b74b2032abfc7"],
    ["INTENT-PROV-0331","records[330]","master 파일에서 code 문자열이 없다는 검사는 이론 문건의 코드 배제를 보증하지 않는다","Codex/results/PHASE_057AR_V1025_T13_T14_OBSERVATIONS.md",[88,100],"aa42a7e3b0f8f7e78e7600cfec90d76835844efde9deb2b2c6753b4cd1a90a43"],
    ["INTENT-PROV-0333","records[332]","구조 검사와 실제 build는 역할이 다르다는 경계는 정확하다","Codex/results/PHASE_057AR_V1025_T13_T14_OBSERVATIONS.md",[114,125],"00c592ae6b7b9709a29913284d2135b0a04c9c0671fca88acf2f0819b0e8e87a"],
    ["INTENT-PROV-0343","records[342]","code map과 구현 각주는 최종 이론 문건에서 분리해야 한다","Codex/results/PHASE_057AS_V1025_DOC_EDIT_OBSERVATIONS.md",[133,144],"79dacb5cac568547fa165a57cfe38076b23645858ea36a91c283c2cfb7f659d2"],
    ["INTENT-PROV-0350","records[349]","v1.0.25 당시 code guide와 fitting guide가 이미 stale했다","Codex/results/PHASE_057AT_V1025_HANDOVER_INDEX_OBSERVATIONS.md",[89,101],"9bc21089aeb2bb01877600bc23a392825f647b2a11e8fa1988b9e43a6e72cf73"],
    ["INTENT-PROV-0361","records[360]","원본과 동일한 warning profile은 유용하지만 충분한 조판 검사는 아니다","Codex/results/PHASE_057AU_V1025_MERGE_READINESS_OBSERVATIONS.md",[99,109],"f892b8bbc94bcec256cee44a4ddd6f7a1ee124d1d9cdf58e92e74872a0f6f956"],
    ["INTENT-PROV-0372","records[371]","구현 서술을 본문에서 옮긴 조치는 사용자 경계를 확인한다","Codex/results/PHASE_057AV_V1025_2_ARCHIVE_OBSERVATIONS.md",[136,147],"c9160f244ea27cf49fd64b19329e274aed4f747f37c108ddb41b8e10af114d4f"],
    ["INTENT-PROV-0376","records[375]","v1.0.25.2는 최신이지만 archive heading 자체는 stale하다","Codex/results/PHASE_057AV_V1025_2_ARCHIVE_OBSERVATIONS.md",[185,196],"f15976af8d7f175f01e0cf4f39523ee214f4ff2d496fa295d0bdf74c79c49252"],
    ["INTENT-PROV-0380","records[379]","문건의 코드 배제는 사용자가 직접 확정한 규칙이다","Codex/results/PHASE_057AW_V1025_2_HANDOVER_OBSERVATIONS.md",[44,56],"335cbaf7e8bcfc758685026be0073bcafc66b03ff12c0d2fe5e66b9cb99fb04f"],
    ["INTENT-PROV-0383","records[382]","latest 문건은 build가 끝나지 않았다","Codex/results/PHASE_057AW_V1025_2_HANDOVER_OBSERVATIONS.md",[86,96],"d762744d99be15a3524acc9df140e789a140cd466a3d4ad1bafa4a9a683ee78f"]
  ],
  "origin_record_columns":["origin_id","ledger_selector","title","source_path","source_lines","source_block_sha256"],
  "selected_defects": [
    {"origin":"P066-S76-DEFECT-001","selector":"observed_defects[0]","record_sha256":"4ba72b6497c569364343f51ec0c99151a076245cb9105ccc7d4f69690d60aade","kind":"PDF_RIGHT_CLIPPING","path":"Claude/docs/v1.0.25/ch1_graphite_v1.0.24.pdf","blob":"4e379edfaf9bd6ca8fc1da32ac036fe84728744e","page":50,"status":"OPEN_ROUTED"},
    {"origin":"P066-S76-DEFECT-002","selector":"observed_defects[1]","record_sha256":"91998f3893e697a6af64c66f1df08be41d82ae06cd4cede0e19e4df07ee766ae","kind":"EMBEDDED_PNG_KOREAN_GLYPH_MISSING","path":"Claude/docs/v1.0.25.2/results/KERNEL_COMPARISON_REPORT_v1025_2.html","blob":"4086482f28af182fb16fbbe02fd1f9f1cc52c69c","embedded_png_count":9,"status":"OPEN_ROUTED"}
  ],
  "disposition_binding": {
    "register_blob":"70d20f2b02679a7b3fb4cf29ce98902dae839ef7",
    "lookup":"rows[target_id=<listed ID>]; every listed target occurred exactly once among 655 rows",
    "selected_target_count":69,
    "canonical_triples_sha256":"d8f5547a40497a1ef9db34211446185ac9de279076be7690cf4e414e9dd0a2f6",
    "canonical_triple_definition":"SHA256 canonical UTF-8 JSON of sorted [target_id,row_index,canonical_record_sha256] triples",
    "target_ids":["C91-51","C91-60","C91-83","C92-03","C92-12","C92-16","C92-28","C92-30","C95-11","F92-P1-01","F92-P1-03","FILE97-010","FILE97-011","FILE97-051","FILE97-052","FILE97-053","FILE97-054","FILE97-055","FILE97-056","FILE97-057","FILE97-058","FILE97-059","FILE97-060","FILE97-061","FILE97-062","FILE97-063","FILE97-064","FILE97-065","FILE97-066","FILE97-067","FILE97-085","FILE97-095","H44-ARCH-001","H44-ARCH-002","H44-ARCH-003","H44-ARCH-004","H44-ARCH-005","H44-ARCH-006","H44-ARCH-007","H44-ARCH-008","H44-ARCH-009","H44-FIT-003","H44-GOV-007","H44-PROD-001","H44-PROD-002","H44-PURE-001","H44-PURE-002","H44-PURE-003","H44-V-1020","H44-V-1022","P065-OBL-0066","P065-OBL-0085","P066-OBL-0007","P066-OBL-0021","P066-OBL-0029","P066-OBL-0030","P066-OBL-0033","P066-OBL-0035","P066-OBL-0037","P066-OBL-0046","P066-OBL-0052","P066-OBL-0060","P066-OBL-0070","P066-OBL-0074","P066-OBL-0077","P066-OBL-0080","P066-OBL-0084","P066-OBL-0085","PHY-031"]
  },
  "selection_summary": {"selected_total":42,"selected_inherited":18,"selected_new":24,"selected_new_manuscript_file_rows":16,"selection_basis":"Semantic direct relevance to body code/work-history separation, designated implementation appendix or separate companion, caption/footnote/heading purity, stale documentation, and source/PDF/layout/build provenance. Keyword search was candidate generation only."},
  "nonclosure": [
    "All 42 selected obligations remain OPEN_CARRY with original owner/acceptance/state; selection is a Step101 boundary link, not completion.",
    "The other 274 active obligations remain losslessly reachable through the unchanged 316-carry pointer; their omission from this focused set is not closure or irrelevance to later science/material gates.",
    "P065-OBL-0085 is many-to-many with H44-PURE/ARCH/GOV/C95/F92/FILE/PHY targets; this mapping does not collapse their predicates.",
    "INTENT-PROV-0350, -0376 and -0383 each have one inherited obligation route here; source-document occurrences may be non-unique, so no owner/path equivalence is inferred.",
    "D74-038 has multiple source-disposition occurrences; the carry obligation selector and immutable prior register row are the authority, not an arbitrarily chosen source path.",
    "No raw source/PDF was reread or rebuilt, and no scholarly prose truth/scientific validity was inferred from schema or prior PASS labels."
  ],
  "findings": {"P0":[],"P1":[],"P2":[]},
  "unknowns": ["Whether Step101 final prose chooses an in-manuscript designated implementation appendix, a separate companion, or both as routing surfaces remains a root-authored boundary decision; selected obligations support either permitted exception without changing their owners."]
}
```

## 후속 Gate와 현재 미결

Step101의 gate는 이 배치 계약과 관련 carry 연결의 완전성·권위 경계에 한정된다.
기존 학술 본문의 전면 수정, manuscript purity PASS, equation freeze, implementation correctness 또는 PDF QA 완료는 아니다.
Phase073은 source/section topology,083은 구현 계약과 예외 경계,087은 실제 분리·조립,
088은 전문 의미 검독,089는 clean LaTeX build와 전 페이지/추출 검증을 각각 수행한다.
Step106은 NOT_YET_EXECUTED, Step107은 NOT_SELECTED; Phase070 이후는107 positive gate 후에만 착수한다.
