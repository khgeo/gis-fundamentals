# លំហាត់ទី១៤៖ ជ្រើសទីតាំងសាលាបឋមសិក្សាថ្មី

!!! info "ព័ត៌មានលំហាត់"
    **មេរៀនពាក់ព័ន្ធ៖** [មេរៀនទី១៤៖ ការវិភាគសមស្របភាពពហុលក្ខខណ្ឌ](../lessons/lesson-14.md)
    **ការអនុវត្តដោយខ្លួនឯង** · QGIS 3.34 LTR · ប្រហែល ១១០ នាទី

## ស្ថានភាព

មន្ទីរអប់រំខេត្តកំពង់ឆ្នាំងមានថវិកាសាងសង់សាលាបឋមសិក្សាថ្មី។ ទីតាំងល្អត្រូវ៖ **នៅជិតផ្លូវជាតិ** (ងាយធ្វើដំណើរ) · **នៅឆ្ងាយពីសាលាបឋមសិក្សាដែលមានស្រាប់** (បម្រើតំបន់ខ្វះសាលា) · **មិនលិចទឹក** និង **មិនមែនជាផ្ទៃទឹក**។ អ្នកត្រូវរកតំបន់ដែលសមស្របបំផុត ហើយពិនិត្យថាលទ្ធផលប្រែប្រួលប៉ុណ្ណា ពេលប្ដូរទម្ងន់។

## គោលបំណង

- បែងចែករវាងលក្ខខណ្ឌ (constraint) និងកត្តា (factor)។
- បម្លែងកត្តាឲ្យមានមាត្រដ្ឋានដូចគ្នា ០ ដល់ ១ (standardisation)។
- គណនាផលបូកមានទម្ងន់ (weighted linear combination)។
- ធ្វើការវិភាគភាពរសើប (sensitivity) ចំពោះទម្ងន់។

## ឯកសារដែលប្រើ

ប្រើសំណុំទិន្នន័យ `Cambodia` ([ឧបសម្ព័ន្ធ ខ](../appendix/b-cambodia-data.md))។ ស្រទាប់ទាំងអស់ប្រើ **EPSG:32648**។

| ស្រទាប់ | ថត |
|---|---|
| `Kh_Province_Boundary` | `Admin/` |
| `Kh_Main_Roads_MPWT2014` | `Infrastructure/` |
| `Kh_School` | `School/` |
| `Kh_Landuse2003` `Flood2011` | `Landuse/` `Water/` |

## ពិសោធន៍មុនចាប់ផ្ដើម · ១០ នាទី

<div class="sim" data-sim="mcda"></div>

## សកម្មភាពទី១៖ រៀបចំស្រទាប់ · ១៥ នាទី

1. `kc_province.gpkg` (`"ProvGis" = 'KH04'`)។ **Vector → Geoprocessing Tools → Buffer** ១០ គម → `kc_buf10.gpkg` (តំបន់ពង្រីក ដើម្បីរាប់បញ្ចូលមណ្ឌលសុខភាពខេត្តជិតខាង)។
2. `kc_landuse.gpkg` ពី [លំហាត់ទី៣](lab-03.md) (ឬ Clip `Kh_Landuse2003` ជាមួយ `kc_province` ម្ដងទៀត)។
3. `flood2011_fixed.gpkg` ពី [លំហាត់ទី៨](lab-08.md) → **Clip** ជាមួយ `kc_province` → `kc_flood.gpkg`
4. `kc_water.gpkg`៖ `kc_landuse` ដែល `"CATEGORY" = 'Water Features'`
5. `primary.gpkg`៖ `Kh_School` ដែល `"SCHOOL_TYP" = 'Primary'` (ទូទាំងប្រទេស ដើម្បីរាប់សាលាខេត្តជិតខាង)

## សកម្មភាពទី២៖ រ៉ាស្ទ័រមូលដ្ឋាន · ២០ នាទី

!!! warning "ក្បួនសំខាន់៖ រ៉ាស្ទ័រទាំងអស់ត្រូវតម្រឹមគ្នា"
    Raster Calculator គណនាក្រឡាទល់ក្រឡា។ រ៉ាស្ទ័រគ្រប់ស្រទាប់ត្រូវមាន **CRS ដូចគ្នា ទំហំក្រឡាដូចគ្នា និងវិសាលភាពដូចគ្នា**។ ក្នុងលំហាត់នេះ ពេល Rasterize ត្រូវកំណត់ Output extent = `kc_buf10` និងទំហំក្រឡា `100` ជានិច្ច។ ក្រឡា ១០០ × ១០០ ម = **១ ហិកតា** ដូច្នេះចំនួនក្រឡា = ផ្ទៃជាហិកតា។

1. **Raster → Conversion → Rasterize**៖ Input `kc_province` · A fixed value to burn `1` · Output raster size units **Georeferenced units** · Width/Height `100` · Output extent **Calculate from layer → `kc_buf10`** · Pre-initialize the output image with value `0` · Output data type **Byte** → `prov.tif`
2. **Raster → Conversion → Rasterize**៖ Input `kc_flood` · A fixed value to burn `1` · Output raster size units **Georeferenced units** · Width/Height `100` · Output extent **Calculate from layer → `kc_buf10`** · Pre-initialize the output image with value `0` · Output data type **Byte** → `flood.tif`
3. **Raster → Conversion → Rasterize**៖ Input `kc_water` · A fixed value to burn `1` · Output raster size units **Georeferenced units** · Width/Height `100` · Output extent **Calculate from layer → `kc_buf10`** · Pre-initialize the output image with value `0` · Output data type **Byte** → `water.tif`
4. **Raster → Conversion → Rasterize**៖ Input `Kh_Main_Roads_MPWT2014` · A fixed value to burn `1` · Output raster size units **Georeferenced units** · Width/Height `100` · Output extent **Calculate from layer → `kc_buf10`** · Pre-initialize the output image with value `0` · Output data type **Byte** → `road.tif` · ធីក **Burn all pixels touched** ផង
5. **Raster → Conversion → Rasterize**៖ Input `primary` · A fixed value to burn `1` · Output raster size units **Georeferenced units** · Width/Height `100` · Output extent **Calculate from layer → `kc_buf10`** · Pre-initialize the output image with value `0` · Output data type **Byte** → `school.tif`
6. **Proximity** លើ `road.tif` → `road_dist.tif` និងលើ `school.tif` → `school_dist.tif` (Georeferenced coordinates · Float32)

## សកម្មភាពទី៣៖ បម្លែងកត្តាទៅ ០–១ · ២០ នាទី

**Raster Calculator**៖

| លទ្ធផល | កន្សោម | ន័យ |
|---|---|---|
| `road_s.tif` | `max(0, 1 - "road_dist@1" / 5000)` | ១ នៅលើផ្លូវ ថយចុះដល់ ០ នៅចម្ងាយ ៥ គម |
| `school_s.tif` | `min(1, "school_dist@1" / 3000)` | ០ នៅសាលាស្រាប់ កើនដល់ ១ នៅចម្ងាយ ៣ គមឡើង |
| `ok.tif` | `("prov@1" = 1) AND ("flood@1" = 0) AND ("water@1" = 0)` | ១ = អាចសាងសង់ · ០ = ហាមឃាត់ |

**សំណួរ៖** ហេតុអ្វីកត្តាទាំងពីរត្រូវបម្លែងមក ០–១ មុនបូក? (ជំនួយ៖ ចម្ងាយផ្លូវជាម៉ែត្រ អាចដល់ ២០ ០០០ ឯពិន្ទុគ្មានឯកតា) · តើ ៥ គម និង ៣ គម ជាការសម្រេចចិត្តរបស់នរណា?

## សកម្មភាពទី៤៖ ផលបូកមានទម្ងន់ · ២០ នាទី

1. **Raster Calculator**៖

    ```text
    (0.4 * "road_s@1" + 0.6 * "school_s@1") * "ok@1"
    ```

    → `suit_40_60.tif`

2. ដាក់និមិត្តសញ្ញា Singleband pseudocolor (ក្រហម → បៃតង) ០ ដល់ ១។
3. **Raster Calculator**៖ `"suit_40_60@1" >= 0.8` → `best_40_60.tif` ហើយប្រើ Raster layer unique values report ដើម្បីរាប់ផ្ទៃ។
4. **Raster → Conversion → Polygonize** លើ `best_40_60` → ពហុកោណ → រកតំបន់ធំៗបី ហើយដាក់ចំណុចបេក្ខភាព ៣ ក្នុងស្រទាប់ `candidates.gpkg` (វាល `rank` `reason`)។

## សកម្មភាពទី៥៖ ភាពរសើបនៃទម្ងន់ · ២០ នាទី

1. ធ្វើម្ដងទៀតជាមួយទម្ងន់ ០,៧ (ផ្លូវ) និង ០,៣ (សាលា) → `suit_70_30.tif` និង `best_70_30.tif`
2. **Raster Calculator**៖ `("best_40_60@1" = 1) AND ("best_70_30@1" = 1)` → `best_both.tif`
3. រាប់ផ្ទៃ `best_both` ។ ភាគរយនៃ `best_40_60` ដែលនៅតែល្អ ពេលប្ដូរទម្ងន់?

**សំណួរ៖** ចំណុចបេក្ខភាពរបស់អ្នក នៅតែល្អទាំងពីរសេណារីយ៉ូឬទេ? · បើតំបន់ «ល្អបំផុត» ប្រែប្រួលខ្លាំងតាមទម្ងន់ តើអ្នកត្រូវរាយការណ៍ទៅអ្នកសម្រេចចិត្តដូចម្ដេច?

## សកម្មភាពទី៦៖ ផែនទី និងអនុសាសន៍ · ៥ នាទី

ផែនទី A4 ដែលមាន `suit_40_60` · ចំណុចបេក្ខភាព ៣ · សាលាស្រាប់ · ផ្លូវជាតិ · តារាងទម្ងន់ និងលក្ខខណ្ឌ។ សរសេរអនុសាសន៍ ១ កថាខណ្ឌ ព្រមទាំងកត្តាដែលមិនបានរាប់បញ្ចូល (ដង់ស៊ីតេកុមារ ម្ចាស់ដី ថវិកា)។

## លទ្ធផលត្រូវប្រគល់

- រ៉ាស្ទ័រ `road_s` `school_s` `ok` `suit_40_60` `suit_70_30` `best_both`។
- `candidates.gpkg` ជាមួយ ៣ ចំណុច។
- តារាងផ្ទៃ ផែនទី និងអនុសាសន៍។

## ពិនិត្យលទ្ធផលដោយខ្លួនឯង

អាចវាយលេខខ្មែរ ឬលេខអារ៉ាប់ ហើយមិនចាំបាច់ដាក់សញ្ញាក្បៀស។ ផ្នែកនេះសម្រាប់ពិនិត្យខ្លួនឯងប៉ុណ្ណោះ។

<div class="self-check" data-min="30" data-max="34" data-hint="ភាគច្រើនមកពីតំបន់ជំនន់" markdown>
**១.** ភាគរយនៃខេត្តដែលត្រូវហាមឃាត់ (`ok` = 0 ក្នុងខេត្ត)?
</div>

<div class="self-check" data-min="8000" data-max="11000" data-hint="ចំនួនក្រឡាតម្លៃ ១ = ហិកតា" markdown>
**២.** ផ្ទៃ `best_40_60` (ពិន្ទុ ≥ ០,៨) ប្រហែលប៉ុន្មានហិកតា?
</div>

<div class="self-check" data-min="9000" data-max="12000" markdown>
**៣.** ផ្ទៃ `best_70_30` ប្រហែលប៉ុន្មានហិកតា?
</div>

<div class="self-check" data-min="1" data-max="1" markdown>
**៤.** ទម្ងន់ទាំងអស់ត្រូវបូកបានប៉ុន្មាន?
</div>

