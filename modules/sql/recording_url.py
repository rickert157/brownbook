import sqlite3
from modules.config import (
        status_type_warning, 
        status_type_error, 
        status_type_info,
        sitemap_second_level, 
        sitemap_first_step_file,
        sitemap_db,
        sitemap_last_level
        )
from modules.miniTools import (
        log_time,
        log_print
        )

def recording_urls_to_db():
    conn = sqlite3.connect(sitemap_db)
    create_table = f"""
    CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY,
        url TEXT UNIQUE
    )
    """
    conn.execute(create_table)
    conn.commit()

    list_urls = [] 
    with open(sitemap_second_level, 'r') as file:
        for line in file.readlines():
            url = line.strip()
            list_urls.append([url])

    if len(list_urls) != 0:
        recording_command = f"""INSERT OR IGNORE INTO urls (url) VALUES (?)"""
        conn.executemany(recording_command, list_urls)
        conn.commit()


if __name__ == '__main__':
    recording_urls_to_db()
