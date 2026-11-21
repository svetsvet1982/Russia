# Style pass: from choppy lines to connected speech

## Problem
The dialogue is too choppy. Too many turns are lists of words or chains of 1–3-word sentences, for example «Дождь. Ночь. Мост. Пять минут.» or «Вижу. Двое. Серый.». This reads like a telegram, not like people talking.

## Targets (per episode, measured by `python3 /home/user/Russia/tools/style_stats.py <file>`)
- `frag` ≤ 15%: share of sentences of 1–3 words.
- `avg` ≥ 9.0: average words per sentence.
- `chop` ≤ 3%: share of turns made only of sentences shorter than 5 words.
- Word count (`python3 /home/user/Russia/tools/count_words.py <file>`) must stay within 90–120% of target.

## How to fix (Russian spoken dialogue, natural, idiomatic, with ё)
- Merge chains of short sentences into one or two full spoken sentences. Join them with conjunctions and subordinate clauses (потому что, хотя, если, когда, пока, чтобы, а, но, и, зато, так что, раз уж), with relative clauses (который, где, куда), with participial and adverbial phrases where natural, and with introductory words (по-моему, кстати, видишь ли).
  - Bad: «Дождь. Ночь. Мост поднимут через пять минут. Успеем.»
  - Good: «Дождь, ночь, а мост поднимут через пять минут, так что если не будем стоять, ещё успеем.»
- Replace word lists with real sentences that have a subject and a verb, and in which the speaker reacts to the other person.
- Keep characters' voices (기획서.md §6-3). Ветров is still the most laconic, but laconic means short *answers*, not telegraphese. Keep his dry irony and his habit of answering with a question.
- Radio and operational chatter may stay brisk, but use real radio phrases in full sentences («Первая, я Москва, вижу двоих у моста, иду за ними.»), not bare nouns.
- Deliberate one-word punches are allowed where they land hard, at most about 8 per episode. Examples: a one-word answer at a climax, «Нет.», a name called out.
- Do not add new plot facts. Rephrase and connect; do not invent new events, names, numbers or revelations. Keep everything consistent with `bible/continuity.md`.

## Hard rules (unchanged)
1. Keep the same number of turns, the same numbering, the same speaker for each turn, the same scene breaks, scene headings, header and ending lines. `python3 /home/user/Russia/tools/check_turns.py <file>` must print OK with no WARN.
2. Keep plot, facts, names, dates, times, numbers, who-knows-what and ты/вы usage unchanged.
3. Keep verbatim each episode's final turn and any line the beat sheets (`bible/part*_beats.md`) mark as fixed. Also keep verbatim the ep1 roof sample (turns 96–118) and the ep13 turns 1–10. If a fixed line is choppy, leave it.
4. Never name the embassy's / "other side" country.
5. At most 3 very long turns (>80 words) per episode.

## Method
Read the episode. Rewrite the whole file with the Write tool. Then run all three scripts and iterate until every target is met. Do NOT git commit.
