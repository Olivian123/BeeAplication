-- GetFamiliiDeAlbine
CREATE OR ALTER PROCEDURE GetFamiliiDeAlbine
AS
BEGIN
    SELECT * FROM FamilieDeAlbine;
END;
GO

-- AddFamilieDeAlbine
CREATE OR ALTER PROCEDURE AddFamilieDeAlbine
    @id_regina INT,
    @id_stup INT,
    @stare_familie NVARCHAR(50)
AS
BEGIN
    DECLARE @cantitate INT;
    
    SELECT @cantitate = cantitate FROM Stup WHERE id_stup = @id_stup;
    IF @cantitate < 1
	BEGIN
		RAISERROR('Not enough bee hives available!', 16, 1)
        RETURN
	END
    
    UPDATE Stup SET cantitate = cantitate - 1 WHERE id_stup = @id_stup;
    
    INSERT INTO FamilieDeAlbine (id_regina, id_stup, stare_familie) 
    VALUES (@id_regina, @id_stup, @stare_familie);
END;
GO

-- GetRegine
CREATE OR ALTER PROCEDURE GetRegine
AS
BEGIN
    SELECT * FROM Regina;
END;
GO

-- GetStupi
CREATE OR ALTER PROCEDURE GetStupi
AS
BEGIN
    SELECT * FROM Stup;
END;
GO

-- AddStup
CREATE OR ALTER PROCEDURE AddStup
    @tip NVARCHAR(255),
    @numar_rame INT,
    @dimensiuni NVARCHAR(255),
    @material NVARCHAR(255),
    @cantitate INT
AS
BEGIN
    INSERT INTO Stup (tip, numar_rame, dimensiuni, material, cantitate)
    VALUES (@tip, @numar_rame, @dimensiuni, @material, @cantitate);
END;
GO

-- GetApicultori
CREATE OR ALTER PROCEDURE GetAllApicultori
AS
BEGIN
    SELECT * FROM Apicultor;
END;
GO

-- AddApicultor
CREATE OR ALTER PROCEDURE AddApicultor
    @nume VARCHAR(100),
    @prenume VARCHAR(100),
    @rol VARCHAR(100),
	@id_maestru INT
AS
BEGIN
    DECLARE @data_angajarii DATE = GETDATE();

    INSERT INTO Apicultor (nume, prenume, data_angajarii, rol, id_maestru)
    VALUES (@nume, @prenume, @data_angajarii, @rol, @id_maestru);
END;
GO

-- GetRecipient
CREATE OR ALTER PROCEDURE GetRecipient
AS
BEGIN
    SELECT * FROM Recipient;
END;
GO

-- AddRecipient
CREATE OR ALTER PROCEDURE AddRecipient
    @nume_recipient NVARCHAR(255),
    @numar_unitati INT,
    @cantitate DECIMAL(18, 2),
    @unitate_cantitate NVARCHAR(50)
AS
BEGIN
    INSERT INTO Recipient (nume_recipient, numar_unitati, cantitate, unitate_cantitate)
    VALUES (@nume_recipient, @numar_unitati, @cantitate, @unitate_cantitate);
END;
GO

-- GetMiere
CREATE OR ALTER PROCEDURE GetMiere
AS
BEGIN
    SELECT * FROM Miere;
END;
GO

-- Get Produse
CREATE OR ALTER PROCEDURE GetProduse
AS
BEGIN
	SELECT * FROM Produs
END;
GO

-- GetInterventii
CREATE OR ALTER PROCEDURE GetInterventii
AS
BEGIN
SELECT i.data_interventie, 
       i.observatii, do.detalii, 
	   CONCAT(a.nume, ' ', a.prenume) as 'Nume Apicultor', 
	   i.id_familie AS 'Numar Stup'
  FROM Interventie        i
  JOIN DetaliiOperatiune do ON i.id_interventie = do.id_interventie
  JOIN Apicultor          a ON i.id_apicultor   = a.id_apicultor
END;
GO

-- GetDataFamAlbine
CREATE OR ALTER PROCEDURE GetDataFamAlbine
AS
BEGIN
SELECT r.tip_regina, r.provenienta, s.tip, s.numar_rame, s.material , fa.stare_familie
 FROM FamilieDeAlbine fa
 JOIN Stup             s ON fa.id_stup   = s.id_stup
 JOIN Regina           r ON fa.id_regina = r.id_regina
END;
GO

-- GetStupRasa
CREATE OR ALTER PROCEDURE GET_STUP_RASA
AS
BEGIN
	SELECT * FROM ZV_STUP_RASA
END;
GO

-- GetTotalVanzariProdus
CREATE OR ALTER PROCEDURE GET_Total_Vanzari_Produs
AS
BEGIN
	SELECT * FROM ZV_Total_Vanzari_Produs
END;
GO

-- GetTratamentHrana
CREATE OR ALTER PROCEDURE GetTratamentHrana
AS
BEGIN
SELECT TOP (1000) *
  FROM [ferma].[dbo].[ZV_Trtament_Hrana_TIP]
END;
GO





