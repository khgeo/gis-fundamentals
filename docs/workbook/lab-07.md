# លំហាត់ទី៧៖ ធ្វើឲ្យផែនទីក្រដាសមានទីតាំង

!!! info "ព័ត៌មានលំហាត់"
    **មេរៀនពាក់ព័ន្ធ៖** [មេរៀនទី៧៖ ការបំប្លែងទៅឌីជីថល និង Georeferencing](../lessons/lesson-07.md)
    **ការអនុវត្តដោយខ្លួនឯង** · QGIS 3.34 LTR · ប្រហែល ១០០ នាទី

## ស្ថានភាព

ការិយាល័យស្រុកមានផែនទីក្រដាសចាស់នៃក្រុងកំពង់ឆ្នាំង ដែលបានស្កេនជារូបភាព JPG។ រូបភាពមិនមាន CRS ហើយរៀងខ្លួនបន្តិចពេលស្កេន។ អ្នកត្រូវដាក់វាឲ្យត្រូវទីតាំង (Georeference) ហើយគូរផ្លូវជាតិឡើងវិញជាវ៉ិចទ័រ។

## គោលបំណង

- ជ្រើស និងបញ្ចូលចំណុចបញ្ជា (GCP) ពីក្រឡាកូអរដោនេលើផែនទី។
- ជ្រើសប្រភេទការបំប្លែង ហើយបកស្រាយកំហុស RMS។
- គូរ (digitize) បន្ទាត់ និងពហុកោណ ដោយប្រើ Snapping។
- ប្រៀបធៀបលទ្ធផលជាមួយទិន្នន័យដែលមានស្រាប់។

## ឯកសារដែលប្រើ

[:material-download: ទាញយកផែនទីស្កេន](../assets/data/lab-07/kampong_chhnang_scan.jpg){ .md-button } (១ ១៣៩ × ១ ១៣៩ ភីកសែល · ១៨៧ KB)

ចុចស្ដាំលើប៊ូតុង → **Save link as** ដើម្បីរក្សាទុកក្នុងថត `lab-07`។

| ស្រទាប់ | ថត | ប្រើសម្រាប់ |
|---|---|---|
| `kampong_chhnang_scan.jpg` | ទាញយកខាងលើ | ផែនទីក្រដាសដែលត្រូវ Georeference |
| `Kh_All_Roads_MPWT2014` | `Infrastructure/` | ប្រៀបធៀបផ្លូវដែលគូរ |
| `Kh_Lake_n_Mekong` | `Water/` | ប្រៀបធៀបទន្លេ |

ផែនទីមានសញ្ញាបូក (+) ជាក្រឡាកូអរដោនេ UTM Zone 48N រៀងរាល់ ២ គីឡូម៉ែត្រ។ ស្លាក `464E 1356N` មានន័យថា **E = 464 000 ម · N = 1 356 000 ម**។

## ពិសោធន៍មុនចាប់ផ្ដើម · ១០ នាទី

<div class="sim" data-sim="georef"></div>

## សកម្មភាពទី១៖ បញ្ចូលចំណុចបញ្ជា · ៣០ នាទី

1. កំណត់ CRS គម្រោងជា **EPSG:32648** (ជ្រុងខាងក្រោមស្ដាំ)។ បន្ថែម `Kh_Lake_n_Mekong` ដើម្បីជាឯកសារយោង។
2. ចូល **Layer → Georeferencer** → **Open Raster** → ជ្រើស `kampong_chhnang_scan.jpg`។ បើ QGIS សួរ CRS សម្រាប់រូបភាព ចុច Cancel។
3. ពង្រីកទៅសញ្ញាបូក `462E 1360N`។ ចុច **Add Point** ហើយចុចចំកណ្ដាលសញ្ញាបូក។ វាយ៖ X (East) = `462000` · Y (North) = `1360000` · CRS **EPSG:32648**។
4. បញ្ចូល GCP យ៉ាងតិច **៨** ដែលរាយពេញផែនទី (ជ្រុងទាំងបួន និងកណ្ដាល)។
5. **Settings → Transformation Settings**៖

    | ប៉ារ៉ាម៉ែត្រ | តម្លៃ |
    |---|---|
    | Transformation type | **Polynomial 1** |
    | Resampling method | Nearest neighbour |
    | Target CRS | EPSG:32648 |
    | Output raster | `kampong_chhnang_georef.tif` |
    | Load in project when done | ✓ |

6. មើលតារាង GCP ខាងក្រោម៖ ជួរ **Residual (pixels)** និង RMS នៅរបារខាងក្រោម។ GCP ដែលមានកំហុសធំជាងគេ ត្រូវពិនិត្យ ហើយចុចម្ដងទៀត ឬលុប។
7. ចុច **Start Georeferencing** (▶)។ រក្សាទុក GCP ជា `lab07.points` ផង។

!!! tip "RMS ល្អ គឺប៉ុន្មាន?"
    ផែនទីនេះ ១ ភីកសែល ≈ ១០ ម៉ែត្រ។ RMS ក្រោម **១ ភីកសែល** គឺល្អ។ ប៉ុន្តែ RMS ទាប មិនធានាថាផែនទីត្រឹមត្រូវទេ បើ GCP ទាំងអស់ប្រមូលផ្ដុំនៅកន្លែងតែមួយ។

## សកម្មភាពទី២៖ ពិនិត្យលទ្ធផល · ១៥ នាទី

1. កំណត់ភាពថ្លា (Opacity) របស់ `kampong_chhnang_georef` ៦០%។
2. ដាក់ `Kh_Lake_n_Mekong` និង `Kh_All_Roads_MPWT2014` នៅខាងលើ។ ពិនិត្យថាទន្លេ និងផ្លូវជាតិត្រួតគ្នាឬទេ។
3. ប្រើ **Measure Line** វាស់ចម្ងាយពីផ្លូវក្នុងរូបភាព ទៅផ្លូវក្នុងស្រទាប់វ៉ិចទ័រ នៅ ៣ កន្លែងផ្សេងគ្នា។

**សំណួរ៖** កំហុសធំជាងគេនៅតំបន់ណា? តើនៅទីនោះមាន GCP ឬទេ?

## សកម្មភាពទី៣៖ គូរផ្លូវជាតិឡើងវិញ · ៣០ នាទី

1. បង្កើតស្រទាប់ GeoPackage `digitized.gpkg` · Layer `main_road` · **LineString** · EPSG:32648 · វាល `name` (Text)។
2. បង្កើតស្រទាប់ទីពីរ `river_island` · **Polygon** · វាល `name`។
3. **Project → Snapping Options**៖ បើក Snapping · Vertex · ១២ ភីកសែល · សម្រាប់ស្រទាប់ `main_road` និង `river_island`។
4. គូរផ្លូវជាតិពណ៌ក្រហមទាំងពីរ ដែលឆ្លងកាត់ផែនទី។ ដាក់ចំណុចកំពូលនៅរាល់ពេលផ្លូវបត់។
5. គូរកោះមួយក្នុងទន្លេជាពហុកោណ។
6. ប្រើ **Vector → Geometry Tools → Check Validity** លើ `river_island`។
7. គណនាប្រវែងផ្លូវ `$length` និងផ្ទៃកោះ `$area / 10000`។

<div class="sim" data-sim="simplify"></div>

**សំណួរ៖** ប្រវែងផ្លូវដែលអ្នកគូរ វែងជាង ឬខ្លីជាងផ្លូវក្នុង `Kh_All_Roads_MPWT2014`? ហេតុអ្វី? · ចំណុចកំពូលច្រើនពេក ឬតិចពេក មានផលអ្វី?

## លទ្ធផលត្រូវប្រគល់

- `kampong_chhnang_georef.tif` និង `lab07.points`។
- រូបថតអេក្រង់តារាង GCP ដែលមាន RMS។
- `digitized.gpkg` ជាមួយ `main_road` និង `river_island`។
- ចម្លើយសំណួរ។

## ពិនិត្យលទ្ធផលដោយខ្លួនឯង

អាចវាយលេខខ្មែរ ឬលេខអារ៉ាប់ ហើយមិនចាំបាច់ដាក់សញ្ញាក្បៀស។ ផ្នែកនេះសម្រាប់ពិនិត្យខ្លួនឯងប៉ុណ្ណោះ។

<div class="self-check" data-min="16" data-max="16" markdown>
**១.** ផែនទីស្កេនមានសញ្ញាបូក (GCP ដែលអាចប្រើ) ប៉ុន្មាន?
</div>

<div class="self-check" data-min="3" data-max="3" markdown>
**២.** Polynomial 1 ត្រូវការ GCP យ៉ាងតិចប៉ុន្មាន?
</div>

<div class="self-check" data-min="6" data-max="6" markdown>
**៣.** Polynomial 2 ត្រូវការ GCP យ៉ាងតិចប៉ុន្មាន?
</div>

<div class="self-check" data-min="1354000" data-max="1354000" markdown>
**៤.** សញ្ញាបូក `466E 1354N` មានកូអរដោនេ Y (North) ប៉ុន្មានម៉ែត្រ?
</div>

