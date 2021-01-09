# ReadNovelFull-Tracker

Script to check for new Chapters on https://readnovelfull.com made to run on Heroku

Switched from JSON to PostgreSQL because Heroku restarts dynos frequently

Really hacky DB solution but it does what I want so i won't bother any further.

```sql
CREATE TABLE settings (
   NAME VARCHAR NOT NULL,
   VALUE VARCHAR not NULL
);

create table novels (
	novel VARCHAR not null,
	name VARCHAR,
	id INT,
	last_chapter VARCHAR);
	

insert into settings
VALUES('WEBHOOK_ID', '-'),
('WEBHOOK_TOKEN', '-'),
('DISCORD_USER','-'),
('WEBSITE','https://readnovelfull.com'),
('EXTENSION','.html'),
('CHAPTER_ARCHIVE','/ajax/chapter-archive?novelId=')

insert into novels (novel)
VALUES('the-legendary-mechanic'),
('reincarnation-of-the-strongest-sword-god'),
('mages-are-too-op'),
('supreme-magus'),
('overgeared')
```
