CREATE OR ALTER PROCEDURE add_interventie_from_json
    @json_data NVARCHAR(MAX)  -- JSON input as a parameter
AS
BEGIN
    -- Start a transaction to ensure atomicity
    BEGIN TRANSACTION;

    -- Parse the JSON input
    DECLARE @id_apicultor INT;
    SET @id_apicultor = JSON_VALUE(@json_data, '$.id_apicultor');

    DECLARE @data_interventie DATE;
    SET @data_interventie = JSON_VALUE(@json_data, '$.data_interventie');

    DECLARE @observatii NVARCHAR(255);
    SET @observatii = JSON_VALUE(@json_data, '$.observatii');

    DECLARE @id_familie INT;
    SET @id_familie = JSON_VALUE(@json_data, '$.id_familie');

    DECLARE @detalii NVARCHAR(255);
    SET @detalii = JSON_VALUE(@json_data, '$.detalii');

    -- Validate required fields (simplified example)
    IF @id_apicultor IS NULL OR @data_interventie IS NULL OR @id_familie IS NULL OR @detalii IS NULL
    BEGIN
        RAISERROR('Missing required fields!', 16, 1);
        ROLLBACK TRANSACTION;
        RETURN;
    END

    -- Insert into Interventie table
    DECLARE @id_interventie INT;
    INSERT INTO Interventie (id_apicultor, data_interventie, observatii, id_familie)
    OUTPUT INSERTED.id_interventie
    VALUES (@id_apicultor, @data_interventie, @observatii, @id_familie);

    -- Capture the id_interventie
    SELECT @id_interventie = SCOPE_IDENTITY();

    -- Insert into DetaliiOperatiune table
    DECLARE @id_operatiune INT;
    INSERT INTO DetaliiOperatiune (id_interventie, detalii)
    OUTPUT INSERTED.id_operatiune
    VALUES (@id_interventie, @detalii);

    -- Capture the id_operatiune
    SELECT @id_operatiune = SCOPE_IDENTITY();

    -- Process operations based on the details in 'detalii'
    IF CHARINDEX('schimbare regina', @detalii) > 0
    BEGIN
        -- Extract the required field for schimbare regina
        DECLARE @id_regina INT;
        SET @id_regina = JSON_VALUE(@json_data, '$.id_regina');

        -- Ensure the value exists
        IF @id_regina IS NOT NULL
        BEGIN
            -- Call insert_schimbare_regina operation
            EXEC insert_schimbare_regina @id_operatiune, @id_regina, @id_familie;
        END
        ELSE
        BEGIN
            RAISERROR('Missing id_regina for schimbare regina!', 16, 1);
            ROLLBACK TRANSACTION;
            RETURN;
        END
    END

    IF CHARINDEX('roire', @detalii) > 0
    BEGIN
        -- Extract the required fields for roire
        DECLARE @provenienta_regina NVARCHAR(100);
        DECLARE @tip_stup NVARCHAR(100);
        SET @provenienta_regina = JSON_VALUE(@json_data, '$.provenienta_regina');
        SET @tip_stup = JSON_VALUE(@json_data, '$.tip_stup');

        -- Ensure the values exist
        IF @provenienta_regina IS NOT NULL AND @tip_stup IS NOT NULL
        BEGIN
            -- Call insert_roire operation
            EXEC insert_roire @id_operatiune, @data_interventie, @provenienta_regina, @tip_stup, @id_familie;
        END
        ELSE
        BEGIN
            RAISERROR('Missing fields for roire!', 16, 1);
            ROLLBACK TRANSACTION;
            RETURN;
        END
    END

    IF CHARINDEX('tratament', @detalii) > 0
    BEGIN
        -- Extract the required fields for tratament
        DECLARE @tip_tratament NVARCHAR(100);
        DECLARE @doza DECIMAL(10, 2);
        SET @tip_tratament = JSON_VALUE(@json_data, '$.tip_tratament');
        SET @doza = JSON_VALUE(@json_data, '$.tratament.doza');

        -- Ensure the values exist
        IF @tip_tratament IS NOT NULL AND @doza IS NOT NULL
        BEGIN
            -- Call insert_tratament operation
            EXEC insert_tratament @id_operatiune, @tip_tratament, @doza, @data_interventie;
        END
        ELSE
        BEGIN
            RAISERROR('Missing fields for tratament!', 16, 1);
            ROLLBACK TRANSACTION;
            RETURN;
        END
    END

    IF CHARINDEX('administrare_hrana', @detalii) > 0
    BEGIN
        -- Extract the required fields for administrare_hrana
        DECLARE @tip_hrana NVARCHAR(100);
        DECLARE @cantitate_hrana DECIMAL(10, 2);
        DECLARE @motiv_administrare NVARCHAR(255);
        SET @tip_hrana = JSON_VALUE(@json_data, '$.tip_hrana');
        SET @cantitate_hrana = JSON_VALUE(@json_data, '$.cantitate_hrana');
        SET @motiv_administrare = JSON_VALUE(@json_data, '$.motiv_administrare');

        -- Ensure the values exist
        IF @tip_hrana IS NOT NULL AND @cantitate_hrana IS NOT NULL AND @motiv_administrare IS NOT NULL
        BEGIN
            -- Call insert_administrare_hrana operation
            EXEC insert_administrare_hrana @id_operatiune, @tip_hrana, @cantitate_hrana, @motiv_administrare;
        END
        ELSE
        BEGIN
            RAISERROR('Missing fields for administrare_hrana!', 16, 1);
            ROLLBACK TRANSACTION;
            RETURN;
        END
    END

    IF CHARINDEX('extras_rame', @detalii) > 0
    BEGIN
        -- Extract the required fields for extras_rame
        DECLARE @numar_rame_extrase INT;
        DECLARE @cantitate_miere DECIMAL(10, 2);
        DECLARE @tip_miere NVARCHAR(100);
        SET @numar_rame_extrase = JSON_VALUE(@json_data, '$.numar_rame_extrase');
        SET @cantitate_miere = JSON_VALUE(@json_data, '$.cantitate_miere');
        SET @tip_miere = JSON_VALUE(@json_data, '$.tip_miere');

        -- Ensure the values exist
        IF @numar_rame_extrase IS NOT NULL AND @cantitate_miere IS NOT NULL AND @tip_miere IS NOT NULL
        BEGIN
            -- Call insert_extras_rame operation
            EXEC insert_extras_rame @id_operatiune, @numar_rame_extrase, @cantitate_miere, @tip_miere;
        END
        ELSE
        BEGIN
            RAISERROR('Missing fields for extras_rame!', 16, 1);
            ROLLBACK TRANSACTION;
            RETURN;
        END
    END

    -- Commit transaction if everything is successful
    COMMIT TRANSACTION;

    -- Return success message with the id_interventie
    SELECT 'Operation successful' AS message, @id_interventie AS id_interventie;

END;
