CREATE PROCEDURE insert_schimbare_regina
    @id_operatiune INT,
    @id_regina INT,
    @id_familie INT
AS
BEGIN
    -- Declare the necessary variables
    DECLARE @old_id_regina INT;

    -- Validate input parameters
    IF @id_regina IS NULL OR @id_familie IS NULL
    BEGIN
        RAISERROR ('All fields are required for schimbare_regina!', 16, 1);
        RETURN;
    END

    -- Get the current id_regina for the given id_familie
    SELECT @old_id_regina = id_regina
    FROM FamilieDeAlbine
    WHERE id_familie = @id_familie;

    -- If no old regina is found, return an error
    IF @old_id_regina IS NULL
    BEGIN
        RAISERROR ('No regina found for the given family!', 16, 1);
        RETURN;
    END

    -- Delete the old regina from the Regina table
    DELETE FROM Regina
    WHERE id_regina = @old_id_regina;

    -- Update the FamilieDeAlbine table to link the new regina
    UPDATE FamilieDeAlbine
    SET id_regina = @id_regina
    WHERE id_familie = @id_familie;

    -- Optionally, return a success message or status
    PRINT 'Operation schimbare_regina complete!';
END;
