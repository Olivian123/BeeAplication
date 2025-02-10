USE [ferma];
GO

-- Table: AdministrareHrana
SET ANSI_NULLS ON;
GO
SET QUOTED_IDENTIFIER ON;
GO
CREATE TABLE [dbo].[AdministrareHrana] (
    [id_hrana] INT IDENTITY(1,1) NOT NULL,
    [id_operatiune] INT NULL,
    [tip_hrana] NVARCHAR(50) NULL,
    [cantitate_hrana] FLOAT NULL,
    [motiv_administrare] NVARCHAR(255) NULL,
    PRIMARY KEY CLUSTERED ([id_hrana] ASC)
) ON [PRIMARY];
GO

-- Table: Apicultor
CREATE TABLE [dbo].[Apicultor] (
    [id_apicultor] INT IDENTITY(1,1) NOT NULL,
    [nume] NVARCHAR(100) NULL,
    [prenume] NVARCHAR(100) NULL,
    [data_angajarii] DATE NULL,
    [rol] NVARCHAR(50) NULL,
    PRIMARY KEY CLUSTERED ([id_apicultor] ASC)
) ON [PRIMARY];
GO

-- Table: DetaliiOperatiune
CREATE TABLE [dbo].[DetaliiOperatiune] (
    [id_operatiune] INT IDENTITY(1,1) NOT NULL,
    [id_interventie] INT NULL,
    [detalii] NVARCHAR(255) NULL,
    PRIMARY KEY CLUSTERED ([id_operatiune] ASC)
) ON [PRIMARY];
GO

-- Table: ExtrasRame
CREATE TABLE [dbo].[ExtrasRame] (
    [id_extras_rame] INT IDENTITY(1,1) NOT NULL,
    [id_operatiune] INT NULL,
    [numar_rame] INT NULL,
    [tip_rame] NVARCHAR(50) NULL,
    [data_extras] DATE NULL,
    [id_miere] INT NULL,
    PRIMARY KEY CLUSTERED ([id_extras_rame] ASC)
) ON [PRIMARY];
GO

-- Table: FamilieDeAlbine
CREATE TABLE [dbo].[FamilieDeAlbine] (
    [id_familie] INT IDENTITY(1,1) NOT NULL,
    [stare_familie] NVARCHAR(50) NULL,
    [id_regina] INT NULL,
    [id_stup] INT NULL,
    PRIMARY KEY CLUSTERED ([id_familie] ASC)
) ON [PRIMARY];
GO

-- Table: Interventie
CREATE TABLE [dbo].[Interventie] (
    [id_interventie] INT IDENTITY(1,1) NOT NULL,
    [id_apicultor] INT NULL,
    [data_interventie] DATE NULL,
    [observatii] NVARCHAR(255) NULL,
    [id_familie] INT NULL,
    PRIMARY KEY CLUSTERED ([id_interventie] ASC)
) ON [PRIMARY];
GO

-- Table: Miere
CREATE TABLE [dbo].[Miere] (
    [id_miere] INT IDENTITY(1,1) NOT NULL,
    [cantitate] DECIMAL(10, 2) NOT NULL,
    [unitate_masura] NVARCHAR(20) NOT NULL,
    [tip] NVARCHAR(100) NOT NULL,
    [observatii] NVARCHAR(255) NULL,
    [data_extractie] DATE NULL,
    PRIMARY KEY CLUSTERED ([id_miere] ASC)
) ON [PRIMARY];
GO

-- Table: Produs
CREATE TABLE [dbo].[Produs] (
    [id_produs] INT IDENTITY(1,1) NOT NULL,
    [nume_produs] NVARCHAR(50) NOT NULL,
    [data_ambalare] DATE NOT NULL,
    [cantitate] DECIMAL(10, 2) NOT NULL,
    [observatii] NVARCHAR(255) NULL,
    [id_miere] INT NULL,
    [id_recipient] INT NULL,
    [pret] DECIMAL(10, 2) NULL,
    PRIMARY KEY CLUSTERED ([id_produs] ASC)
) ON [PRIMARY];
GO

-- Table: Recipient
CREATE TABLE [dbo].[Recipient] (
    [id_recipient] INT IDENTITY(1,1) NOT NULL,
    [nume_recipient] NVARCHAR(30) NULL,
    [numar_unitati] INT NULL,
    [cantitate] DECIMAL(10, 2) NOT NULL,
    [unitate_cantitate] NVARCHAR(20) NOT NULL,
    PRIMARY KEY CLUSTERED ([id_recipient] ASC)
) ON [PRIMARY];
GO

-- Table: Regina
CREATE TABLE [dbo].[Regina] (
    [id_regina] INT IDENTITY(1,1) NOT NULL,
    [tip_regina] NVARCHAR(100) NULL,
    [data_imperechere] DATE NULL,
    [status_] NVARCHAR(50) NULL,
    [varsta] INT NULL,
    [provenienta] NVARCHAR(50) NULL,
    PRIMARY KEY CLUSTERED ([id_regina] ASC)
) ON [PRIMARY];
GO

-- Table: Roire
CREATE TABLE [dbo].[Roire] (
    [id_roire] INT IDENTITY(1,1) NOT NULL,
    [id_operatiune] INT NULL,
    [id_stup_nou] INT NULL,
    [id_regina] INT NULL,
    [id_stup] INT NULL,
    PRIMARY KEY CLUSTERED ([id_roire] ASC)
) ON [PRIMARY];
GO

-- Table: SchimbareRegina
CREATE TABLE [dbo].[SchimbareRegina] (
    [id_schimbare_regina] INT IDENTITY(1,1) NOT NULL,
    [id_operatiune] INT NULL,
    [id_regina] INT NULL,
    [tip_regina_noua] NVARCHAR(100) NULL,
    [motiv_schimbare] NVARCHAR(255) NULL,
    PRIMARY KEY CLUSTERED ([id_schimbare_regina] ASC)
) ON [PRIMARY];
GO

-- Table: Stup
CREATE TABLE [dbo].[Stup] (
    [id_stup] INT IDENTITY(1,1) NOT NULL,
    [tip] NVARCHAR(50) NULL,
    [numar_rame] INT NULL,
    [dimensiuni] NVARCHAR(50) NULL,
    [material] NVARCHAR(50) NULL,
    [cantitate] INT NULL,
    PRIMARY KEY CLUSTERED ([id_stup] ASC)
) ON [PRIMARY];
GO

-- Table: Tratamente
CREATE TABLE [dbo].[Tratamente] (
    [id_tratament] INT IDENTITY(1,1) NOT NULL,
    [id_operatiune] INT NULL,
    [tip_tratament] NVARCHAR(100) NULL,
    [doza] NVARCHAR(50) NULL,
    [data_tratament] DATE NULL,
    PRIMARY KEY CLUSTERED ([id_tratament] ASC)
) ON [PRIMARY];
GO

-- Table: Vanzare
CREATE TABLE [dbo].[Vanzare] (
    [id_vanzare] INT IDENTITY(1,1) NOT NULL,
    [cantitate] INT NULL,
    [data_vanzare] DATE NULL,
    [id_produs] INT NULL,
    PRIMARY KEY CLUSTERED ([id_vanzare] ASC)
) ON [PRIMARY];
GO

-- Add Foreign Key Constraints
ALTER TABLE [dbo].[AdministrareHrana] ADD FOREIGN KEY ([id_operatiune]) REFERENCES [dbo].[DetaliiOperatiune] ([id_operatiune]);
ALTER TABLE [dbo].[DetaliiOperatiune] ADD FOREIGN KEY ([id_interventie]) REFERENCES [dbo].[Interventie] ([id_interventie]);
ALTER TABLE [dbo].[ExtrasRame] ADD FOREIGN KEY ([id_operatiune]) REFERENCES [dbo].[DetaliiOperatiune] ([id_operatiune]);
ALTER TABLE [dbo].[ExtrasRame] ADD CONSTRAINT [FK_ExtrasRame_Miere] FOREIGN KEY ([id_miere]) REFERENCES [dbo].[Miere] ([id_miere]);
ALTER TABLE [dbo].[FamilieDeAlbine] ADD CONSTRAINT [FK_FamilieDeAlbine_Regina] FOREIGN KEY ([id_regina]) REFERENCES [dbo].[Regina] ([id_regina]);
ALTER TABLE [dbo].[FamilieDeAlbine] ADD CONSTRAINT [FK_FamilieDeAlbine_Stup] FOREIGN KEY ([id_stup]) REFERENCES [dbo].[Stup] ([id_stup]);
ALTER TABLE [dbo].[Interventie] ADD CONSTRAINT [FK_Interventie_Apicultor] FOREIGN KEY ([id_apicultor]) REFERENCES [dbo].[Apicultor] ([id_apicultor]);
ALTER TABLE [dbo].[Interventie] ADD CONSTRAINT [FK_Interventie_Familie] FOREIGN KEY ([id_familie]) REFERENCES [dbo].[FamilieDeAlbine] ([id_familie]);
ALTER TABLE [dbo].[Produs] ADD CONSTRAINT [FK_Produs_Miere] FOREIGN KEY ([id_miere]) REFERENCES [dbo].[Miere] ([id_miere]);
ALTER TABLE [dbo].[Produs] ADD CONSTRAINT [FK_Produs_Recipiet] FOREIGN KEY ([id_recipient]) REFERENCES [dbo].[Recipient] ([id_recipient]);
ALTER TABLE [dbo].[Roire] ADD FOREIGN KEY ([id_operatiune]) REFERENCES [dbo].[DetaliiOperatiune] ([id_operatiune]);
ALTER TABLE [dbo].[Roire] ADD CONSTRAINT [FK_Roire_Regina] FOREIGN KEY ([id_regina]) REFERENCES [dbo].[Regina] ([id_regina]);
ALTER TABLE [dbo].[Roire] ADD CONSTRAINT [FK_Roire_Stup] FOREIGN KEY ([id_stup]) REFERENCES [dbo].[Stup] ([id_stup]);
ALTER TABLE [dbo].[SchimbareRegina] ADD FOREIGN KEY ([id_operatiune]) REFERENCES [dbo].[DetaliiOperatiune] ([id_operatiune]);
ALTER TABLE [dbo].[SchimbareRegina] ADD CONSTRAINT [FK_SchimbareRegina_Regina] FOREIGN KEY ([id_regina]) REFERENCES [dbo].[Regina] ([id_regina]);
ALTER TABLE [dbo].[Tratamente] ADD FOREIGN KEY ([id_operatiune]) REFERENCES [dbo].[DetaliiOperatiune] ([id_operatiune]);
ALTER TABLE [dbo].[Vanzare] ADD CONSTRAINT [FK_Vanzare_Produs] FOREIGN KEY ([id_produs]) REFERENCES [dbo].[Produs] ([id_produs]);
GO
