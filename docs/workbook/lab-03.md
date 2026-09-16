# លំហាត់ទី៣៖ បម្លែងការប្រើប្រាស់ដីទៅជារ៉ាស្ទ័រ តើអ្វីបាត់?

!!! info "ព័ត៌មានលំហាត់"
    **មេរៀនពាក់ព័ន្ធ៖** [មេរៀនទី៣៖ គំរូទិន្នន័យរ៉ាស្ទ័រ និងការជ្រើសរើសគំរូ](../lessons/lesson-03.md)
    **ការអនុវត្តដោយខ្លួនឯង** · QGIS 3.34 LTR · ប្រហែល ៩០ នាទី

## ស្ថានភាព

ក្រុមការងារមួយត្រូវការផែនទីការប្រើប្រាស់ដីខេត្តកំពង់ឆ្នាំងជា **រ៉ាស្ទ័រ** ដើម្បីប្រើក្នុងគំរូកសិកម្ម។ តើត្រូវជ្រើសទំហំក្រឡាប៉ុន្មាន? ក្រឡាតូច ត្រឹមត្រូវជាង ប៉ុន្តែឯកសារធំ។ ក្រឡាធំ លឿន ប៉ុន្តែព័ត៌មានអ្វីខ្លះបាត់?

## គោលបំណង

- បម្លែងពហុកោណទៅជារ៉ាស្ទ័រ (Rasterize) ដោយប្រើវាលលេខ។
- ប្រៀបធៀបផ្ទៃពីវ៉ិចទ័រ និងពីរ៉ាស្ទ័រនៅទំហំក្រឡាខុសគ្នា។
- ពន្យល់ទំនាក់ទំនងរវាងទំហំក្រឡា ចំនួនក្រឡា និងទំហំឯកសារ។
- សម្រេចថាគំរូណាស័ក្ដិសមសម្រាប់ការងារណា។

## ឯកសារដែលប្រើ

ប្រើសំណុំទិន្នន័យ `Cambodia` ([ឧបសម្ព័ន្ធ ខ](../appendix/b-cambodia-data.md))។ ស្រទាប់ទាំងអស់ប្រើ **EPSG:32648**។

| ស្រទាប់ | ថត | ខ្លឹមសារ |
|---|---|---|
| `Kh_Province_Boundary` | `Admin/` | ព្រំខេត្ត |
| `Kh_Landuse2003` | `Landuse/` | ការប្រើប្រាស់ដី ២០០៣ · វាល `CATEGORY` (៧ ក្រុម) |

## ពិសោធន៍មុនចាប់ផ្ដើម · ៥ នាទី

<div class="sim" data-sim="raster-resolution"></div>

## សកម្មភាពទី១៖ រៀបចំស្រទាប់វ៉ិចទ័រ · ២០ នាទី

1. ទាញខេត្តកំពង់ឆ្នាំង៖ **Extract by expression** `"ProvGis" = 'KH04'` → `kc_province.gpkg`
2. **Clip** `Kh_Landuse2003` ជាមួយ `kc_province` → `kc_landuse.gpkg` (អាចចំណាយពេល ១ ទៅ ២ នាទី)
3. Rasterize ត្រូវការ **វាលលេខ** មិនមែនអក្សរទេ។ បង្កើតវាល Integer `cat_id` ដោយ Field Calculator៖

    ```text
    CASE
      WHEN "CATEGORY" = 'Agricultural lands'    THEN 1
      WHEN "CATEGORY" = 'Forest covers'         THEN 2
      WHEN "CATEGORY" = 'Grasslands'            THEN 3
      WHEN "CATEGORY" = 'Shrublands'            THEN 4
      WHEN "CATEGORY" = 'Water Features'        THEN 5
      WHEN "CATEGORY" = 'Urban, Built-up Areas' THEN 6
      WHEN "CATEGORY" = 'Soils and Rocks'       THEN 7
    END
    ```

4. បង្កើតវាល `area_ha = $area / 10000` ហើយប្រើ **Statistics by categories** (`area_ha` តាម `CATEGORY`) ដើម្បីបានផ្ទៃវ៉ិចទ័រនៃក្រុមនីមួយៗ។ កត់ត្រាក្នុងតារាងខាងក្រោម។

## សកម្មភាពទី២៖ Rasterize នៅ ៣០ ម និង ២៥០ ម · ២០ នាទី

1. ចូល **Raster → Conversion → Rasterize (Vector to Raster)**។
2. កំណត់៖

    | ប៉ារ៉ាម៉ែត្រ | តម្លៃ |
    |---|---|
    | Input layer | `kc_landuse` |
    | Field to use for a burn-in value | `cat_id` |
    | Output raster size units | **Georeferenced units** |
    | Width / Horizontal resolution | `30` |
    | Height / Vertical resolution | `30` |
    | Output extent | Calculate from layer → `kc_landuse` |
    | Assign a specified NoData value | `0` |
    | Output data type | **Byte** |

3. រក្សាទុកជា `kc_lu_30m.tif`។ ធ្វើម្ដងទៀតជាមួយ `250` → `kc_lu_250m.tif`។
4. ពិនិត្យ **Layer Properties → Information**៖ កត់ត្រាចំនួនជួរឈរ (Width) ជួរដេក (Height) និងទំហំឯកសារក្នុង File Explorer។

## សកម្មភាពទី៣៖ វាស់ផ្ទៃពីរ៉ាស្ទ័រ · ២០ នាទី

1. **Processing Toolbox → Raster layer unique values report**៖ Input `kc_lu_30m` → បើកតារាងលទ្ធផល។
2. តារាងមាន `value` `count` និង `m2`។ ផ្ទៃ (ហ.ត) = `m2 / 10000`។
3. ធ្វើដូចគ្នាសម្រាប់ `kc_lu_250m`។
4. បំពេញតារាង៖

    | ក្រុម | វ៉ិចទ័រ (ហ.ត) | ៣០ ម (ហ.ត) | ២៥០ ម (ហ.ត) | ខុសគ្នា ២៥០ ម (%) |
    |---|---:|---:|---:|---:|
    | Agricultural lands | | | | |
    | Forest covers | | | | |
    | Grasslands | | | | |
    | Shrublands | | | | |
    | Water Features | | | | |
    | Urban, Built-up Areas | | | | |
    | Soils and Rocks | | | | |

5. ពង្រីកផែនទីទៅក្រុងកំពង់ឆ្នាំង ហើយប្រៀបធៀបរ៉ាស្ទ័រទាំងពីរជាមួយព្រំវ៉ិចទ័រ។ តើតំបន់ទីក្រុងតូចៗ និងស្ទឹងស្ដើងៗ មើលទៅដូចម្ដេចនៅ ២៥០ ម?

**សំណួរ៖** ហេតុអ្វីផ្ទៃសរុបនៃក្រុមធំៗ នៅជិតផ្ទៃវ៉ិចទ័រ ទោះក្រឡា ២៥០ ម ក៏ដោយ? · ក្រុមណាខុសភាគរយច្រើនជាងគេ ហើយហេតុអ្វី? · ផ្ទៃសរុបត្រឹមត្រូវ មានន័យថាទីតាំងក្រឡានីមួយៗត្រឹមត្រូវឬទេ?

## សកម្មភាពទី៤៖ ជ្រើសរើសគំរូ · ១៥ នាទី

សម្រាប់ការងារនីមួយៗ ជ្រើស «វ៉ិចទ័រ» ឬ «រ៉ាស្ទ័រ» ហើយសរសេរហេតុផលមួយប្រយោគ៖

| ការងារ | គំរូ | ហេតុផល |
|---|---|---|
| ចុះបញ្ជីក្បាលដីស្រែ ដើម្បីចេញប្លង់ | | |
| គណនាជម្រាលពី DEM | | |
| ផែនទីសីតុណ្ហភាពផ្ទៃដីពីផ្កាយរណប | | |
| បណ្ដាញផ្លូវសម្រាប់រកផ្លូវខ្លីបំផុត | | |
| គំរូហានិភ័យទឹកជំនន់ដែលបូកស្រទាប់ ៥ | | |

<div class="match-quiz" data-quiz="lab-02-geometry"></div>

## លទ្ធផលត្រូវប្រគល់

- រ៉ាស្ទ័រ `kc_lu_30m.tif` និង `kc_lu_250m.tif`។
- តារាងប្រៀបធៀបផ្ទៃ និងព័ត៌មានទំហំឯកសារ។
- ចម្លើយសំណួរ និងតារាងជ្រើសរើសគំរូ។

## ពិនិត្យលទ្ធផលដោយខ្លួនឯង

អាចវាយលេខខ្មែរ ឬលេខអារ៉ាប់ ហើយមិនចាំបាច់ដាក់សញ្ញាក្បៀស។ ផ្នែកនេះសម្រាប់ពិនិត្យខ្លួនឯងប៉ុណ្ណោះ។

<div class="self-check" data-min="169000" data-max="171500" data-hint="ត្រូវ Clip ជាមួយព្រំខេត្ត KH04 មុន" markdown>
**១.** ផ្ទៃ Agricultural lands ពីវ៉ិចទ័រក្នុងខេត្តកំពង់ឆ្នាំង (ហ.ត)?
</div>

<div class="self-check" data-min="2640" data-max="2665" data-hint="មើល Layer Properties → Information" markdown>
**២.** រ៉ាស្ទ័រ ៣០ ម មានចំនួនជួរឈរ (Width) ប្រហែលប៉ុន្មាន?
</div>

<div class="self-check" data-min="21000" data-max="22100" data-hint="ផ្ទៃ = count × 250 × 250 ÷ 10000" markdown>
**៣.** ផ្ទៃ Water Features ពីរ៉ាស្ទ័រ ២៥០ ម (ហ.ត)?
</div>

<div class="self-check" data-min="4" data-max="4" markdown>
**៤.** បើកាត់ទំហំក្រឡាពី ៣០ ម មក ១៥ ម ចំនួនក្រឡាកើនប៉ុន្មានដង?
</div>

