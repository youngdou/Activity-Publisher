SET SESSION storage_engine = "InnoDB";
SET SESSION time_zone = "+0:00";
ALTER DATABASE CHARACTER SET "utf8";

DROP TABLE IF EXISTS activity;
CREATE TABLE activity (
    actName     VARCHAR(30)   NOT NULL PRIMARY KEY,
    actType     VARCHAR(10)   NOT NULL,
    actTime     VARCHAR(100)  NOT NULL,
    actLoc      VARCHAR(100)  NOT NULL,
    actIntru    VARCHAR(50)   NOT NULL,
    actFor      VARCHAR(30)   NOT NULL,
    actPub      VARCHAR(50)   NOT NULL,
    actJoin     VARCHAR(200)  NOT NULL,
    actDDL      VARCHAR(16)   NOT NULL,
    actDetail   VARCHAR(200)  NOT NULL,

    PEChapter   VARCHAR(30),
    welTime     VARCHAR(30),
    other       VARCHAR(30),
    actDem      VARCHAR(30)   
);