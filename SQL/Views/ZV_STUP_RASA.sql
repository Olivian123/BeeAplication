USE [ferma]
GO

SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

-- pentru fiecare tip de cutie de stup care este cea mai comuna rasa
-- Complexitate: 5

CREATE VIEW [dbo].[ZV_STUP_RASA]
AS
WITH RankedCounts AS (
    SELECT 
        s.tip AS TipStup,
        r.tip_regina AS RasaRegina,
        COUNT(*) AS NumarFamilii,
        ROW_NUMBER() OVER (PARTITION BY s.tip ORDER BY COUNT(*) DESC) AS Rnk
    FROM Stup s
    JOIN FamilieDeAlbine fa ON s.id_stup = fa.id_stup
    JOIN Regina r ON fa.id_regina = r.id_regina
    GROUP BY s.tip, r.tip_regina
)
SELECT 
    TipStup,
    RasaRegina,
    NumarFamilii
FROM RankedCounts
WHERE Rnk = 1;

GO


