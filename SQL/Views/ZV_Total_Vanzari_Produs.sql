-- pentru fiecare produs vandut care este cantitatea vanduta si totalul obtinut
-- totalul pentru fiecare produs trebuie sa fie mai mare decat 100
-- Complexitate: 4

CREATE OR ALTER VIEW ZV_Total_Vanzari_Produs
AS
SELECT p.nume_produs, 
       COUNT(v.id_vanzare) AS nr_vanzari,
	   SUM(v.cantitate) as 'Numar porduse vandute ',
	   SUM(v.cantitate) * p.pret as 'Total vanzari produs',
       MIN(v.data_vanzare) AS prima_vanzare,
       MAX(v.data_vanzare) AS ultima_vanzare
FROM produs p
JOIN vanzare v ON p.id_produs = v.id_produs
WHERE v.data_vanzare BETWEEN '2024-01-01' AND '2026-01-01'
GROUP BY p.id_produs, p.nume_produs, p.pret
HAVING SUM(v.cantitate) * p.pret > 100;
