CREATE OR ALTER VIEW ZV_DATA_FAM_ALBINE
AS
SELECT r.tip_regina, r.provenienta, s.tip, s.numar_rame, s.material , fa.stare_familie
 FROM FamilieDeAlbine fa
 JOIN Stup             s ON fa.id_stup   = s.id_stup
 JOIN Regina           r ON fa.id_regina = r.id_regina
