# file: extract_metadata.py

import psycopg2
from psycopg2 import sql
from pymediainfo import MediaInfo

def extract_metadata(file_path):
    """
    Extract metadata from a media file.

    Args:
        file_path (str): Path to the media file.

    Returns:
        Dict: A dictionary containing metadata.
    """
    media_info = MediaInfo.parse(file_path)
    metadata = {}
    for track in media_info.tracks:
        if track.track_type == 'General':
            metadata['file_name'] = track.file_name
            metadata['file_extension'] = track.file_extension
            metadata['duration'] = track.duration
            metadata['file_size'] = track.file_size
            # Add more fields as needed
    return metadata

def save_metadata_to_db(metadata, db_config):
    """
    Save metadata to PostgreSQL database.

    Args:
        metadata (Dict): Metadata dictionary.
        db_config (Dict): Database configuration dictionary.
    """
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()

    # Ensure table exists
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS media_metadata (
        id SERIAL PRIMARY KEY,
        file_name TEXT,
        file_extension TEXT,
        duration BIGINT,
        file_size BIGINT,
        file_type TEXT
    );
    '''
    cursor.execute(create_table_query)

    # Insert metadata
    insert_query = '''
    INSERT INTO media_metadata (file_name, file_extension, duration, file_size)
    VALUES (%s, %s, %s, %s)
    RETURNING id;
    '''
    cursor.execute(insert_query, (
        metadata.get('file_name'),
        metadata.get('file_extension'),
        metadata.get('duration'),
        metadata.get('file_size')
    ))
    conn.commit()
    cursor.close()
    conn.close()

# Usage example
if __name__ == "__main__":
    file_path = 'path/to/media/file'
    db_config = {
        'dbname': 'yourdbname',
        'user': 'youruser',
        'password': 'yourpass',
        'host': 'localhost',
        'port': 5432
    }
    metadata = extract_metadata(file_path)
    save_metadata_to_db(metadata, db_config)