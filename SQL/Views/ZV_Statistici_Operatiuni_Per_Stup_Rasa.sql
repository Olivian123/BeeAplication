-- Pentru fiecare tip de stup și regină, sa se calculeze:
-- cele mai populare tipuri de cutii de stup pentru fiecare regină;
-- numărul mediu de tratamente și hraniri pe tip de regină.
-- Complexitate: 7

CREATE OR ALTER VIEW ZV_Statistici_Operatiuni_Per_Stup_Rasa
AS
-- Calcularea celor mai populare tipuri de stupuri pentru fiecare regină
WITH RankedCounts AS (
    SELECT 
        s.tip AS TipStup,
        r.tip_regina AS RasaRegina,
        COUNT(*) AS NumarFamilii,
        ROW_NUMBER() OVER (PARTITION BY s.tip ORDER BY COUNT(*) DESC) AS Rnk
    FROM Stup s
    JOIN FamilieDeAlbine fa ON s.id_stup = fa.id_stup -- +1
    JOIN Regina r ON fa.id_regina = r.id_regina -- +1
    GROUP BY s.tip, r.tip_regina -- +1
),
-- Calculul numărului mediu de tratamente și hraniri per tip de regină
TratamenteHrana AS (
    SELECT 
        r.tip_regina,
        COUNT(CASE WHEN i.observatii LIKE '%tratament%' THEN 1 END) / COUNT(DISTINCT r.id_regina) AS numar_mediu_tratamente,
        COUNT(CASE WHEN i.observatii LIKE '%hrana%' THEN 1 END) / COUNT(DISTINCT r.id_regina) AS numar_mediu_hraniri,
        COUNT(DISTINCT r.id_regina) AS 'Numar Familii'
    FROM FamilieDeAlbine fa
    JOIN Interventie i ON fa.id_familie = i.id_familie -- +1
    JOIN DetaliiOperatiune de ON i.id_interventie = de.id_interventie -- +1
    JOIN Regina r ON fa.id_regina = r.id_regina -- +1
    GROUP BY r.tip_regina
)
-- Selectarea informațiilor combinate
SELECT 
    rc.TipStup,
    rc.RasaRegina,
    rc.NumarFamilii AS NumarFamiliiStup,
    th.numar_mediu_tratamente,
    th.numar_mediu_hraniri
FROM RankedCounts rc
JOIN TratamenteHrana th ON rc.RasaRegina = th.tip_regina -- +1
WHERE rc.Rnk = 1;