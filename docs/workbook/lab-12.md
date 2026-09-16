# លំហាត់ទី១២៖ ស្រែណាខ្លះលិចទឹក ហើយនៅឆ្ងាយពីមណ្ឌលសុខភាព?

!!! info "ព័ត៌មានលំហាត់"
    **មេរៀនពាក់ព័ន្ធ៖** [មេរៀនទី១២៖ ការវិភាគរ៉ាស្ទ័រ និងពីជគណិតផែនទី](../lessons/lesson-12.md)
    **ការអនុវត្តដោយខ្លួនឯង** · QGIS 3.34 LTR · ប្រហែល ១០០ នាទី

## ស្ថានភាព

ក្រសួងកសិកម្មចង់ដឹងថា ស្រែប៉ុន្មានហិកតាក្នុងខេត្តកំពង់ឆ្នាំងលិចក្នុងទឹកជំនន់ឆ្នាំ ២០១១ ហើយស្រុកណានៅឆ្ងាយពីមណ្ឌលសុខភាពជាងគេ។ លំហាត់នេះប្រើ **រ៉ាស្ទ័រ** ដែលបង្កើតចេញពីវ៉ិចទ័រ ដើម្បីអនុវត្តប្រតិបត្តិការក្នុងតំបន់ (local) ជិតខាង/ចម្ងាយ (distance) និងតាមតំបន់ (zonal)។

## គោលបំណង

- Rasterize វ៉ិចទ័រ ឲ្យតម្រឹមគ្នាលើក្រឡាតែមួយ។
- គណនារ៉ាស្ទ័រចម្ងាយ (Proximity)។
- ប្រើ Raster Calculator ជាមួយកន្សោមតក្កវិជ្ជា។
- គណនាស្ថិតិតាមតំបន់ (Zonal statistics)។

## ឯកសារដែលប្រើ

ប្រើសំណុំទិន្នន័យ `Cambodia` ([ឧបសម្ព័ន្ធ ខ](../appendix/b-cambodia-data.md))។ ស្រទាប់ទាំងអស់ប្រើ **EPSG:32648**។

| ស្រទាប់ | ថត |
|---|---|
| `Kh_Province_Boundary` `Kh_District_area` | `Admin/` |
| `Kh_Landuse2003` | `Landuse/` |
| `Flood2011` | `Water/` |
| `Kh_Health_Center` | `Health/` |

## ពិសោធន៍មុនចាប់ផ្ដើម · ១០ នាទី

<div class="sim" data-sim="map-algebra"></div>

## សកម្មភាពទី១៖ រៀបចំវ៉ិចទ័រ · ១៥ នាទី

1. `kc_province.gpkg` (`"ProvGis" = 'KH04'`)។ **Vector → Geoprocessing Tools → Buffer** ១០ គម → `kc_buf10.gpkg` (តំបន់ពង្រីក ដើម្បីរាប់បញ្ចូលមណ្ឌលសុខភាពខេត្តជិតខាង)។
2. `kc_landuse.gpkg` ពី [លំហាត់ទី៣](lab-03.md) (ឬ Clip `Kh_Landuse2003` ជាមួយ `kc_province` ម្ដងទៀត)។
3. `flood2011_fixed.gpkg` ពី [លំហាត់ទី៨](lab-08.md) → **Clip** ជាមួយ `kc_province` → `kc_flood.gpkg`
4. **Extract by expression** លើ `kc_landuse`៖ `"CATEGORY" = 'Agricultural lands'` → `kc_agri.gpkg`

## សកម្មភាពទី២៖ Rasterize · ២០ នាទី

!!! warning "ក្បួនសំខាន់៖ រ៉ាស្ទ័រទាំងអស់ត្រូវតម្រឹមគ្នា"
    Raster Calculator គណនាក្រឡាទល់ក្រឡា។ រ៉ាស្ទ័រគ្រប់ស្រទាប់ត្រូវមាន **CRS ដូចគ្នា ទំហំក្រឡាដូចគ្នា និងវិសាលភាពដូចគ្នា**។ ក្នុងលំហាត់នេះ ពេល Rasterize ត្រូវកំណត់ Output extent = `kc_buf10` និងទំហំក្រឡា `100` ជានិច្ច។ ក្រឡា ១០០ × ១០០ ម = **១ ហិកតា** ដូច្នេះចំនួនក្រឡា = ផ្ទៃជាហិកតា។

1. **Raster → Conversion → Rasterize**៖ Input `kc_province` · A fixed value to burn `1` · Output raster size units **Georeferenced units** · Width/Height `100` · Output extent **Calculate from layer → `kc_buf10`** · Pre-initialize the output image with value `0` · Output data type **Byte** → `prov.tif`
2. **Raster → Conversion → Rasterize**៖ Input `kc_agri` · A fixed value to burn `1` · Output raster size units **Georeferenced units** · Width/Height `100` · Output extent **Calculate from layer → `kc_buf10`** · Pre-initialize the output image with value `0` · Output data type **Byte** → `agri.tif`
3. **Raster → Conversion → Rasterize**៖ Input `kc_flood` · A fixed value to burn `1` · Output raster size units **Georeferenced units** · Width/Height `100` · Output extent **Calculate from layer → `kc_buf10`** · Pre-initialize the output image with value `0` · Output data type **Byte** → `flood.tif`
4. **Raster → Conversion → Rasterize**៖ Input `Kh_Health_Center` · A fixed value to burn `1` · Output raster size units **Georeferenced units** · Width/Height `100` · Output extent **Calculate from layer → `kc_buf10`** · Pre-initialize the output image with value `0` · Output data type **Byte** → `hc.tif`
5. ពិនិត្យ **Layer Properties → Information** នៃរ៉ាស្ទ័រទាំងបួន៖ Width Height និង Extent ត្រូវដូចគ្នាទាំងអស់។

## សកម្មភាពទី៣៖ រ៉ាស្ទ័រចម្ងាយ · ១៥ នាទី

1. **Raster → Analysis → Proximity (Raster Distance)**៖

    | ប៉ារ៉ាម៉ែត្រ | តម្លៃ |
    |---|---|
    | Input layer | `hc.tif` |
    | A list of pixel values to use as target | `1` |
    | Distance units | **Georeferenced coordinates** |
    | Output data type | Float32 |

    → `hc_dist.tif` (ឯកតា ម៉ែត្រ)

2. ដាក់និមិត្តសញ្ញា **Singleband pseudocolor** ហើយប្រើ Identify ចុចលើក្រឡាផ្សេងៗ។

## សកម្មភាពទី៤៖ Raster Calculator · ២០ នាទី

**Raster → Raster Calculator** បង្កើតរ៉ាស្ទ័របី៖

| លទ្ធផល | កន្សោម | អត្ថន័យ |
|---|---|---|
| `agri_flood.tif` | `("agri@1" = 1) AND ("flood@1" = 1)` | ស្រែដែលលិចទឹក |
| `agri_far.tif` | `("agri@1" = 1) AND ("hc_dist@1" > 5000) AND ("prov@1" = 1)` | ស្រែដែលនៅឆ្ងាយពីមណ្ឌលសុខភាពជាង ៥ គម |
| `agri_flood_far.tif` | `("agri_flood@1" = 1) AND ("agri_far@1" = 1)` | ស្រែលិចទឹក ហើយនៅឆ្ងាយ |

បន្ទាប់មក ប្រើ **Raster layer unique values report** លើរ៉ាស្ទ័រនីមួយៗ។ ចំនួនក្រឡាដែលមានតម្លៃ `1` = ផ្ទៃជាហិកតា។

**សំណួរ៖** ហេតុអ្វីកន្សោម `agri_far` ត្រូវមាន `"prov@1" = 1`? · ភាគរយស្រែដែលលិចទឹកប៉ុន្មាន?

## សកម្មភាពទី៥៖ ស្ថិតិតាមតំបន់ · ២០ នាទី

1. **Extract by expression** លើ `Kh_District_area`៖ `"ProvGis" = 'KH04'` → `kc_districts.gpkg`
2. **Processing → Zonal statistics**៖ Raster `hc_dist` · Vector `kc_districts` · Statistics **Mean** និង **Max** · Prefix `hc_` → `kc_districts_dist.gpkg`
3. បង្កើតវាល `mean_km = "hc_mean" / 1000` ហើយតម្រៀប។
4. ធ្វើផែនទី **Graduated** លើ `mean_km`។

**សំណួរ៖** ស្រុកណាឆ្ងាយពីមណ្ឌលសុខភាពជាងគេជាមធ្យម? · ប្រៀបធៀបជាមួយលទ្ធផល [លំហាត់ទី១០](lab-10.md)។ វិធីទាំងពីរ (វ៉ិចទ័រ និងរ៉ាស្ទ័រ) យល់ស្របគ្នាឬទេ?

## លទ្ធផលត្រូវប្រគល់

- រ៉ាស្ទ័រ `prov` `agri` `flood` `hc_dist` `agri_flood` `agri_far` `agri_flood_far`។
- តារាងផ្ទៃ (ហ.ត) និង `kc_districts_dist.gpkg`។
- ផែនទីមួយ និងការបកស្រាយ ៥ ទៅ ៨ ប្រយោគ។

## ពិនិត្យលទ្ធផលដោយខ្លួនឯង

អាចវាយលេខខ្មែរ ឬលេខអារ៉ាប់ ហើយមិនចាំបាច់ដាក់សញ្ញាក្បៀស។ ផ្នែកនេះសម្រាប់ពិនិត្យខ្លួនឯងប៉ុណ្ណោះ។

<div class="self-check" data-min="169000" data-max="171200" markdown>
**១.** ផ្ទៃស្រែ (`agri.tif` = 1) ប៉ុន្មានហិកតា?
</div>

<div class="self-check" data-min="52500" data-max="56000" data-hint="ពិនិត្យថា flood.tif បង្កើតពី flood2011_fixed ដែល Clip រួច" markdown>
**២.** ស្រែដែលលិចទឹក (`agri_flood`) ប៉ុន្មានហិកតា?
</div>

<div class="self-check" data-min="54000" data-max="58000" markdown>
**៣.** ស្រែដែលនៅឆ្ងាយពីមណ្ឌលសុខភាពជាង ៥ គម ប៉ុន្មានហិកតា?
</div>

<div class="self-check" data-answer="Tuek Phos|Tuk Phos|Teuk Phos|ទឹកផុស" markdown>
**៤.** ស្រុកណាមានចម្ងាយមធ្យមទៅមណ្ឌលសុខភាពវែងជាងគេ?
</div>

<div class="self-check" data-min="9.6" data-max="10.4" markdown>
**៥.** ចម្ងាយមធ្យមនៃស្រុកនោះ (គម ទសភាគ ១ ខ្ទង់)?
</div>

