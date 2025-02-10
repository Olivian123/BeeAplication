-- pentru fiecare apicultor cu vechime de cel putin un an si 
-- care a intervenit macar odata
-- sa se calculeze:
-- experienta in fucntie de numarul mediu de interventii
-- si care este maestrul sau
-- Complexitate: 6

CREATE OR ALTER VIEW ZV_Experienta_Maestru_Apicultori
AS
SELECT 
    a.nume, 
    a.prenume, 
    COUNT(i.id_interventie) AS numar_interventii,
    AVG(COUNT(i.id_interventie)) OVER () AS numar_mediu_interventii,
    CASE 
        WHEN COUNT(i.id_interventie) >= (AVG(COUNT(i.id_interventie)) OVER ()) + 5 THEN 'Expert' 
        WHEN COUNT(i.id_interventie) BETWEEN (AVG(COUNT(i.id_interventie)) OVER ()) AND (AVG(COUNT(i.id_interventie)) OVER ()) + 5 THEN 'Intermediar'
        ELSE 'Incepator'
    END AS nivel_experienta,
    COUNT(DISTINCT fa.id_familie) AS numar_familii,
    CONCAT(m.nume, ' ', m.prenume) as nume_maestru
FROM Apicultor a
LEFT JOIN Interventie i ON a.id_apicultor = i.id_apicultor -- +1
LEFT JOIN FamilieDeAlbine fa ON i.id_familie = fa.id_familie -- +1
LEFT JOIN Apicultor m ON a.id_maestru = m.id_apicultor -- +1
WHERE a.data_angajarii >= DATEADD(YEAR, -5, GETDATE()) -- +1
GROUP BY a.id_apicultor, a.nume, a.prenume, m.nume, m.prenume -- +1
HAVING COUNT(i.id_interventie) > 1 -- +1
