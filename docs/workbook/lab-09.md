# លំហាត់ទី៩៖ សួរទិន្នន័យ៖ សាលាណាខ្លះប្រឈមទឹកជំនន់?

!!! info "ព័ត៌មានលំហាត់"
    **មេរៀនពាក់ព័ន្ធ៖** [មេរៀនទី៩៖ សំណួរតាមគុណលក្ខណៈ និងតាមលំហ](../lessons/lesson-09.md)
    **ការអនុវត្តដោយខ្លួនឯង** · QGIS 3.34 LTR · ប្រហែល ៩០ នាទី

## ស្ថានភាព

ក្រោយទឹកជំនន់ឆ្នាំ ២០១១ មន្ទីរអប់រំខេត្តកំពង់ឆ្នាំងចង់ដឹង៖ សាលាណាខ្លះស្ថិតក្នុងតំបន់លិចទឹក សាលាណានៅជិតផ្លូវជាតិ (ងាយជម្លៀស) និងឃុំណាខ្លះនៅជាប់សង្កាត់ខ្សាម (ទីរួមខេត្ត)។ អ្នកត្រូវឆ្លើយដោយប្រើសំណួរ **តាមគុណលក្ខណៈ** និង **តាមលំហ**។

## គោលបំណង

- សរសេរ Select by expression ដែលមានលក្ខខណ្ឌច្រើន។
- ជ្រើសរើសតាមទីតាំងដោយប្រើ within intersect touches និង distance។
- រួមបញ្ចូលសំណួរតាមគុណលក្ខណៈ និងតាមលំហ ក្នុងលំដាប់ត្រឹមត្រូវ។
- បែងចែករវាងលទ្ធផលពីគុណលក្ខណៈ និងលទ្ធផលពីទីតាំង។

## ឯកសារដែលប្រើ

ប្រើសំណុំទិន្នន័យ `Cambodia` ([ឧបសម្ព័ន្ធ ខ](../appendix/b-cambodia-data.md))។ ស្រទាប់ទាំងអស់ប្រើ **EPSG:32648**។

| ស្រទាប់ | ថត |
|---|---|
| `Kh_Province_Boundary` `Kh_Commune_area` | `Admin/` |
| `Kh_School` | `School/` |
| `Census_Village` | `Census_2008/` |
| `Flood2011` | `Water/` |
| `Kh_Main_Roads_MPWT2014` | `Infrastructure/` |

## ពិសោធន៍មុនចាប់ផ្ដើម · ១០ នាទី

<div class="sim" data-sim="predicates"></div>

<div class="match-quiz" data-quiz="l09-queries"></div>

## សកម្មភាពទី១៖ រៀបចំ · ១០ នាទី

1. `kc_province.gpkg` (`"ProvGis" = 'KH04'`) និង `kc_communes.gpkg` (`"ProvGis" = 'KH04'`)។
2. **Fix geometries** លើ `Flood2011` → `flood2011_fixed.gpkg` (មើល [លំហាត់ទី៨](lab-08.md))។
3. **Extract by location**៖ `Kh_School` **are within** `kc_province` → `kc_schools.gpkg`

## សកម្មភាពទី២៖ សំណួរតាមគុណលក្ខណៈ · ១៥ នាទី

1. ភូមិធំ៖ `Census_Village` ដោយ `left("VILL_CODE", 2) = '04' AND "TOTPOP" > 3000`
2. សាលាបឋមសិក្សាជនបទ៖ `kc_schools` ដោយ `"SCHOOL_TYP" = 'Primary' AND "Location" = 'Rural'`
3. សាលាដែលឈ្មោះមានពាក្យ «Chrey»៖ `"SCHOOL_NAM" ILIKE '%chrey%'`

**សំណួរ៖** `LIKE` និង `ILIKE` ខុសគ្នាដូចម្ដេច? · `%` មានន័យអ្វី?

## សកម្មភាពទី៣៖ សំណួរតាមលំហ · ២៥ នាទី

| សំណួរ | ឧបករណ៍ | ការកំណត់ |
|---|---|---|
| ក. សាលាណាខ្លះនៅក្នុងតំបន់ជំនន់ ២០១១? | Select by Location | `kc_schools` **are within** `flood2011_fixed` |
| ខ. សាលាណាខ្លះនៅក្នុងចម្ងាយ ១ គម ពីផ្លូវជាតិ? | **Select within distance** | `kc_schools` · `Kh_Main_Roads_MPWT2014` · 1000 ម |
| គ. ឃុំណាខ្លះប៉ះព្រំសង្កាត់ខ្សាម? | Select by Location | `kc_communes` **touch** សង្កាត់ `KH040304` (ជ្រើសខ្សាមមុន ហើយធីក Selected features only) |
| ឃ. ដូចសំណួរ គ ប៉ុន្តែប្រើ **intersect** | Select by Location | ដូចខាងលើ ប្ដូរ touch → intersect |

កត់ត្រាចំនួនលទ្ធផលនីមួយៗ។

**សំណួរ៖** ហេតុអ្វីសំណួរ ឃ មានលទ្ធផលច្រើនជាងសំណួរ គ មួយ?

## សកម្មភាពទី៤៖ រួមបញ្ចូលគុណលក្ខណៈ និងលំហ · ២០ នាទី

**សំណួរ៖** សាលាបឋមសិក្សាណាខ្លះនៅក្នុងតំបន់ជំនន់ ២០១១?

1. ធ្វើសំណួរ ក ម្ដងទៀត (សាលាក្នុងជំនន់)។
2. ក្នុង Attribute Table ប្រើ Select by expression `"SCHOOL_TYP" = 'Primary'` ជាមួយ **Filter current selection** (ជម្រើសនៅខាងក្រោមប៊ូតុង Select Features)។
3. រក្សាទុកលទ្ធផលជា `kc_primary_flood.gpkg`
4. **Statistics by categories** តាម `DISTRICT` ដើម្បីដឹងស្រុកដែលមានសាលាប្រឈមច្រើនជាងគេ។

!!! warning "Modify current selection"
    Select by Location មានជម្រើស៖ **creating new selection** · **adding to** · **removing from** · **selecting within current selection**។ ភ្លេចប្ដូរជម្រើស គឺជាមូលហេតុទូទៅដែលលទ្ធផលខុស។

## សកម្មភាពទី៥៖ គុណលក្ខណៈ ទល់នឹង ទីតាំង · ១០ នាទី

1. រាប់ `Kh_School` ដែល `"PROVINCE" = 'Kampong Chhnang'` (តាមគុណលក្ខណៈ)។
2. ប្រៀបធៀបជាមួយចំនួនក្នុង `kc_schools` (តាមទីតាំង)។
3. ពន្យល់ភាពខុសគ្នា។

## លទ្ធផលត្រូវប្រគល់

- តារាងចំនួនលទ្ធផលនៃសំណួរទាំងអស់ ជាមួយកន្សោម ឬការកំណត់ដែលបានប្រើ។
- `kc_primary_flood.gpkg` និងតារាងតាមស្រុក។
- ផែនទីមួយបង្ហាញសាលាក្នុងជំនន់ និងផ្លូវជាតិ។

## ពិនិត្យលទ្ធផលដោយខ្លួនឯង

អាចវាយលេខខ្មែរ ឬលេខអារ៉ាប់ ហើយមិនចាំបាច់ដាក់សញ្ញាក្បៀស។ ផ្នែកនេះសម្រាប់ពិនិត្យខ្លួនឯងប៉ុណ្ណោះ។

<div class="self-check" data-min="6" data-max="6" markdown>
**១.** ភូមិក្នុងខេត្តកំពង់ឆ្នាំងដែលមានប្រជាជនលើស ៣ ០០០ នាក់?
</div>

<div class="self-check" data-min="78" data-max="82" data-hint="ត្រូវប្រើ flood2011_fixed" markdown>
**២.** សាលាទាំងអស់ក្នុងតំបន់ជំនន់ ២០១១ (សំណួរ ក)?
</div>

<div class="self-check" data-min="117" data-max="121" markdown>
**៣.** សាលាក្នុងចម្ងាយ ១ គម ពីផ្លូវជាតិ (សំណួរ ខ)?
</div>

<div class="self-check" data-min="4" data-max="4" markdown>
**៤.** ឃុំដែល touch សង្កាត់ខ្សាម (សំណួរ គ)?
</div>

<div class="self-check" data-min="63" data-max="67" markdown>
**៥.** សាលាបឋមសិក្សាក្នុងតំបន់ជំនន់?
</div>

<div class="self-check" data-min="415" data-max="415" markdown>
**៦.** សាលាក្នុងខេត្តតាមទីតាំង (`kc_schools`)?
</div>

