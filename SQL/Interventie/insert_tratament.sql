CREATE PROCEDURE insert_tratament
    @id_operatiune INT,
    @tip_tratament NVARCHAR(100),
    @doza DECIMAL(10, 2),
    @date DATE
AS
BEGIN
    -- Validate required fields
    IF @tip_tratament IS NULL OR @doza IS NULL
    BEGIN
        RAISERROR('All fields required for tratament!', 16, 1);
        RETURN;
    END

    -- Insert into Tratamente table
    INSERT INTO Tratamente (id_operatiune, tip_tratament, doza, data_tratament)
    VALUES (@id_operatiune, @tip_tratament, @doza, @date);
END;
