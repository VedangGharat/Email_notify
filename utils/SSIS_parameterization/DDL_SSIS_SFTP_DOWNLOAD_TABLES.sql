
/****** Object:  Table [DEV_HAOYUAN].[dbo].[Test_File_Insert]    Script Date: 2/27/2024 2:55:49 PM ******/
DROP TABLE IF EXISTS [DEV_HAOYUAN].[dbo].[Test_File_Insert];

-- Make table of submission file metadata
CREATE TABLE [DEV_HAOYUAN].[dbo].[Test_File_Insert](
	 [FILE_ID] [int] IDENTITY(1,1) NOT NULL
	,[FILENAME] [nchar](100) NULL
	,[SFTP_FILEPATH] [nchar](255) NULL
	,[SUBMISSION_ZIP] [nchar](100) NOT NULL
	,[LAST_WRITE_TIME] [smalldatetime] NULL
	,[LAST_ACCESS_TIME] [smalldatetime] NULL
	,[UPLOADED] [bit] NULL
 ,CONSTRAINT [PK_Test_File_Insert] PRIMARY KEY CLUSTERED 
(
	[FILE_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO


/****** Object:  Table [DEV_HAOYUAN].[dbo].[Test_File_Insert]    Script Date: 2/27/2024 2:55:49 PM ******/

DROP TABLE IF EXISTS [DEV_HAOYUAN].[dbo].[Test_Provider];
-- Make table of submission file metadata
CREATE TABLE [DEV_HAOYUAN].[dbo].[Test_Provider](
	 [PROVIDER_PK] [int] IDENTITY(1,1) NOT NULL
	,[PROVIDER_NAME] [nchar](20) NOT NULL
	,[PROVIDER_ABBREVIATION] [nchar](5) NULL
	,[CMA_ID] [nchar](10) NOT NULL
 
 ,CONSTRAINT [PROVIDER_PK] PRIMARY KEY CLUSTERED 
(
	[PROVIDER_PK] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

-- Insert Test Providers and their IDs
INSERT INTO [DEV_HAOYUAN].[dbo].[Test_Provider]
VALUES 
	 ('Test Provider 1', 'TP1', '99999')
	,('Test Provider 2', 'TP2', '00000')
	;
GO