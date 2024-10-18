import sqlite3
import click
from datetime import datetime

def export_full(dbpath="hubs.db", out='-', max_age=60*60*24):
    """Create a tab separated dump of the database"""
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT hub.ip, hub.port, hub.proto_version, hub.app_version, hub.ts, hub_info.fid, addr.country_code, addr.as_name
        FROM hub LEFT JOIN hub_info ,addr
        ON hub.ip = hub_info.ip AND hub.port = hub_info.port AND hub.ip = addr.ip
        WHERE unixepoch(hub.ts) > unixepoch() - ?
        """, (max_age,))
    records = cursor.fetchall()
    with click.open_file(out, 'w') as file_h:
        for r in records:
            click.echo(f'{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}\t{r[5] if r[5] else 0}\t{r[6]}\t{r[7]}\t{r[4]}', file=file_h)

def export_countries(dbpath="hubs.db", out='-', max_age=60*60*24):
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT count(*) as C, addr.country_code, addr.country_name
        FROM hub LEFT JOIN addr
        ON hub.ip = addr.ip
        WHERE unixepoch(hub.ts) > unixepoch() - ?
        GROUP BY addr.country_code
        ORDER BY C DESC
        """, (max_age,))
    records = cursor.fetchall()
    file_h = click.open_file(out, 'w')
    for r in records:
        click.echo(f'{r[0]}\t{r[1]}\t{r[2]}', file=file_h)

def export_asn(dbpath="hubs.db", out='-', max_age=60*60*24):
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT count(*) as C, addr.as_number, addr.as_name
        FROM hub LEFT JOIN addr
        ON hub.ip = addr.ip
        WHERE unixepoch(hub.ts) > unixepoch() - ?
        GROUP BY addr.as_number
        ORDER BY C DESC
        """, (max_age,))
    records = cursor.fetchall()
    file_h = click.open_file(out, 'w')
    for r in records:
        click.echo(f'{r[0]}\t{r[1]}\t{r[2]}', file=file_h)

def export_fids(dbpath="hubs.db", out='-', max_age=60*60*24):
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT hub_info.fid, count(*) AS C
        FROM hub LEFT JOIN hub_info
        ON hub.ip = hub_info.ip AND hub.port = hub_info.port
        WHERE unixepoch(hub.ts) > unixepoch() - ?
        GROUP BY hub_info.fid
        ORDER BY C DESC, addr.as_name ASC
        """, (max_age,))

    records = cursor.fetchall()
    file_h = click.open_file(out, 'w')
    for r in records:
        click.echo(f'{r[0]}\t{r[1]}', file=file_h)

def export_app_version(dbpath="hubs.db", out='-', max_age=60*60*24):
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT app_version, count(*) AS C
        FROM hub 
        WHERE unixepoch(hub.ts) > unixepoch() - ?
        GROUP BY app_version
        ORDER BY C DESC
        """, (max_age,))

    records = cursor.fetchall()
    file_h = click.open_file(out, 'w')
    for r in records:
        click.echo(f'{r[0]}\t{r[1]}', file=file_h)

def export_latlong(dbpath="hubs.db", out='-', max_age=60*60*24):
    """Export IP, port, lat, long"""
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT count(*), addr.latitude, addr.longitude, addr.country_code, addr.zip_code
        FROM hub LEFT JOIN hub_info ,addr
        ON hub.ip = hub_info.ip AND hub.port = hub_info.port AND hub.ip = addr.ip
        WHERE unixepoch(hub.ts) > unixepoch() - ?
        GROUP BY latitude, longitude
        """, (max_age,))
    records = cursor.fetchall()
    with click.open_file(out, 'w') as file_h:
        for r in records:
            click.echo(f'{r[0]}\t{r[1]}\t{r[2]}\t{r[3]}\t{r[4]}', file=file_h)


if __name__ == "__main__":
    export_full()
    export_countries()
    export_fids()
