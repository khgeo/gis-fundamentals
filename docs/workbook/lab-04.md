# លំហាត់ទី៤៖ សាលារៀនខេត្តកំពង់ឆ្នាំងក្នុងតារាងគុណលក្ខណៈ

!!! info "ព័ត៌មានលំហាត់"
    **មេរៀនពាក់ព័ន្ធ៖** [មេរៀនទី៤៖ គុណលក្ខណៈ និងតារាងទិន្នន័យ](../lessons/lesson-04.md)
    **ការអនុវត្តដោយខ្លួនឯង** · QGIS 3.34 LTR · ប្រហែល ៨០ នាទី

## ស្ថានភាព

មន្ទីរអប់រំខេត្តសុំតារាងសង្ខេបសាលារៀនតាមប្រភេទ និងតាមស្រុក។ អ្នកមិនចាំបាច់គូរផែនទីទេ ប៉ុន្តែត្រូវស្គាល់តារាងគុណលក្ខណៈឲ្យច្បាស់៖ ប្រភេទវាល ការជ្រើសរើស ការតម្រៀប និងស្ថិតិ។

## គោលបំណង

- អានរចនាសម្ព័ន្ធតារាង៖ វាល ប្រភេទវាល និងកំណត់ត្រា។
- ប្រើ Select by expression និងកន្សោមលក្ខខណ្ឌ។
- គណនាស្ថិតិ និងតារាងសង្ខេបតាមប្រភេទ។
- រកកំហុសប្រភេទវាលដែលប៉ះពាល់លេខកូដ។

## ឯកសារដែលប្រើ

ប្រើសំណុំទិន្នន័យ `Cambodia` ([ឧបសម្ព័ន្ធ ខ](../appendix/b-cambodia-data.md))។ ស្រទាប់ទាំងអស់ប្រើ **EPSG:32648**។

| ស្រទាប់ | ថត | វាលសំខាន់ៗ |
|---|---|---|
| `Kh_School` | `School/` | `SCHOOL_COD` `SCHOOL_NAM` `SCHOOL_TYP` `Location` `PROVINCE` `DISTRICT` |

## ពិសោធន៍មុនចាប់ផ្ដើម · ១០ នាទី

<div class="sim" data-sim="field-types"></div>

<div class="match-quiz" data-quiz="l04-scales"></div>

## សកម្មភាពទី១៖ ស្គាល់រចនាសម្ព័ន្ធតារាង · ១៥ នាទី

1. បន្ថែម `Kh_School` ហើយបើក **Layer Properties → Fields**។
2. បំពេញតារាង៖

    | វាល | ប្រភេទ (Type) | ប្រវែង | កម្រិតរង្វាស់ (Nominal/Ordinal/Interval/Ratio) |
    |---|---|---|---|
    | `SCHOOL_COD` | | | |
    | `SCHOOL_TYP` | | | |
    | `Location` | | | |
    | `PROVINCE` | | | |

3. បើក Attribute Table ហើយមើលតម្លៃ `SCHOOL_COD` មួយចំនួន។

**សំណួរ៖** `SCHOOL_COD` រក្សាទុកជាប្រភេទអ្វី? ហេតុអ្វីនេះជាបញ្ហាសម្រាប់លេខកូដ? (ជំនួយ៖ សាកល្បងលេខ `020404` ក្នុងពិសោធន៍ខាងលើ)

## សកម្មភាពទី២៖ ជ្រើសរើសដោយកន្សោម · ២០ នាទី

1. ក្នុង Attribute Table ចុច **Select features using an expression** (ε)។
2. ជ្រើសសាលារៀនក្នុងខេត្តកំពង់ឆ្នាំង៖

    ```text
    "PROVINCE" = 'Kampong Chhnang'
    ```

    កត់ត្រាចំនួនដែលបានជ្រើស។ ចុច **Show Selected Features** នៅខាងក្រោមតារាង។

3. ជ្រើសតែសាលាបឋមសិក្សាជនបទក្នុងខេត្តនេះ៖

    ```text
    "PROVINCE" = 'Kampong Chhnang'
    AND "SCHOOL_TYP" = 'Primary'
    AND "Location" = 'Rural'
    ```

4. សាកល្បងកន្សោមខុសៗ ហើយសង្កេតសារកំហុស៖ `"PROVINCE" = "Kampong Chhnang"` (សញ្ញាសម្រង់ពីរជាន់) · `"PROVINCE" = 'kampong chhnang'` (អក្សរតូច)។

!!! warning "សញ្ញាសម្រង់ពីរប្រភេទ"
    ក្នុង QGIS `"ឈ្មោះវាល"` ប្រើសញ្ញាសម្រង់ពីរជាន់ ឯ `'តម្លៃអក្សរ'` ប្រើសញ្ញាសម្រង់មួយជាន់។ ការប្រៀបធៀបអក្សរ **ប្រកាន់អក្សរធំតូច**។

## សកម្មភាពទី៣៖ តារាងសង្ខេប · ២០ នាទី

1. ជ្រើសសាលារៀនខេត្តកំពង់ឆ្នាំងម្ដងទៀត ហើយ **Export → Save Selected Features As** → `kc_schools.gpkg`
2. **Processing → Statistics by categories**៖ Input `kc_schools` · Field to calculate statistics on៖ ទុកទទេ · Field(s) with categories៖ `SCHOOL_TYP` → បានចំនួនតាមប្រភេទ។
3. ធ្វើម្ដងទៀតដោយប្រើ `DISTRICT` និង `SCHOOL_TYP` ទាំងពីរ ដើម្បីបានតារាងពីរវិមាត្រ។
4. ក្នុង Attribute Table ចុចចំណងជើង `DISTRICT` ដើម្បីតម្រៀប ហើយពិនិត្យថាឈ្មោះស្រុកសរសេរស៊ីគ្នាឬទេ។

**សំណួរ៖** តើស្រុកណាមានសាលារៀនច្រើនជាងគេ? · ភាគរយសាលាជនបទប៉ុន្មាន?

## សកម្មភាពទី៤៖ បង្កើតវាលថ្មី · ១៥ នាទី

1. បើក **Toggle editing** លើ `kc_schools`។
2. ក្នុង Field Calculator បង្កើតវាលអក្សរ `code_txt` ប្រវែង ១០៖

    ```text
    lpad(to_string(to_int("SCHOOL_COD")), 10, '0')
    ```

3. ប្រៀបធៀប `SCHOOL_COD` និង `code_txt` ក្នុងតារាង។ រក្សាទុក ហើយបិទការកែ។

## លទ្ធផលត្រូវប្រគល់

- តារាងរចនាសម្ព័ន្ធវាល។
- `kc_schools.gpkg` ជាមួយវាល `code_txt`។
- តារាងសង្ខេបតាមប្រភេទ និងតាមស្រុក។
- ចម្លើយសំណួរ។

## ពិនិត្យលទ្ធផលដោយខ្លួនឯង

អាចវាយលេខខ្មែរ ឬលេខអារ៉ាប់ ហើយមិនចាំបាច់ដាក់សញ្ញាក្បៀស។ ផ្នែកនេះសម្រាប់ពិនិត្យខ្លួនឯងប៉ុណ្ណោះ។

<div class="self-check" data-min="416" data-max="416" markdown>
**១.** សាលារៀនដែល `PROVINCE` = 'Kampong Chhnang' មានប៉ុន្មាន?
</div>

<div class="self-check" data-min="263" data-max="264" data-hint="ពិនិត្យអក្ខរាវិរុទ្ធ 'Primary'" markdown>
**២.** សាលាបឋមសិក្សា (Primary) ក្នុងខេត្តនេះមានប៉ុន្មាន?
</div>

<div class="self-check" data-min="14" data-max="14" markdown>
**៣.** សាលា Lycee G7-12 មានប៉ុន្មាន?
</div>

<div class="self-check" data-answer="Real|Double|Decimal|Decimal number|float|double precision|real" markdown>
**៤.** វាល `SCHOOL_COD` ជាប្រភេទអ្វី?
</div>

