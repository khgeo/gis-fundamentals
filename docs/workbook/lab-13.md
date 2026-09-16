# លំហាត់ទី១៣៖ ពីចំណុចភូមិ ទៅជាផ្ទៃអក្ខរកម្ម

!!! info "ព័ត៌មានលំហាត់"
    **មេរៀនពាក់ព័ន្ធ៖** [មេរៀនទី១៣៖ ផ្ទៃ ទីសណ្ឋាន និងអាំងទែប៉ូឡាស្យុង](../lessons/lesson-13.md)
    **ការអនុវត្តដោយខ្លួនឯង** · QGIS 3.34 LTR · ប្រហែល ១០០ នាទី

## ស្ថានភាព

ជំរឿនឆ្នាំ ២០០៨ ផ្ដល់អត្រាអក្ខរកម្មរបស់ភូមិនីមួយៗ ជាចំណុច។ អង្គការអប់រំមួយចង់បានផែនទីរលោងមួយដែលបង្ហាញលំនាំទូទៅទូទាំងខេត្តកំពង់ឆ្នាំង។ អ្នកនឹងធ្វើអាំងទែប៉ូឡាស្យុង IDW វាស់កំហុសដោយការផ្ទៀងផ្ទាត់ ហើយពិភាក្សាថាតើ «ផ្ទៃអក្ខរកម្ម» មានន័យឬទេ។

## គោលបំណង

- ពិនិត្យស្ថិតិ និងការចែកចាយចំណុចមុនធ្វើអាំងទែប៉ូឡាស្យុង។
- បង្កើតផ្ទៃ IDW ជាមួយស្វ័យគុណខុសៗគ្នា។
- វាស់កំហុសដោយបំបែកចំណុចបណ្ដុះ (training) និងចំណុចពិនិត្យ (test)។
- បង្កើតខ្សែវណ្ឌ (contour) ពីផ្ទៃ ហើយស្គាល់ដែនកំណត់នៃការធ្វើផ្ទៃពីទិន្នន័យសង្គម។

## ឯកសារដែលប្រើ

ប្រើសំណុំទិន្នន័យ `Cambodia` ([ឧបសម្ព័ន្ធ ខ](../appendix/b-cambodia-data.md))។ ស្រទាប់ទាំងអស់ប្រើ **EPSG:32648**។

| ស្រទាប់ | ថត | វាល |
|---|---|---|
| `Census_Village` | `Census_2008/` | `VILL_CODE` `T_LIT15` (អត្រាអក្ខរកម្ម ១៥ ឆ្នាំឡើង %) |
| `Kh_Province_Boundary` | `Admin/` | |

## ពិសោធន៍មុនចាប់ផ្ដើម · ១០ នាទី

<div class="sim" data-sim="idw"></div>

## សកម្មភាពទី១៖ ស្គាល់ទិន្នន័យ · ១៥ នាទី

1. **Extract by expression** លើ `Census_Village`៖ `left("VILL_CODE", 2) = '04'` → `kc_villages.gpkg`
2. **Processing → Basic statistics for fields** លើ `T_LIT15`៖ កត់ត្រា count min max mean median។
3. ដាក់និមិត្តសញ្ញា **Graduated** លើ `T_LIT15` (៥ ថ្នាក់ Quantile)។ សង្កេតលំនាំ៖ ភូមិអក្ខរកម្មទាប ប្រមូលផ្ដុំនៅតំបន់ណា?

**សំណួរ៖** ភូមិនៅរាយប៉ាយស្មើគ្នាឬទេ? តំបន់ណាដែលគ្មានភូមិសោះ ហើយ IDW នឹងធ្វើអ្វីនៅទីនោះ?

## សកម្មភាពទី២៖ IDW · ២០ នាទី

1. **Processing → Interpolation → IDW Interpolation**៖

    | ប៉ារ៉ាម៉ែត្រ | តម្លៃ |
    |---|---|
    | Vector layer | `kc_villages` · Interpolation attribute `T_LIT15` → ចុច **+** |
    | Distance coefficient P | `2` |
    | Extent | Calculate from layer → `kc_province` |
    | Output raster size · Pixel size X/Y | `250` |

    → `lit_idw_p2.tif`

2. **Raster → Extraction → Clip Raster by Mask Layer**៖ Mask `kc_province` → `lit_idw_p2_clip.tif`
3. ធ្វើម្ដងទៀតជាមួយ P = `1` និង P = `4`។ ប្រៀបធៀបផែនទីទាំងបី។
4. ពិនិត្យ **Information** នៃរ៉ាស្ទ័រ៖ តម្លៃ Min Max។

**សំណួរ៖** ហេតុអ្វីតម្លៃ Max នៃផ្ទៃ IDW មិនអាចលើសពីតម្លៃ Max នៃភូមិ? · P តូច និង P ធំ ផ្ដល់រូបរាងខុសគ្នាដូចម្ដេច?

## សកម្មភាពទី៣៖ វាស់កំហុស (Validation) · ២៥ នាទី

1. **Processing → Random extract**៖ Input `kc_villages` · Method **Percentage of selected features** · `20` → `test.gpkg`
2. បង្កើតចំណុចបណ្ដុះ៖ **Select by Location** → Select features from `kc_villages` · where the features **are disjoint** · by comparing to `test` → **Export → Save Selected Features As** → `train.gpkg`។ ពិនិត្យថា ចំនួន `train` + `test` = ចំនួន `kc_villages`។

3. IDW (P = 2, pixel 250) ពី `train` → `lit_train.tif`
4. **Processing → Sample raster values**៖ Input `test` · Raster `lit_train` · prefix `pred_` → `test_pred.gpkg`
5. Field Calculator៖ `abs_err = abs("pred_1" - "T_LIT15")`
6. **Basic statistics for fields** លើ `abs_err` → Mean = MAE (កំហុសដាច់ខាតមធ្យម)។
7. ធ្វើម្ដងទៀតជាមួយ P = 1 និង P = 4 ដោយប្រើ `train` និង `test` ដដែល។

| P | MAE (ពិន្ទុភាគរយ) |
|---|---:|
| ១ | |
| ២ | |
| ៤ | |

**សំណួរ៖** P ណាផ្ដល់ MAE តូចជាងគេ? · ហេតុអ្វីមិនអាចវាស់កំហុសដោយប្រើចំណុចដែលបានប្រើបង្កើតផ្ទៃរួច?

## សកម្មភាពទី៤៖ ខ្សែវណ្ឌ និងការបកស្រាយ · ២០ នាទី

1. **Raster → Extraction → Contour**៖ Input `lit_idw_p2_clip` · Interval `10` → `lit_contour.gpkg` (វាល `ELEV` = តម្លៃអក្ខរកម្ម)។
2. ដាក់ស្លាកលើខ្សែវណ្ឌ ហើយដាក់ `kc_villages` នៅខាងលើ។
3. សរសេរការបកស្រាយ ៥ ទៅ ៨ ប្រយោគ ដែលឆ្លើយ៖ តំបន់ណាអក្ខរកម្មទាប · MAE ប៉ុន្មាន · **ហេតុអ្វីផ្ទៃនេះត្រូវប្រើដោយប្រុងប្រយ័ត្ន** (ជំនួយ៖ អក្ខរកម្មជាលក្ខណៈមនុស្ស មិនមែនជាតម្លៃបន្តនៅគ្រប់ចំណុចលើដីដូចសីតុណ្ហភាពទេ)។

!!! tip "បន្ថែម៖ ទីសណ្ឋានពិតប្រាកដ"
    សំណុំទិន្នន័យវគ្គសិក្សាមិនមាន DEM ទេ។ បើចង់អនុវត្ត Slope Aspect និង Hillshade ទាញយក SRTM ឬ Copernicus DEM ៣០ ម ពីប្រភពក្នុង [ឧបសម្ព័ន្ធ ខ](../appendix/b-cambodia-data.md) សម្រាប់ខេត្តកំពង់ស្ពឺ ហើយប្រើ **Raster → Analysis → Hillshade / Slope**។

<div class="sim" data-sim="hillshade"></div>

## លទ្ធផលត្រូវប្រគល់

- `lit_idw_p1` `p2` `p4` (clip) និង `lit_contour.gpkg`។
- តារាង MAE និង `test_pred.gpkg`។
- ផែនទីផ្ទៃ IDW ជាមួយខ្សែវណ្ឌ និងការបកស្រាយ។

## ពិនិត្យលទ្ធផលដោយខ្លួនឯង

អាចវាយលេខខ្មែរ ឬលេខអារ៉ាប់ ហើយមិនចាំបាច់ដាក់សញ្ញាក្បៀស។ ផ្នែកនេះសម្រាប់ពិនិត្យខ្លួនឯងប៉ុណ្ណោះ។

<div class="self-check" data-min="568" data-max="568" markdown>
**១.** ចំនួនភូមិក្នុង `kc_villages`?
</div>

<div class="self-check" data-min="17.8" data-max="17.9" markdown>
**២.** តម្លៃ `T_LIT15` ទាបជាងគេ?
</div>

<div class="self-check" data-min="74.2" data-max="74.4" markdown>
**៣.** តម្លៃមធ្យម `T_LIT15` (ទសភាគ ១ ខ្ទង់)?
</div>

<div class="self-check" data-min="100" data-max="100" markdown>
**៤.** តម្លៃ Max នៃ `lit_idw_p2.tif` មិនអាចលើសពីប៉ុន្មាន?
</div>

<div class="self-check" data-min="113" data-max="114" data-hint="២០% នៃ ៥៦៨" markdown>
**៥.** បើយក ២០% ជាចំណុចពិនិត្យ តើមានភូមិប៉ុន្មានក្នុង `test`?
</div>

