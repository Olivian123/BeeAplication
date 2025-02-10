CREATE PROCEDURE insert_roire
    @id_operatiune INT,
    @data DATETIME,
    @provenienta_regina NVARCHAR(100),
    @tip_stup NVARCHAR(100),
    @id_familie INT
AS
BEGIN
    -- Get the tip_regina for the given family (FamilieDeAlbine)
    DECLARE @tip_regina NVARCHAR(100);
    SELECT @tip_regina = r.tip_regina
    FROM FamilieDeAlbine fa
    JOIN Regina r ON fa.id_regina = r.id_regina
    WHERE fa.id_familie = @id_familie;

    DECLARE @id_new_regina INT;
    DECLARE @status_ NVARCHAR(50) = 'activa';
    DECLARE @data_imperechere_regina DATE = CAST(GETDATE() AS DATE);

    -- Insert a new regina into the Regina table and capture the id_regina
    DECLARE @output_table TABLE (id_regina INT);
    INSERT INTO Regina (tip_regina, data_imperechere, status_, provenienta, varsta)
    OUTPUT INSERTED.id_regina INTO @output_table
    VALUES (@tip_regina, @data_imperechere_regina, @status_, @provenienta_regina, 0);

    -- Get the newly inserted id_regina from the output table
    SELECT @id_new_regina = id_regina FROM @output_table;

    DECLARE @id_stup INT;
    DECLARE @current_cantitate INT;
    DECLARE @new_cantitate INT;

    -- Check if a matching stup exists and get its current cantitate
    SELECT @id_stup = id_stup, @current_cantitate = cantitate
    FROM Stup
    WHERE tip = @tip_stup;

    -- If no stup is found, return an error
    IF @id_stup IS NULL
    BEGIN
        RAISERROR('Stup not found!', 16, 1);
        RETURN;
    END

    -- Decrease the quantity (cantitate) of the chosen Stup by 1
    SET @new_cantitate = @current_cantitate - 1;

    -- Update Stup to subtract 1 from the cantitate field
    UPDATE Stup
    SET cantitate = @new_cantitate
    WHERE id_stup = @id_stup;

    -- Insert a new record into FamilieDeAlbine with the new regina and stup
    INSERT INTO FamilieDeAlbine (id_regina, id_stup, stare_familie)
    VALUES (@id_new_regina, @id_stup, 'activa');

    -- Return a success message
    PRINT 'Operation roire complete!';
END;
