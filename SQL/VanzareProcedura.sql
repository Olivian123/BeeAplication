CREATE OR ALTER PROCEDURE VanzareProcedura
    @nume_produs NVARCHAR(100),
    @cantitate_ceruta INT
AS
BEGIN
    DECLARE @id_produs INT;
    DECLARE @cantitate_totala INT;

    -- Step 1: Extract product data from Produs table
    SELECT @id_produs = id_produs, @cantitate_totala = cantitate
    FROM Produs
    WHERE nume_produs = @nume_produs;

    -- Step 2: Check if the product exists
    IF @id_produs IS NULL
    BEGIN
        RAISERROR('No product found!', 16, 1);
        RETURN;
    END

    -- Step 3: Validate requested quantity
    IF @cantitate_ceruta <= 0
    BEGIN
        RAISERROR('Quantity requested must be positive!', 16, 1);
        RETURN;
    END

    IF @cantitate_ceruta > @cantitate_totala
    BEGIN
        RAISERROR('Not enough products available, there are %d available!', 16, 1, @cantitate_totala);
        RETURN;
    END

    -- Step 4: Update product quantity in Produs table
    UPDATE Produs
    SET cantitate = @cantitate_totala - @cantitate_ceruta
    WHERE id_produs = @id_produs;

    -- Step 5: Insert sale into Vanzare table
    INSERT INTO Vanzare (cantitate, data_vanzare, id_produs)
    VALUES (@cantitate_ceruta, GETDATE(), @id_produs);
END;

