# លំហាត់ទី៥៖ ភ្ជាប់ជំរឿនប្រជាជនទៅព្រំឃុំ

!!! info "ព័ត៌មានលំហាត់"
    **មេរៀនពាក់ព័ន្ធ៖** [មេរៀនទី៥៖ មូលទិន្នន័យ ការភ្ជាប់តារាង និង Field Calculator](../lessons/lesson-05.md)
    **ការអនុវត្តដោយខ្លួនឯង** · QGIS 3.34 LTR · ប្រហែល ៩០ នាទី

## ស្ថានភាព

ព្រំឃុំ `Kh_Commune_area` មានឈ្មោះ និងលេខកូដ ប៉ុន្តែគ្មានប្រជាជន។ ជំរឿនឆ្នាំ ២០០៨ មានប្រជាជន និងអក្ខរកម្ម ប៉ុន្តែលេខកូដមានទម្រង់ខុសគ្នា។ អ្នកត្រូវភ្ជាប់ពួកវា ហើយធ្វើផែនទីដង់ស៊ីតេប្រជាជនខេត្តកំពង់ឆ្នាំង។

## គោលបំណង

- ពិនិត្យវាលភ្ជាប់ និងកែទម្រង់លេខកូដឲ្យដូចគ្នា។
- ភ្ជាប់តារាងតាមគុណលក្ខណៈ (Join) និងពិនិត្យកំណត់ត្រាដែលគ្មានដៃគូ។
- គណនាដង់ស៊ីតេ ដោយប្រើផ្ទៃពីធរណីមាត្រ។
- ជៀសវាងផែនទី choropleth ពីចំនួនដុល។

## ឯកសារដែលប្រើ

ប្រើសំណុំទិន្នន័យ `Cambodia` ([ឧបសម្ព័ន្ធ ខ](../appendix/b-cambodia-data.md))។ ស្រទាប់ទាំងអស់ប្រើ **EPSG:32648**។

| ស្រទាប់ | ថត | វាលសំខាន់ៗ |
|---|---|---|
| `Kh_Commune_area` | `Admin/` | `CommGis` (ឧ. `KH040301`) `COM_NAME` `ProvGis` |
| `Census_Commune` | `Census_2008/` | `COMM_CODE` (ឧ. `040301`) `TOTPOP` `T_LIT15` |

## ពិសោធន៍មុនចាប់ផ្ដើម · ៥ នាទី

<div class="sim" data-sim="join"></div>

## សកម្មភាពទី១៖ រៀបចំស្រទាប់ · ១៥ នាទី

1. **Extract by expression** លើ `Kh_Commune_area`៖ `"ProvGis" = 'KH04'` → `kc_communes.gpkg` · កត់ត្រាចំនួនឃុំ។
2. បើក Attribute Table នៃ `kc_communes` និង `Census_Commune`។ ប្រៀបធៀបតម្លៃ `CommGis` និង `COMM_CODE`។ តើខុសគ្នាត្រង់ណា?
3. ក្នុង `Census_Commune` (បើក Toggle editing) បង្កើតវាលអក្សរ `join_code` ប្រវែង ៨៖

    ```text
    'KH' || "COMM_CODE"
    ```

    រក្សាទុកការកែ។

## សកម្មភាពទី២៖ ភ្ជាប់តារាង · ២០ នាទី

1. **Layer Properties** នៃ `kc_communes` → **Joins** → ចុច **+**។
2. កំណត់៖

    | ប៉ារ៉ាម៉ែត្រ | តម្លៃ |
    |---|---|
    | Join layer | `Census_Commune` |
    | Join field | `join_code` |
    | Target field | `CommGis` |
    | Joined fields | `TOTPOP` `T_LIT15` |
    | Custom field name prefix | `c08_` |

3. បើក Attribute Table នៃ `kc_communes`។ ប្រើ Select by expression៖ `"c08_TOTPOP" IS NULL` ដើម្បីរាប់ឃុំដែលគ្មានដៃគូ។
4. Join ក្នុង Layer Properties ជាការភ្ជាប់ **បណ្ដោះអាសន្ន**។ ដើម្បីរក្សាទុកជាអចិន្ត្រៃយ៍ ចុចស្ដាំ → **Export → Save Features As** → `kc_communes_pop.gpkg`

!!! tip "ពេលភ្ជាប់មិនបាន"
    ពិនិត្យ៖ ប្រភេទវាលដូចគ្នាឬទេ (អក្សរ និងលេខ) · មានដកឃ្លានៅខាងមុខ ឬខាងក្រោយឬទេ · លេខ ០ ខាងមុខបាត់ឬទេ · ឆ្នាំនៃព្រំដែន និងឆ្នាំនៃតារាងដូចគ្នាឬទេ។

## សកម្មភាពទី៣៖ Field Calculator · ២០ នាទី

នៅក្នុង `kc_communes_pop` បង្កើតវាលទាំងនេះ៖

| វាល | ប្រភេទ | កន្សោម |
|---|---|---|
| `area_km2` | Decimal | `$area / 1000000` |
| `dens` | Decimal | `"c08_TOTPOP" / "area_km2"` |
| `dens_class` | Text | `CASE WHEN "dens" < 100 THEN 'ទាប' WHEN "dens" < 500 THEN 'មធ្យម' ELSE 'ខ្ពស់' END` |

**សំណួរ៖** ហេតុអ្វីមិនប្រើផ្ទៃពីវាល `AREA` ក្នុងតារាងជំរឿន? · ឃុំណាមានដង់ស៊ីតេខ្ពស់ជាងគេ?

## សកម្មភាពទី៤៖ ផែនទីពីរ ប្រៀបធៀប · ២០ នាទី

1. ចម្លងស្រទាប់ `kc_communes_pop` (Duplicate Layer)។
2. ស្រទាប់ទី១៖ **Graduated** លើ `c08_TOTPOP` (ចំនួនដុល)។ ស្រទាប់ទី២៖ **Graduated** លើ `dens`។ ប្រើ ៥ ថ្នាក់ **Quantile** ទាំងពីរ។
3. បិទ/បើកស្រទាប់ទាំងពីរ ហើយប្រៀបធៀប។

**សំណួរ៖** ឃុំណាដែលមើលទៅ «សំខាន់» ក្នុងផែនទីចំនួនដុល ដោយសារតែមានផ្ទៃធំ? · ផែនទីមួយណាឆ្លើយសំណួរ «តើមនុស្សរស់នៅក្រាស់នៅឯណា?» បានត្រឹមត្រូវ?

## លទ្ធផលត្រូវប្រគល់

- `kc_communes_pop.gpkg` ជាមួយវាល `c08_TOTPOP` `T_LIT15` `area_km2` `dens` `dens_class`។
- ផែនទីពីរ (ចំនួនដុល និងដង់ស៊ីតេ) និងការពន្យល់ ៣ ទៅ ៥ ប្រយោគ។

## ពិនិត្យលទ្ធផលដោយខ្លួនឯង

អាចវាយលេខខ្មែរ ឬលេខអារ៉ាប់ ហើយមិនចាំបាច់ដាក់សញ្ញាក្បៀស។ ផ្នែកនេះសម្រាប់ពិនិត្យខ្លួនឯងប៉ុណ្ណោះ។

<div class="self-check" data-min="69" data-max="69" markdown>
**១.** ខេត្តកំពង់ឆ្នាំងមានឃុំ សង្កាត់ប៉ុន្មានក្នុង `Kh_Commune_area`?
</div>

<div class="self-check" data-min="0" data-max="0" data-hint="KH040301 ≠ 040301" markdown>
**២.** បើភ្ជាប់ `CommGis` = `COMM_CODE` ដោយផ្ទាល់ (គ្មាន 'KH') តើត្រូវគ្នាប៉ុន្មាន?
</div>

<div class="self-check" data-min="0" data-max="0" markdown>
**៣.** ក្រោយប្រើ `join_code` តើមានឃុំប៉ុន្មានដែលគ្មានដៃគូ?
</div>

<div class="self-check" data-answer="B'er|Ber|Ph'er|Pher|B er|ប្អេរ" data-hint="តម្រៀបតាម dens ពីធំទៅតូច" markdown>
**៤.** ឃុំណាមានដង់ស៊ីតេប្រជាជនខ្ពស់ជាងគេ (ឈ្មោះឡាតាំង)?
</div>

<div class="self-check" data-answer="Phlov Tuk|Phlov Touk|ផ្លូវទូក" data-hint="តម្រៀបតាម c08_T_LIT15" markdown>
**៥.** ឃុំណាមានអត្រាអក្ខរកម្មទាបជាងគេ?
</div>

