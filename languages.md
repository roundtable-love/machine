# [ARCHIVE_COMMIT] Machine: Language Register 1.0

```text
Status: DRAFT
UID: MACHINE-LANGUAGES-1.0
Base: Machine 1.0 (MACHINE-1.0)
```

## 1. Coverage Model

The goal of MACHINE-1.0 is universal human access. The ceiling is not ambition —
it is model fidelity. AI-generated transpilation degrades for under-resourced
languages to the point of parity violation, which the spec explicitly prohibits.
A bad translation is worse than no translation.

| Tier | Languages | Coverage | Status  |
|------|-----------|----------|---------|
| 1    | 64        | ~95%     | Current |
| 2    | 200       | ~99%     | Roadmap |
| 3    | Community | Remainder| Open    |

**Tier 3** covers languages that AI models cannot handle with sufficient
fidelity. Community-contributed translations are accepted for these languages
provided they pass a native-speaker parity audit.

## 2. Fidelity Constraints (Normative)

Per §2 of MACHINE-1.0: Zero Leak — logic parity SHALL be maintained across all
transpiled builds.

A transpilation output MUST be rejected if:

- Key terms are untranslated due to model failure.
- RFC 2119 keywords are mistranslated or omitted.
- Structural keywords within code blocks are altered.
- The output fails a native-speaker parity check.

Peer output in non-English languages carries an inherent risk of signal loss due
to the English-native density of Machine IR vocabulary. See §4.2.6 of
MACHINE-1.0.

## 3. Language Register (Normative)

64 languages. Sorted alphabetically by English name.

<!-- prettier-ignore-start -->
| Code  | English          | Native            |
|-------|------------------|-------------------|
| `am`  | Amharic          | አማርኛ              |
| `ar`  | Arabic           | العربية            |
| `az`  | Azerbaijani      | Azərbaycan dili   |
| `bn`  | Bengali          | বাংলা              |
| `my`  | Burmese          | မြန်မာဘာသာ         |
| `ca`  | Catalan          | Català            |
| `ceb` | Cebuano          | Bisaya            |
| `zh`  | Chinese          | 中文               |
| `cs`  | Czech            | Čeština           |
| `da`  | Danish           | Dansk             |
| `nl`  | Dutch            | Nederlands        |
| `en`  | English          | English           |
| `fi`  | Finnish          | Suomi             |
| `fr`  | French           | Français          |
| `de`  | German           | Deutsch           |
| `el`  | Greek            | Ελληνικά          |
| `gu`  | Gujarati         | ગુજરાતી            |
| `ha`  | Hausa            | Hausa             |
| `he`  | Hebrew           | עברית             |
| `hi`  | Hindi            | हिन्दी             |
| `hu`  | Hungarian        | Magyar            |
| `ig`  | Igbo             | Igbo              |
| `id`  | Indonesian       | Bahasa Indonesia  |
| `it`  | Italian          | Italiano          |
| `jam` | Jamaican Creole  | Patwa             |
| `ja`  | Japanese         | 日本語              |
| `jv`  | Javanese         | Basa Jawa         |
| `kn`  | Kannada          | ಕನ್ನಡ              |
| `km`  | Khmer            | ភាសាខ្មែរ           |
| `ko`  | Korean           | 한국어              |
| `ku`  | Kurdish          | Kurdî             |
| `mg`  | Malagasy         | Malagasy          |
| `ms`  | Malay            | Bahasa Melayu     |
| `ml`  | Malayalam        | മലയാളം             |
| `mr`  | Marathi          | मराठी              |
| `ne`  | Nepali           | नेपाली             |
| `no`  | Norwegian        | Norsk             |
| `or`  | Odia             | ଓଡ଼ିଆ              |
| `om`  | Oromo            | Afaan Oromoo      |
| `ps`  | Pashto           | پښتو              |
| `fa`  | Persian          | فارسی             |
| `pl`  | Polish           | Polski            |
| `pt`  | Portuguese       | Português         |
| `pa`  | Punjabi          | ਪੰਜਾਬੀ             |
| `ro`  | Romanian         | Română            |
| `ru`  | Russian          | Русский           |
| `sd`  | Sindhi           | سنڌي              |
| `si`  | Sinhala          | සිංහල             |
| `so`  | Somali           | Soomaali          |
| `es`  | Spanish          | Español           |
| `su`  | Sundanese        | Basa Sunda        |
| `sw`  | Swahili          | Kiswahili         |
| `sv`  | Swedish          | Svenska           |
| `tl`  | Tagalog          | Tagalog           |
| `ta`  | Tamil            | தமிழ்              |
| `te`  | Telugu           | తెలుగు             |
| `th`  | Thai             | ภาษาไทย           |
| `tr`  | Turkish          | Türkçe            |
| `uk`  | Ukrainian        | Українська        |
| `ur`  | Urdu             | اردو              |
| `uz`  | Uzbek            | Oʻzbek tili       |
| `vi`  | Vietnamese       | Tiếng Việt        |
| `yo`  | Yoruba           | Yorùbá            |
| `zu`  | Zulu             | isiZulu           |
<!-- prettier-ignore-end -->

## 4. Rules (Normative)

1. Languages MUST be sorted alphabetically by their English name.
1. ISO 639-1 codes MUST be used where they exist. ISO 639-3 MAY be used for
   languages without a 639-1 code (e.g., `jam`, `ceb`).
1. New languages MUST be added in alphabetical order by English name.
1. `bin/transpile` MUST derive its supported language list from this file.

## 5. Metadata

```text
Language Code: 639-1:en
Regional Variant: 3166-2:GB
Timestamp Standard: 8601
Protocol Class: MACHINE-1.0
```
