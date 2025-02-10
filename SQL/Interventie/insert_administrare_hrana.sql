CREATE PROCEDURE insert_administrare_hrana
    @id_operatiune INT,
    @tip_hrana NVARCHAR(100),
    @cantitate_hrana DECIMAL(10, 2),
    @motiv_administrare NVARCHAR(255)
AS
BEGIN
    -- Validate required fields
    IF @tip_hrana IS NULL OR @cantitate_hrana IS NULL OR @motiv_administrare IS NULL
    BEGIN
        RAISERROR('All fields required for administrare_hrana!', 16, 1);
        RETURN;
    END

    -- Insert into AdministrareHrana table
    INSERT INTO AdministrareHrana (id_operatiune, tip_hrana, cantitate_hrana, motiv_administrare)
    VALUES (@id_operatiune, @tip_hrana, @cantitate_hrana, @motiv_administrare);
END;
