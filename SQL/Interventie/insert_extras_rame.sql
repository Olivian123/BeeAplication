CREATE OR ALTER PROCEDURE insert_extras_rame
    @id_operatiune INT,
    @numar_rame_extrase INT,
    @cantitate_miere DECIMAL(10, 2),
    @tip_miere NVARCHAR(100)
AS
BEGIN
    -- Validate required fields
    IF @numar_rame_extrase IS NULL OR @cantitate_miere IS NULL OR @tip_miere IS NULL
    BEGIN
        RAISERROR('All fields required for extras_rame!', 16, 1);
        RETURN;
    END

    -- Get the date 100 days before today
    DECLARE @lower_date DATE = DATEADD(DAY, -150, GETDATE());

    -- Check if there's a matching row in Miere table
    DECLARE @id_miere INT, @cantitate_totala DECIMAL(10, 2);
    SELECT @id_miere = id_miere, @cantitate_totala = cantitate
    FROM Miere
    WHERE tip = @tip_miere AND data_extractie > @lower_date;

    -- If a matching row is found, update it; otherwise, insert a new row
    IF @id_miere IS NOT NULL
    BEGIN
        -- Update existing row
        UPDATE Miere
        SET cantitate = @cantitate_totala + @cantitate_miere
        WHERE id_miere = @id_miere;
    END
    ELSE
    BEGIN
        -- Insert a new row
        INSERT INTO Miere (cantitate, unitate_masura, tip, data_extractie)
        OUTPUT INSERTED.id_miere
        VALUES (@cantitate_miere, 'kg', @tip_miere, GETDATE());
        
        -- Get the ID of the newly inserted row
        SELECT @id_miere = SCOPE_IDENTITY();
    END

    -- Insert into ExtrasRame table
    INSERT INTO ExtrasRame (id_operatiune, numar_rame, data_extras, id_miere)
    VALUES (@id_operatiune, @numar_rame_extrase, GETDATE(), @id_miere);

    -- Return success message
    PRINT 'Operation extras_rame complete!';
END;
