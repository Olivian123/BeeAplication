CREATE PROCEDURE PackHoney
    @tip_miere NVARCHAR(255),
    @vechime_maxima INT,
    @nume_recipient NVARCHAR(255),
    @numar_unitati INT,
    @pret DECIMAL(10, 2)
AS
BEGIN
    -- Calculate the date limit
    DECLARE @date_before_now DATE
    SET @date_before_now = DATEADD(DAY, -365 * @vechime_maxima, GETDATE())

    -- Declare variables for honey data
    DECLARE @id_miere INT
    DECLARE @cantitate_totala_miere FLOAT

    -- Check honey availability
    SELECT @id_miere = id_miere, @cantitate_totala_miere = cantitate
    FROM Miere
    WHERE tip = @tip_miere AND data_extractie > @date_before_now

    IF @id_miere IS NULL
    BEGIN
        RAISERROR('No suitable honey found!', 16, 1)
        RETURN
    END

    -- Declare variables for recipient data
    DECLARE @id_recipient INT
    DECLARE @cantitate_totala_recip INT
    DECLARE @cantitate_per_unit FLOAT

    -- Check recipient availability
    SELECT @id_recipient = id_recipient, @cantitate_totala_recip = numar_unitati, @cantitate_per_unit = cantitate
    FROM Recipient
    WHERE nume_recipient = @nume_recipient

    IF @id_recipient IS NULL
    BEGIN
        RAISERROR('No suitable recipient found!', 16, 1)
        RETURN
    END

    IF @numar_unitati > @cantitate_totala_recip
    BEGIN
        RAISERROR('Not enough recipients!', 16, 1)
        RETURN
    END

    -- Check honey requirement
    DECLARE @cantitate_ceruta_miere FLOAT
    SET @cantitate_ceruta_miere = @numar_unitati * @cantitate_per_unit
    IF @cantitate_ceruta_miere > @cantitate_totala_miere
    BEGIN
        RAISERROR('Not enough honey!', 16, 1)
        RETURN
    END

    -- Update recipient table
    UPDATE Recipient
    SET numar_unitati = @cantitate_totala_recip - @numar_unitati
    WHERE id_recipient = @id_recipient

    -- Update honey table
    UPDATE Miere
    SET cantitate = @cantitate_totala_miere - @cantitate_ceruta_miere
    WHERE id_miere = @id_miere

    -- Create product name
    DECLARE @nume_produs NVARCHAR(255)
    SET @nume_produs = @nume_recipient + ' ' + @tip_miere

    -- Declare variables for product check
    DECLARE @id_produs INT
    DECLARE @cantitate INT

    -- Check if the product exists or not
    SELECT @id_produs = id_produs, @cantitate = cantitate
    FROM Produs
    WHERE nume_produs = @nume_produs AND id_miere = @id_miere AND id_recipient = @id_recipient

    IF @id_produs IS NOT NULL
    BEGIN
        -- Update the existing product quantity
        UPDATE Produs
        SET cantitate = @cantitate + 1
        WHERE id_produs = @id_produs
    END
    ELSE
    BEGIN
        -- Insert a new product into the Produs table
        INSERT INTO Produs (nume_produs, cantitate, id_miere, id_recipient, pret)
        VALUES (@nume_produs, @cantitate_ceruta_miere, @id_miere, @id_recipient, @pret)
    END

    COMMIT
END
